import factory
from django_factory_boy.auth import UserF


class UserFactory(UserF):
    password = '123456'  # this will be the default password if not set

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user
