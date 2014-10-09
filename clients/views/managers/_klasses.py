from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from clients import forms
from clients import models
from utils import EmailFromTemplate
from utils.views import LoginRequiredMixin, AjaxMixin


class KlassTakingMixin(object):
    """
    A reusable mixin that offers method to send a warning to the class teacher
    telling he is his owner.
    """
    def warn_klass_taken(self, klass):
        """
        Warns the class teacher that he is now related to it.
        """
        email = EmailFromTemplate(
            subject=_('New class under your control'), 
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[klass.teacher.email],
            template_name='managers/clients/klass_taken_email',
            context={'klass': klass},
        )
        email.send()


class KlassCreateView(LoginRequiredMixin, AjaxMixin, KlassTakingMixin, generic.CreateView):
    """
    Let the logged in user create a new class for any managed contract.
    """
    model = models.Klass
    form_class = forms.KlassForm
    template_name = 'managers/clients/klass_create.html'

    def get_form_kwargs(self):
        """
        Puts the contract on the form and let it filter the teachers
        by contract. The client can handle only his own contracts.
        """
        self.contract = get_object_or_404(models.Contract,
                                          client__managers=self.request.user,
                                          pk=self.kwargs['contract_pk'])
        kwargs = super(KlassCreateView, self).get_form_kwargs()
        kwargs['contract'] = self.contract
        return kwargs

    @method_decorator(transaction.commit_on_success)
    def form_valid(self, form):
        klass = self.klass = form.save(commit=False)
        klass.contract = self.contract
        klass.save()

        if klass.teacher:
            self.warn_klass_taken(klass)

        return redirect('manager:klass-detail',
                        pk=self.klass.pk,
                        contract_pk=self.klass.contract.pk)

    def get_context_data(self, **kwargs):
        kwargs = super(KlassCreateView, self).get_context_data(**kwargs)
        kwargs['contract'] = self.contract
        return kwargs



class ManagedKlassesMixin(object):
    """
    A Mixin that offers a list of classes from contracts whose
    the logged in user is manager.
    """
    def get_queryset(self):
        return models.Klass.objects.filter(contract__client__managers=self.request.user)


class ContractKlassDetailView(LoginRequiredMixin, AjaxMixin, ManagedKlassesMixin, 
                              generic.DetailView):
    """
    Details a class from a contract managed by the logged in user.
    """
    template_name = 'managers/clients/klass_detail.html'


class KlassUpdateView(LoginRequiredMixin, AjaxMixin, ManagedKlassesMixin, 
                      KlassTakingMixin, generic.UpdateView):
    """
    Details a class from a contract managed by the logged in user.
    """
    form_class = forms.KlassForm
    template_name = 'managers/clients/klass_update.html'

    def post(self, request, *args, **kwargs):
        self.initial_teacher = self.get_object().teacher
        return super(KlassUpdateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        if self.object.teacher and self.object.teacher != self.initial_teacher:
            self.warn_klass_taken(self.object)
        
        return reverse('manager:klass-detail', kwargs={
                'pk': self.object.pk,
                'contract_pk': self.object.contract.pk})


class KlassDeleteView(LoginRequiredMixin, AjaxMixin, ManagedKlassesMixin, generic.DeleteView):
    """
    Let the user updates the name and the teachers of a class from a
    contract managed by the logged in user.
    """
    template_name = 'managers/clients/klass_confirm_delete.html'

    def get_success_url(self):
        if not self.request.is_ajax():
            messages.success(self.request, _('Class deleted successfully!'))
        return reverse('manager:contract-list')
