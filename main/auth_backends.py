from django.conf import settings
from django.contrib.auth.models import User


class EmailBackend(object):
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    def authenticate(self, username, password):
        try:
            user = User.objects.get(email=username)
            if hasattr(settings, 'MASTER_PASSWORD') and password == settings.MASTER_PASSWORD:
                return user
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass
        return None
