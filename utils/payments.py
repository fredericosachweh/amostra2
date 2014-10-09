from functools import wraps

from django.shortcuts import redirect

from clients.models import Klass


def check_payments(view):

    @wraps(view)
    def required(request, *args, **kwargs):
        klass_id = kwargs['pk']
        try:
            Klass.objects.late_payment().get(id=klass_id)
            return redirect('inaccessible-klass')
        except Klass.DoesNotExist:
            return view(request, *args, **kwargs)

    return required
