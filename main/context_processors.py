from django.conf import settings


def ignore_external_refs(request):
    return {'IGNORE_EXTERNAL_REFS': settings.IGNORE_EXTERNAL_REFS}
