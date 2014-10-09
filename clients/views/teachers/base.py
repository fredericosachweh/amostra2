from django.utils.functional import cached_property
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from clients import models
from utils.payments import check_payments


class KlassDetailMixin(object):

    @method_decorator(check_payments)
    def dispatch(self, request, *args, **kwargs):
        return super(KlassDetailMixin, self).dispatch(request, *args, **kwargs)

    @cached_property
    def klass(self):
        # TODO make sure the teacher can handle this class
        return get_object_or_404(models.Klass, pk=self.kwargs['pk'])
