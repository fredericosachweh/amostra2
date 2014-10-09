from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.utils.functional import cached_property
from django.views import generic

from accounts.views import LoginView
from clients import forms, models


class KlassAccessView(generic.FormView):
    """
    Redirects to the klass found at the specified klass key.
    """
    template_name = 'students/clients/klass_access.html'
    form_class = forms.KlassSearchForm

    def form_valid(self, form):
        klass = form.cleaned_data['klass']
        return redirect('student:klass-login', key=klass.key)

    def get_context_data(self, **kwargs):
        context = super(KlassAccessView, self).get_context_data(**kwargs)
        context['login_form'] = AuthenticationForm()
        return context


class KlassLoginView(LoginView):
    """
    Lists the users of a program and let the user access as some of then, giving his password.
    """
    template_name = 'students/clients/klass_login.html'
    form_class = forms.KlassLoginForm

    @cached_property
    def klass(self):
        return models.Klass.objects.get(key=self.kwargs['key'])

    def get_form_kwargs(self):
        kwargs = super(KlassLoginView, self).get_form_kwargs()
        kwargs['klass'] = self.klass
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(KlassLoginView, self).get_context_data(**kwargs)
        context['klass'] = self.klass
        return context
