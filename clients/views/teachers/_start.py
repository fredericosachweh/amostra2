from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import generic

from base import KlassDetailMixin
from clients import forms
from exercises.models import UserBattery
from utils.models import id_as_username, generate_random_passwords
from utils.payments import check_payments
from utils.views import LoginRequiredMixin, AjaxMixin


class KlassStartView(AjaxMixin, KlassDetailMixin, LoginRequiredMixin, generic.FormView):
    template_name = 'teachers/clients/klass_start.html'
    form_class = forms.KlassStartForm

    def get_form_kwargs(self):
        kwargs = super(KlassStartView, self).get_form_kwargs()
        kwargs['klass'] = self.klass
        return kwargs

    def get_success_url(self):
        return redirect('teacher:klass-started', pk=self.klass.pk)

    def get_context_data(self, *args, **kwargs):
        context = super(KlassStartView, self).get_context_data(*args, **kwargs)
        context['klass'] = self.klass
        return context

    @method_decorator(transaction.commit_on_success)
    def form_valid(self, form):
        self.create_program_usage(**form.cleaned_data)
        self.create_students(form.cleaned_data['students'])
        return self.get_success_url()

    def create_program_usage(self, program, start_date, end_date, modules, **kwargs):
        program_usage = program.programusage_set.create(klass=self.klass,
                                                        start_date=start_date,
                                                        end_date=end_date)
        program_usage.distribute_batteries(modules)

    def create_students(self, students, **kwargs):
        passwords = generate_random_passwords(len(students))
        users = []

        for i, (first_name, last_name) in enumerate(students):
            user = User(
                username=id_as_username('student'),
                first_name=first_name,
                last_name=last_name,
            )
            user.set_password(passwords[i])
            user.save()

            self.klass.students.add(user)
            users.append(user.pk)

        # saves the pair user
        users_passwords = self.request.session.get('password_list', {})
        users_passwords[self.klass.pk] = zip(users, passwords)
        self.request.session['password_list'] = users_passwords


class KlassRescheduleView(KlassStartView):
    """
    Same as the klass start but don't deal with students, just reset the
    already existent users passwords.
    """
    template_name = 'teachers/clients/klass_reschedule.html'
    form_class = forms.KlassRescheduleForm

    def form_valid(self, form):
        self.klass.program_usage.delete()

        self.client = self.klass.contract.client
        self.teacher = self.klass.teacher.teacher_set.get(client=self.client)

        self.create_program_usage(**form.cleaned_data)
        self.reset_passwords(self.klass.students.all())

        return self.get_success_url()

    def reset_passwords(self, students):
        password_list = generate_random_passwords(len(students))
        pw_list = {}

        for student in students:
            password = password_list.pop(0)
            student.set_password(password)
            student.save()
            pw_list[student.get_full_name()] = password

        klass_pw_list = {self.klass.pk: pw_list}
        try:
            self.request.session['password_list'].update(klass_pw_list)
        except KeyError:
            self.request.session['password_list'] = klass_pw_list


class KlassAutoResetPasswordsView(KlassDetailMixin, generic.RedirectView):
    permanent = False

    def get(self, request, *args, **kwargs):
        if not UserBattery.objects.filter(battery__program__programusage__klass=self.klass).count():
            self.reset_passwords(self.klass.students.all())
        return super(KlassAutoResetPasswordsView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse('teacher:klass-started', kwargs={'pk': self.klass.pk})

    def reset_passwords(self, students):
        password_list = generate_random_passwords(len(students))
        pw_list = {}

        for student in students:
            password = password_list.pop(0)
            student.set_password(password)
            student.save()
            pw_list[student.get_full_name()] = password

        klass_pw_list = {self.klass.pk: pw_list}
        try:
            self.request.session['password_list'].update(klass_pw_list)
        except KeyError:
            self.request.session['password_list'] = klass_pw_list
