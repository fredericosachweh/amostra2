import datetime
import factory

from accounts.factories import UserFactory
from models import Client, Teacher, Contract, Klass


class TeacherFactory(factory.DjangoModelFactory):
    """
    Factory for the Teacher model, that relates a client to an user.
    """
    FACTORY_FOR = Teacher
    teacher = factory.LazyAttribute(lambda a: UserFactory())
    client = factory.LazyAttribute(lambda a: ClientFactory())

    @factory.post_generation
    def email(self, create, extracted, **kwargs):
        """
        Updates the created user if specified an email.
        """
        if not create:
            return

        if extracted:
            self.teacher.email = extracted
            self.teacher.save()


class ClientFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Client
    name = factory.Sequence(lambda n: 'Cliente {0}'.format(n))

    @factory.post_generation
    def managers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for manager in extracted:
                self.managers.add(manager)


class ContractFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Contract
    client = factory.LazyAttribute(lambda a: ClientFactory())


class KlassFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Klass
    name = 'Sample Class'
    contract = factory.LazyAttribute(lambda a: ContractFactory())
    end_date = factory.LazyAttribute(lambda a: datetime.date(datetime.date.today().year, 12, 23))
