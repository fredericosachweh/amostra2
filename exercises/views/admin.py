import csv
from decimal import Decimal as D

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.utils.datastructures import SortedDict
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from exercises import forms
from exercises import models
from exercises.views.main import BaseChanceCreateView, BaseChanceDetailView
from utils.views import LoginRequiredMixin


class CategoryFillView(generic.FormView):
    """
    Given a csv file, fill the category with exercises based on the fields
    defined on the category configuration.
    """
    form_class = forms.CSVImportForm
    template_name = 'admin/exercises/category/category_fill.html'

    @cached_property
    def category(self):
        return get_object_or_404(models.Category.objects.all(), pk=self.kwargs['pk'])

    @cached_property
    def questiontypes(self):
        qs = self.category.questiontype_set.all()
        return dict([(t.group_short.lower(), t) for t in qs])

    @cached_property
    def answertypes(self):
        qs = self.category.answertype_set.all()
        return dict([(t.group_short.lower(), t) for t in qs])

    def get_context_data(self, **kwargs):
        context = super(CategoryFillView, self).get_context_data(**kwargs)
        context['category'] = self.category
        context['title'] = 'Import from CSV'
        return context

    @method_decorator(transaction.commit_on_success)
    def form_valid(self, form):
        has_unexpected_columns = False
        keys = []
        counter = 0

        csv_file = form.cleaned_data['csv_file']
        csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')
        for row in csv_reader:
            description, columns = row[0], row[1:]

            # The first row has columns names and indexes
            if not keys:
                for col in columns:
                    group, index = col.split('-')
                    index = int(index) - 1 # convert 1-based to 0-based
                    keys.append((col, group.lower(), index))
                continue

            counter += 1
            exercise = self.category.exercise_set.create(description=description)

            # Groups the keys with correponding values and then sort they
            # together using the col original description
            group = zip(keys, columns)
            sorted_group = sorted(group, lambda x, y: cmp(x[0][0], y[0][0]))

            answers = {}

            for (col, group, index), value in sorted_group:
                # ignore blank values: we are dealing with a multidimensional
                # model, e.g. we can have 7 spaces to answers in a group but
                # uses only 4 of them.
                if value == '':
                    continue

                if group in self.questiontypes:
                    base = self.questiontypes[group]
                    question = models.Question(
                        exercise=exercise,
                        type=base.type,
                        position=index,
                        group=base.group
                    )
                    question.value = value
                    question.save()

                elif group in self.answertypes:
                    base = self.answertypes[group]
                    if base.type not in ('exact', 'boolean'):
                        raise ValueError('For now, only exact or boolean answers can be imported')

                    # convert a blank value to null, once it will be used on a
                    # decimal field
                    if value == '':
                        value = None

                    answer = models.Answer(
                        exercise=exercise,
                        type=base.type,
                        position=index,
                        group=base.group,
                        value=value
                    )
                    answer.next_group = base.next_group
                    try:
                        answers[base.group].append(answer)
                    except KeyError:
                        answers[base.group] = [answer]

                else:
                    has_unexpected_columns = True

            tabindex = 1
            answer = answers['resultado'].pop(0)

            while 1:
                answer.tabindex = tabindex
                answer.save()
                print tabindex, answer.group

                tabindex += 1
                next_groups = answer.next_group.split(' ')
                answer = None
                for next_group in next_groups:
                    try:
                        answer = answers[next_group].pop(0)
                    except KeyError:
                        continue
                    except IndexError:
                        continue
                    finally:
                        if answer is not None:
                            break

                if answer is None:
                    break

        if has_unexpected_columns:
            messages.warning(self.request, _('Unexpected columns was ignored!'))
        messages.success(self.request, _('%d exercises imported successfully') % counter)
        url = reverse('admin:exercises_exercise_changelist') + ('?category__id__exact=%d' % self.category.id)
        return redirect(url)  # redirects the user to the exercise list filtered by category


class CategoryDuplicateView(generic.RedirectView):
    """
    Creates a new instance of the category with a copy of the question and
    answer types. It is usefull to create a more complex exercise category
    based on a simpler one.
    """
    permanent = False

    def get_redirect_url(self, **kwargs):
        category = get_object_or_404(models.Category.objects.all(), pk=self.kwargs['pk'])
        new_category = models.Category.objects.create(subject=category.subject, matter=category.matter, 
                                                      name=category.name + ' copy', slug=category.slug + '-copy')
        for type in category.questiontype_set.all():
            models.QuestionType.objects.create(category=new_category, type=type.type, 
                                               group=type.group, repeat=type.repeat)
        for type in category.answertype_set.all():
            models.AnswerType.objects.create(category=new_category, type=type.type, 
                                             group=type.group, repeat=type.repeat)
        messages.success(self.request, _('Category duplication sucessful'))
        return reverse('admin:exercises_category_change', args=(new_category.id,))


class ProgramAuditView(generic.TemplateView):
    template_name = 'admin/exercises/program/audit.html'

    rowspan_subquery = '''\
        select count(*) from exercises_categoryusage self
        where self.battery_id = exercises_categoryusage.battery_id'''

    @cached_property
    def program(self):
        return models.Program.objects.get(pk=self.kwargs['pk'])

    def get_usages(self):
        """
        Lists program's category usages with exercises count.

        For each category usage in the program, yields the usage and how many
        exercises are there for such filter options.

        It can't be done easily through raw sql because of the tags filtering,
        this we, even if it is a bottleneck, this is not a critical point.
        """
        qs = models.CategoryUsage.objects.filter(
                battery__module__program=self.program)
        qs = qs.select_related('battery', 'battery__module', 'category')
        qs = qs.order_by('battery__module', 'battery')
        qs = qs.extra(select={'rowspan': self.rowspan_subquery})
        for usage in qs:
            qs = usage.category.exercise_set.all()
            clauses = usage.get_clauses()
            if clauses:
                qs = qs.filter(clauses)
            available = qs.count()

            rate = D(available) / usage.exercises_count
            if rate < 1:
                label = 'incomplete'
            elif rate < 3:
                label = 'too-less'
            elif rate > 100:
                label = 'too-much'
            else:
                label = 'enough'
            yield (usage, available, label)

    def get_context_data(self, **kwargs):
        context = super(ProgramAuditView, self).get_context_data(**kwargs)
        context['program'] = self.program
        context['title'] = _('Program batteries')
        context['usages'] = self.get_usages()
        return context


class ProgramReplaceView(generic.FormView):
    template_name = 'admin/exercises/program/program_replace.html'
    form_class = forms.CSVImportForm

    @cached_property
    def program(self):
        return get_object_or_404(models.Program, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ProgramReplaceView, self).get_context_data(**kwargs)
        context['program'] = self.program
        context['title'] = _('Replace program from CSV import')
        return context

    def get_success_url(self):
        return reverse('admin:exercises_program_change', args=(self.program.pk,))

    @method_decorator(transaction.commit_manually)
    def form_valid(self, form):
        csv_file = form.cleaned_data['csv_file']
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

        try:
            self.replace_program(csv_reader)
        except Exception:
            transaction.rollback()
            raise

        messages.success(self.request, _('Program redefinition successful'))
        transaction.commit()
        return redirect(self.get_success_url())

    def format_number(self, number):
        print number
        if number == '':
            return None
        else:
            return D(number.replace(',', '.'))

    def replace_program(self, csv_reader):
        # clear any module/battery already registered
        self.program.module_set.all().delete()

        module_position = 1
        battery_position = 1
        first_row_ignored = False

        for row in csv_reader:
            if not first_row_ignored:
                first_row_ignored = True
                continue

            # autodetect the encoding
            try:
                row = [s.decode('utf-8') for s in row]
            except UnicodeDecodeError:
                row = [s.decode('iso-8859-1') for s in row]

            (day, status, module_name, syllabus, battery_name, category_name,
             tags, count, sorting, f1_low, f1_up, f2_low, f2_up) = row[:13]

            # when the day is blank, the row represents another category usage
            # for the previous day/battery
            if day:
                try:
                    module = self.program.module_set.get(name=module_name)
                except models.Module.DoesNotExist:
                    module = self.program.module_set.create(
                        name=module_name,
                        position=module_position,
                        syllabus=syllabus
                    )
                    module_position += 1

                battery = module.battery_set.create(name=battery_name,
                                                    position=battery_position)
                battery_position += 1

            try:
                category = models.Category.objects.get(name__iexact=category_name.strip())
            except models.Category.DoesNotExist:
                messages.error(self.request, _('Category not found: "{0}"').format(category_name))
                transaction.rollback()
                return redirect(self.get_success_url())

            # Terms in pt-br aleatorio/sequencial that means random/sequential
            if sorting.lower().startswith('a'):
                random_sorting = True
            else:
                random_sorting = False

            battery.categoryusage_set.create(
                category=category,
                exercises_count=count,
                random_sorting=random_sorting,
                filter1_lower=self.format_number(f1_low),
                filter1_upper=self.format_number(f1_up),
                filter2_lower=self.format_number(f2_low),
                filter2_upper=self.format_number(f2_up),
                tags=tags.strip()
            )


class FreeFromBatteryChanceMixin(object):
    def get_next_url(self):
        """
        Returns None for the next_url because standalone
        exercises won't have a next one.
        """
        return None

    def get_pager(self):
        """ Returns 1 of 1 for only one standalone exercise. """
        return {'current': 1, 'count': 1}


class ChanceCreateView(LoginRequiredMixin,
                       FreeFromBatteryChanceMixin,
                       BaseChanceCreateView):
    """
    Shows a chance form free of an user_battery_exercise. This way, an admin
    user can test an exercise solving without need to be on a battery.
    """
    @cached_property
    def exercise(self):
        return get_object_or_404(models.Exercise, pk=self.kwargs['pk'])

    def get_object(self):
        return self.exercise.chance_set.create()

    def get_success_url(self):
        return reverse('admin-chance-detail',
                       kwargs={'pk': self.object.pk})


class ChanceDetailView(LoginRequiredMixin,
                       FreeFromBatteryChanceMixin,
                       BaseChanceDetailView):
    def get_object(self):
        return models.Chance.objects.get(pk=self.kwargs['pk'])

    def get_done_url(self):
        """
        A standalone exercise won't have a done url. The lack of just will
        cause the done button to be hidden in template.
        """
        None


class ProgramUsageAuditView(generic.DetailView):
    template_name = 'admin/exercises/programusage/audit.html'
    model = models.ProgramUsage

    def get_context_data(self, **kwargs):
        context = super(ProgramUsageAuditView, self).get_context_data(**kwargs)
        context['title'] = _('Audit program usage')
        return context

