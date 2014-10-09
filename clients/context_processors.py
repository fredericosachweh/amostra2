from django.conf import settings


def klasses_cost(request):
    return {'KLASSES_COST': settings.KLASSES_COST}
