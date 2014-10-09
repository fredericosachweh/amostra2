from decimal import Decimal

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from clients.models import Klass
from exercises import forms
from exercises import models
from utils.views import LoginRequiredMixin


class UserBatteriesListView(LoginRequiredMixin, generic.ListView):
    """
    Lists the batteries available on the user program today.
    """
    def get_queryset(self):
        today = timezone.now().date()
        batteries = models.BatterySchedule.objects.pending_for_user(self.request.user)
        batteries = batteries.filter(date=today)
        batteries = batteries.select_related('battery',
                                             'battery__module',
                                             'battery__module__matter')
        return batteries

    def get_context_data(self, **kwargs):
        context = super(UserBatteriesListView, self).get_context_data(**kwargs)

        klasses = self.get_queryset().values_list('program_usage__klass', flat=True)
        klasses = set(klasses.distinct())
        if len(klasses) == 1:
            context['current_klass'] = Klass.objects.get(pk=klasses.pop())

        return context


class UserBatteryStartView(LoginRequiredMixin, generic.DetailView):
    """
    Gets a battery schedule and creates a new user battery for it.
    """
    template_name = 'exercises/userbattery_start.html'

    def get(self, request, *args, **kwargs):
        user_battery = self.get_object()
        if user_battery.is_done:
            return redirect('student:user-battery-done',
                            user_battery=user_battery.pk)

        return super(UserBatteryStartView, self).get(request, *args, **kwargs)

    def get_object(self):
        schedule = get_object_or_404(models.BatterySchedule, pk=self.kwargs['schedule'])
        user = self.request.user
        user_battery, created = schedule.userbattery_set.get_or_create(user=user)
        return user_battery

    def get_context_data(self, **kwargs):
        context = super(UserBatteryStartView, self).get_context_data(**kwargs)
        context['next'] = self.object.userbatteryexercise_set.next()
        context['current_klass'] = self.object.battery_schedule.program_usage.klass
        return context


class BaseChanceCreateView(generic.UpdateView):
    """
    Reather than updates the exercise, create chances for its questions.
    """
    model = models.UserBatteryExercise
    form_class = forms.ChanceItemFormSet

    def dispatch(self, request, *args, **kwargs):
        self.request, self.args, self.kwargs = request, args, kwargs
        self.object = self.get_object()
        if self.object.is_finished():
            messages.error(request, _('You already answered this exercise!'))
            return redirect(self.get_success_url())
        else:
            return super(BaseChanceCreateView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        """
        Returns a chance for the exercise of the given position in battery.

        If there is an unfinished attempt, reuse it, otherwise, return as many
        attempts as configured, returning the last finished one when exausted
        (it will be filtered in the dispatch method).
        """
        user_exercise = get_object_or_404(
            models.UserBatteryExercise,
            user_battery__pk=self.kwargs['user_battery'],
            user_battery__user=self.request.user,
            position=self.kwargs['position'],
        )

        if user_exercise.chance_set.unfinished().count():
            chance = user_exercise.chance_set.unfinished().get()
        else:
            number = user_exercise.attempts_spent
            if number < user_exercise.user_battery.attempts:
                chance = user_exercise.chance_set.create(number=number + 1)
            else:
                chance = user_exercise.chance_set.finished().reverse()[0]
        return chance

    @cached_property
    def exercise(self):
        return self.object.exercise

    def get_next_url(self):
        """
        Returns the url for the next exercise.
        """
        next = self.object.user_battery_exercise.next()
        if not next:
            return None
        else:
            next_url = reverse('student:chance-create',
                               kwargs={'user_battery': next.user_battery.pk,
                                       'position': next.position})
            return next_url

    def get_pager(self):
        return {'current': self.object.user_battery_exercise.position,
                'count': self.object.user_battery.exercises.count()}

    def get_template_names(self):
        category_slug = self.exercise.category.slug
        subject_slug = self.exercise.subject.slug
        matter_slug = self.exercise.matter.slug
        return [
            'exercises/form/%s/%s/%s.html' % (matter_slug, subject_slug, category_slug),
            'exercises/form/%s/%s/default.html' % (matter_slug, subject_slug),
            'exercises/form/%s.html' % category_slug,
            'exercises/form/default.html'
        ]

    def get_form_kwargs(self):
        """
        The ChanceFormSet expects an exercise to copy fields from.
        """
        kwargs = super(BaseChanceCreateView, self).get_form_kwargs()
        del kwargs['instance']
        kwargs.update({'exercise': self.exercise})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(BaseChanceCreateView, self).get_context_data(**kwargs)
        context['questions'] = self.exercise.questions
        context['answers'] = context['form'].answers
        context['exercise'] = self.exercise
        context['next_url'] = self.get_next_url()
        context['pager'] = self.get_pager()
        return context

    @method_decorator(transaction.commit_on_success)
    def form_valid(self, form):
        """
        Creates the chance items for the current chance.

        There is no way to update a done chance, this way, we can assume a
        chance won't have any chance item before save.
        """
        for f in form:
            item = f.save(commit=False)
            item.chance = self.object
            item.save()
            if item.has_choices():
                item.choices = f.cleaned_data['choices']  # set choices only when really needed

        self.object.finished_at = timezone.now()
        self.object.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        """
        Redirects to the chance-detail view correspondent to the form.
        """
        return self.object.get_absolute_url()


class ChanceCreateView(LoginRequiredMixin, BaseChanceCreateView):
    def get_context_data(self, **kwargs):
        context = super(ChanceCreateView, self).get_context_data(**kwargs)
        context['current_klass'] = self.object.user_battery.battery_schedule.program_usage.klass
        return context


class BaseChanceDetailView(generic.DetailView):
    def get_object(self):
        return get_object_or_404(
            models.Chance,
            user_battery__pk=self.kwargs['user_battery'],
            user_battery__user=self.request.user,
            user_battery_exercise__position=self.kwargs['position'],
            number=self.kwargs['number']
        )

    def get_next_url(self):
        """
        Returns next for current chance or mark the battery as done.

        When there is not exercise left to be solved, marks the user_battery as
        done and returns None, indicating there is no next.
        """
        next = self.object.user_battery_exercise.next()
        if next is None:
            user_battery = self.object.user_battery
            user_battery.is_done = True
            user_battery.save()

            return None
        else:
            return reverse('student:chance-create',
                           kwargs={'user_battery': next.user_battery.pk,
                                   'position': next.position})

    def get_done_url(self):
        """
        Returns the url used when all the exercises where done.
        """
        return reverse('student:user-battery-done',
                       kwargs={'user_battery': self.object.user_battery.pk})

    def get_pager(self):
        return {'current': self.object.user_battery_exercise.position,
                'count': self.object.user_battery.exercises.count()}

    def get_template_names(self):
        category_slug = self.object.exercise.category.slug
        subject_slug = self.object.exercise.subject.slug
        matter_slug = self.object.exercise.matter.slug
        return [
            'exercises/detail/%s/%s/%s.html' % (matter_slug, subject_slug, category_slug),
            'exercises/detail/%s/%s/default.html' % (matter_slug, subject_slug),
            'exercises/detail/%s.html' % category_slug,
            'exercises/detail/default.html'
        ]

    def get_context_data(self, **kwargs):
        context = super(BaseChanceDetailView, self).get_context_data(**kwargs)
        context['questions'] = self.object.exercise.questions
        context['answers'] = self.object.answers
        context['next_url'] = self.get_next_url()
        context['done_url'] = self.get_done_url()
        context['pager'] = self.get_pager()
        return context


class ChanceDetailView(LoginRequiredMixin, BaseChanceDetailView):
    def get_context_data(self, **kwargs):
        context = super(ChanceDetailView, self).get_context_data(**kwargs)
        context['current_klass'] = self.object.user_battery.battery_schedule.program_usage.klass
        return context


class UserBatteryDoneView(LoginRequiredMixin, generic.DetailView):
    template_name = 'exercises/userbattery_done.html'

    def get_object(self):
        return get_object_or_404(
            self.request.user.userbattery_set.all(),
            pk=self.kwargs['user_battery']
        )

    def get_context_data(self, **kwargs):
        context = super(UserBatteryDoneView, self).get_context_data(**kwargs)
        context['exercises_count'] = self.object.exercises.count()
        context['correct_count'] = self.object.userbatteryexercise_set.correct().count()
        context['success_rate'] = context['correct_count'] / Decimal(context['exercises_count'])
        context['current_klass'] = self.object.battery_schedule.program_usage.klass
        return context


# teachers views

class ProgramUsageDetailView(generic.DetailView):
    template_name = 'teachers/exercises/programusage_detail.html'

    def get_object(self):
        program_usage = models.ProgramUsage.objects.get(klass__teacher=self.request.user,
                                                        pk=self.kwargs['pk'])
        return program_usage


class SyllabusListView(generic.ListView):
    template_name = 'exercises/syllabus_list.html'
    model = models.Program

    def get_queryset(self):
        queryset = super(SyllabusListView, self).get_queryset()
        program = queryset.get(pk=self.kwargs['pk'])
        return program.module_set.all().select_related()
