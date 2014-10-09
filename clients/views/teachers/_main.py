from decimal import Decimal
import datetime

from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.utils.datastructures import SortedDict

from base import KlassDetailMixin
from clients import forms, models
from exercises.models import UserBattery
from utils.models import generate_random_passwords
from utils.views import LoginRequiredMixin, AjaxMixin, PdfMixin
from utils.payments import check_payments


class KlassListView(LoginRequiredMixin, generic.ListView):
    """
    Lists a set of klasses whose teacher is the logged in user.
    """
    template_name = 'teachers/clients/klass_list.html'

    def get_queryset(self):
        return models.Klass.objects.filter(teacher=self.request.user)


class KlassDetailView(LoginRequiredMixin, generic.DetailView):
    @method_decorator(check_payments)
    def dispatch(self, request, *args, **kwargs):
        return super(KlassDetailView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.taught_klasses.all()

    def get_context_data(self, **kwargs):
        context = super(KlassDetailView, self).get_context_data(**kwargs)
        context['passwd_form'] = forms.KlassPasswdForm(instance=self.object)
        return context


class KlassPerformanceMixin(object):

    @method_decorator(check_payments)
    def dispatch(self, request, *args, **kwargs):
        return super(KlassDetailView, self).dispatch(request, *args, **kwargs)

    def get_performance(self, dates=None):
        subquery = '''
        SELECT {what} FROM exercises_userbattery, exercises_batteryschedule
        WHERE exercises_userbattery.user_id = auth_user.id
        AND exercises_userbattery.battery_schedule_id = exercises_batteryschedule.id '''

        if dates:
            subquery += '''
            AND exercises_batteryschedule.date >= '{start_date}'
            AND exercises_batteryschedule.date <= '{end_date}'
            '''.format(**dates)

        # TODO ordering must come from custom user model
        users = self.get_object().students.all().order_by('first_name', 'last_name').extra(select={
            'batteries_count': subquery.format(what='COUNT(exercises_userbattery.id)'),
            'exercises_count': subquery.format(what='SUM(exercises_userbattery.exercises_count)'),
            'correct_answers': subquery.format(what='SUM(exercises_userbattery.correct_answers)'),
            'attempts': subquery.format(what='SUM(exercises_userbattery.attempts_spent)'),
            'time': subquery.format(what='SUM(exercises_userbattery.time_spent)'),
        })
        for user in users:
            if not user.exercises_count:
                yield user, {}
            else:
                exercises_count = Decimal(int(user.exercises_count))
                yield user, {
                    'correct_answers': user.correct_answers,
                    'exercises_count': user.exercises_count,
                    'score': Decimal(int(user.correct_answers)) / exercises_count * 10,
                    'attempts': Decimal(str(user.attempts)) / exercises_count,
                    'time': user.time / user.batteries_count
                }


class KlassDashboardView(KlassPerformanceMixin, KlassDetailView):
    template_name = 'teachers/clients/klass_dashboard.html'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.password_list_printed_at:
            return super(KlassDashboardView, self).get(request, *args, **kwargs)

        password_list = request.session.get('password_list', {})
        if str(obj.pk) in password_list:
            return redirect('teacher:klass-started', pk=obj.pk)

        if datetime.date.today() < obj.program_usage.start_date:
            return redirect('teacher:klass-auto-reset-passwords', pk=obj.pk)
        else:
            if UserBattery.objects.filter(battery__module__program__programusage__klass=obj).count():
                raise Exception('You should not be here. Class started without passwords?')
            else:
                return redirect('teacher:klass-reschedule', pk=obj.pk)

    def get_context_data(self, **kwargs):
        context = super(KlassDashboardView, self).get_context_data(**kwargs)
        context['performance'] = self.get_performance()
        context['performance_form'] = forms.PerformanceForm(klass=self.get_object())
        return context


class KlassPerformanceView(KlassPerformanceMixin, KlassDetailView):
    template_name = 'teachers/clients/klass_performance.html'

    def get_context_data(self, **kwargs):
        context = super(KlassPerformanceView, self).get_context_data(**kwargs)
        context['form'] = form = forms.PerformanceForm(data=self.request.GET, klass=self.get_object())
        if form.is_valid():
            dates = dict([(k, v.strftime('%Y-%m-%d')) for k, v in form.cleaned_data.items()])
        else:
            dates = None
        context['performance'] = self.get_performance(dates)
        return context


class PasswdListView(PdfMixin, KlassDetailMixin, LoginRequiredMixin, generic.TemplateView):
    """
    Renders the PDF password list and saves in the klass the passwords were
    printed.
    """
    template_name = 'teachers/clients/passwd_list.html'

    def get(self, request, *args, **kwargs):
        password_list = request.session.get('password_list', {})

        if str(self.klass.pk) in password_list:
            self.klass.password_list_printed_at = timezone.now()
            self.klass.save()

            self.passwords = SortedDict(password_list[str(self.klass.pk)])
            return super(PasswdListView, self).get(request, *args, **kwargs)
        else:
            raise ValueError('You are trying to access the pdf list of passwords'
                             ' but it is not in the session.')

    def get_context_data(self, *args, **kwargs):
        context = super(PasswdListView, self).get_context_data(*args, **kwargs)
        context['klass'] = self.klass

        users = User.objects.filter(pk__in=self.passwords.keys())
        context['passwords'] = zip(users, self.passwords.values())
        return context


class PasswdUpdateView(AjaxMixin, LoginRequiredMixin, generic.UpdateView):
    template_name = 'teachers/clients/passwd_update.html'
    form_class = forms.KlassPasswdForm

    @method_decorator(check_payments)
    def dispatch(self, request, *args, **kwargs):
        return super(KlassDetailView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return models.Klass.objects.filter(teacher=self.request.user)  # TODO DRY

    def get_success_url(self):
        return redirect('teacher:passwd-updated', pk=self.object.pk)

    def form_valid(self, form):
        self.object.password_list_printed_at = None
        self.object.save()

        # reather than update the students list, use the students list to reset
        # their passwords
        users = form.cleaned_data['students']
        passwords = generate_random_passwords(len(users))
        users_passwords = []
        for user, passwd in zip(users, passwords):
            user.set_password(passwd)
            user.save()
            users_passwords.append((user.pk, passwd))

        # saves the pair user
        password_list = self.request.session.get('password_list', {})
        password_list[str(self.object.pk)] = users_passwords
        self.request.session['password_list'] = password_list
        return self.get_success_url()
