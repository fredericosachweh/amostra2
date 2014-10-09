from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.views import generic

import forms
from clients.forms import KlassSearchForm


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()

        # According to the user profile, redirect it to the proper place
        if request.user.is_authenticated():
            redirect_to = request.user.get_home_url()
            return redirect(redirect_to)
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        # Login before know where to redirect
        auth_login(self.request, form.get_user())
        redirect_to = self.request.user.get_home_url()
        return redirect(redirect_to)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['klass_form'] = KlassSearchForm()
        return context


class AccountUpdateView(generic.UpdateView):
    form_class = forms.UserForm
    template_name = 'registration/user_update.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, _('User account update successful'))
        return reverse('accounts:user-update')
