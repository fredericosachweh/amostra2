import factory
import models


class MatterFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Matter
    name = factory.Sequence(lambda n: 'Matter {0}'.format(n))
    slug = factory.Sequence(lambda n: 'matter-{0}'.format(n))


class SubjectFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Subject
    matter = factory.LazyAttribute(lambda a: MatterFactory())
    name = factory.Sequence(lambda n: 'Subject {0}'.format(n))
    slug = factory.Sequence(lambda n: 'subject-{0}'.format(n))
    description = factory.Sequence(lambda n: 'Subject description'.format(n))


class CategoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Category
    subject = factory.LazyAttribute(lambda a: SubjectFactory())
    matter = factory.LazyAttribute(lambda a: a.subject.matter)
    name = factory.Sequence(lambda n: 'Category {0}'.format(n))
    slug = factory.Sequence(lambda n: 'category-{0}'.format(n))
