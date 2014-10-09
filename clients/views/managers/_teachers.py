from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from clients import forms
from utils import EmailFromTemplate
from utils.models import id_as_username, generate_random_passwords
from utils.views import LoginRequiredMixin, AjaxMixin


class ManagedTeachersMixin(object):
    pass


class TeacherListView(LoginRequiredMixin, AjaxMixin, generic.ListView):
    """
    Lists the teachers related to the logged in user's clients.
    """
    template_name = 'managers/clients/teacher_list.html'

    def get_queryset(self):
        users = User.objects.filter(teacher__client__managers=self.request.user).distinct()
        users = users.annotate(klasses_count=Count('taught_klasses', distinct=True))
        # TODO taught_klasses doesn't filter this client items
        return users

    def get_context_data(self, **kwargs):
        """
        Tells how many are the managed clients to decide to show or not show
        the update link (there's no need to update when there is only one
        choice).
        """
        # TODO DRY - when using django 1.5, put it in the view obj
        context = super(TeacherListView, self).get_context_data(**kwargs)
        context['managed_clients_count'] = self.request.user.managed_clients.count()
        return context


class TeacherDetailView(LoginRequiredMixin, AjaxMixin, generic.DetailView):
    template_name = 'managers/clients/teacher_detail.html'

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        """
        Tells how many are the managed clients to decide to show or not show
        the update link (there's no need to update when there is only one
        choice).
        """
        # TODO DRY - when using django 1.5, put it in the view obj
        context = super(TeacherDetailView, self).get_context_data(**kwargs)
        context['managed_clients_count'] = self.request.user.managed_clients.count()
        return context


class TeacherCreateView(LoginRequiredMixin, AjaxMixin, generic.FormView):
    """
    Asks the user for a name and an email of a new teacher. The email
    will be checked and, if it already exists, the existing
    teacher will just be attached to the client.

    If the logged in user has more than one client related to it, offers a
    field to choose what clients the new teacher will be attached to.
    """
    template_name = 'managers/clients/teacher_create.html'
    form_class = forms.TeacherCreateForm

    def get_form_kwargs(self):
        """
        Puts the contract on the form and let it filter the teachers
        by contract. The client can handle only his own contracts.
        """
        kwargs = super(TeacherCreateView, self).get_form_kwargs()
        kwargs['manager'] = self.request.user
        return kwargs

    def form_valid(self, form):
        first_name, last_name = form.cleaned_data['name']
        email = form.cleaned_data['email']

        if 'clients' in form.fields:
            clients = form.cleaned_data['clients']
        else:
            # if the manager has only one client, the form doen't have the
            # clients field, we must set it separated
            clients = self.request.user.managed_clients.all()

        try:
            # avoids double registration by trying to use an already existant
            # user and filters his attached clients from the manager choices
            teacher_user = User.objects.get(email=email)
            password = None
            clients = clients.exclude(teachers=teacher_user)
        except User.DoesNotExist:
            teacher_user = User(first_name=first_name,
                                last_name=last_name,
                                username=id_as_username('teacher'),
                                email=email)
            password = generate_random_passwords(1, flat=True)
            teacher_user.set_password(password)
            teacher_user.save()

            self.warn_user_create(teacher_user, password, clients)

        for client in clients:
            teacher_user.teacher_set.create(client=client)

        return redirect('manager:teacher-detail', pk=teacher_user.pk)

    def warn_user_create(self, user, password, clients):
        """
        Sends an email to the just created user with his
        password and instructions.
        """
        email = EmailFromTemplate(
            subject=_('Welcome to Mainiti'),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
            template_name='managers/clients/teacher_created_email',
            context={'user': user, 'password': password, 'clients': clients},
        )
        email.send()


class TeacherUpdateView(LoginRequiredMixin, AjaxMixin, generic.FormView):
    """
    Let the user set to what clients the teacher will be related.
    """
    template_name = 'managers/clients/teacher_update.html'
    form_class = forms.TeacherUpdateForm

    def get_form_kwargs(self):
        """
        Puts the contract on the form and let it filter the teachers
        by contract. The client can handle only his own contracts.
        """
        kwargs = super(TeacherUpdateView, self).get_form_kwargs()
        kwargs['manager'] = self.request.user
        return kwargs

    def get_initial(self):
        teacher_pk = self.kwargs['pk']
        teacher = self.teacher = User.objects.get(pk=teacher_pk)
        return {'clients': [t.client for t in teacher.teacher_set.all()]}

    def form_valid(self, form):
        """
        Clears all teacher instances related to logged in user clients and
        creates the selected ones again.
        """
        manager = self.request.user
        self.teacher.teacher_set.filter(client__managers=manager).delete()

        if 'clients' in form.fields:
            clients = form.cleaned_data['clients']
        else:
            clients = self.request.user.managed_clients.all()

        for client in clients:
            self.teacher.teacher_set.create(client=client)

        return redirect('manager:teacher-detail', pk=self.teacher.pk)

    def get_context_data(self, *args, **kwargs):
        context = super(TeacherUpdateView, self).get_context_data(*args, **kwargs)
        context['object'] = self.teacher
        return context


class TeacherDeleteView(LoginRequiredMixin, AjaxMixin, generic.DeleteView):
    """
    Given an user, removes all teacher instances that relates it to the
    logged-in user clients.
    """
    template_name = 'managers/clients/teacher_confirm_delete.html'
    model = User

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

        user = self.get_object()
        manager = request.user
        klasses = user.taught_klasses.filter(contract__client__managers=manager)
        if klasses.count():
            return redirect('manager:teacher-cant-delete', pk=user.pk)
        else:
            return super(TeacherDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        manager = self.request.user
        user.teacher_set.filter(client__managers=manager).delete()
        return redirect('manager:teacher-list')


class TeacherCantDeleteView(LoginRequiredMixin, AjaxMixin, generic.DetailView):
    template_name = 'managers/clients/teacher_cant_delete.html'
    model = User
