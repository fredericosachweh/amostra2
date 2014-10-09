from django.views import generic

from clients import models
from utils.views import LoginRequiredMixin


class ManagedContractsMixin(object):
    """
    A Mixin that offers a list of contracts whose the logged in user is manager.
    """
    def get_queryset(self):
        return models.Contract.objects.filter(client__managers=self.request.user)


class ContractListView(LoginRequiredMixin, ManagedContractsMixin, generic.ListView):
    """ Shows logged in manager contracts. """
    template_name = 'managers/clients/contract_list.html'


class ContractDetailView(LoginRequiredMixin, ManagedContractsMixin, generic.DetailView):
    """ Details logged in manager contract. """
    template_name = 'managers/clients/contract_detail.html'
