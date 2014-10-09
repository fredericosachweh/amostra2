from decimal import Decimal
import datetime
import random

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.template.defaultfilters import floatformat
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from clients.models import Client, Contract, Klass
from excludeddates.models import SystemDate
from utils.models import MultiDict, MultiDictManager


QUESTION_TYPES = [
    ('char', _('One line text')),
    ('boolean', _('Boolean option')),
    ('text', _('Multi line text')),
    ('image', _('Image')),
]


ANSWER_TYPES = [
    ('boolean', _('Boolean')),
    ('digit', _('Exact digit')),
    ('digit_or_blank', _('Exact digit or blank')),
    ('exact', _('Exact')),
    ('exact_or_blank', _('Exact or blank')),
    ('near', _('Approximate')),
    ('radio', _('Single choice')),
    ('checkbox', _('Multiple choices')),
]


class Matter(models.Model):
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('matter')
        verbose_name_plural = _('matters')


class Subject(models.Model):
    matter = models.ForeignKey(Matter, verbose_name=_('matter'))
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'))
    description = models.TextField(_('description'), blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('subject')
        verbose_name_plural = _('subjects')


class CategoryManager(models.Manager):
    def eligible_for_demos(self):
        return self.filter(eligible_for_demos=True)


class Category(models.Model):
    subject = models.ForeignKey(Subject, verbose_name=_('subject'))
    matter = models.ForeignKey(Matter,
                               verbose_name=_('matter'),
                               editable=False,
                               blank=True,
                               null=True)  # autopopulated from the subject
    name = models.CharField(_('name'), max_length=255, db_index=True)
    slug = models.SlugField(_('slug'))
    eligible_for_demos = models.BooleanField(_('eligible for demonstrations?'),
                                             default=False
                                             )
    sites = models.ManyToManyField(Site, verbose_name=_('sites'))
    objects = CategoryManager()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('subject', 'name')
        verbose_name = _('category')
        verbose_name_plural = _('categories')


def set_matter_from_subject(sender, instance, **kwargs):
    instance.matter = instance.subject.matter
models.signals.pre_save.connect(set_matter_from_subject, sender=Category)


class QuestionType(models.Model):
    category = models.ForeignKey(Category, verbose_name=_('category'))
    type = models.CharField(_('type'), max_length=20, choices=QUESTION_TYPES)
    group = models.SlugField(_('group name'), max_length=10)
    group_short = models.SlugField(_('group short name'),
                                   max_length=10,
                                   help_text=_('Short group name for data '
                                               'importing.')
                                   )

    class Meta:
        ordering = ('group',)
        verbose_name = _('question type')
        verbose_name_plural = _('question types')


class AnswerType(models.Model):
    category = models.ForeignKey(Category, verbose_name=_('category'))
    type = models.CharField(_('type'), max_length=20, choices=ANSWER_TYPES)
    group = models.SlugField(_('group name'), max_length=10)
    group_short = models.SlugField(_('group short name'),
                                   max_length=10,
                                   help_text=_('Short group name for data '
                                               'importing.')
                                   )
    next_group = models.CharField(_('next group'), max_length=50)

    class Meta:
        ordering = ('group',)
        verbose_name = _('answer type')
        verbose_name_plural = _('answer types')


class ExerciseManager(models.Manager):
    def public(self):
        return self.filter(is_public=True)

    def get_random(self, used=[]):
        return self.exclude(id__in=used).order_by('?')[0]


class Exercise(models.Model):
    category = models.ForeignKey(Category, verbose_name=_('category'))
    tags = models.CharField(_('tags'),
                            max_length=255,
                            blank=True,
                            db_index=True,
                            help_text=_('Comma separated list of tags to be '
                                        'more specific than category')
                            )
    description = models.TextField(_('description'))
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    # TODO prevent exercise changing after it was being used
    times_used = models.IntegerField(_('times used'), default=0)
    is_public = models.BooleanField(_('is public?'), default=True)
    objects = ExerciseManager()

    # filtering
    filter1 = models.DecimalField(_('filter 1'),
                                  max_digits=17,
                                  decimal_places=9,
                                  blank=True,
                                  null=True,
                                  db_index=True
                                  )
    filter2 = models.DecimalField(_('filter 2'),
                                  max_digits=17,
                                  decimal_places=9,
                                  blank=True,
                                  null=True,
                                  db_index=True
                                  )

    # denornalization
    matter = models.ForeignKey(Matter,
                               verbose_name=_('matter'),
                               editable=False,
                               blank=True,
                               null=True
                               )  # autofilled from the category
    subject = models.ForeignKey(Subject,
                                verbose_name=_('subject'),
                                editable=False,
                                blank=True,
                                null=True
                                )  # autofilled from the category

    def __unicode__(self):
        return self.description

    @models.permalink
    def get_absolute_url(self):
        return ('admin-chance-create', (), {'pk': self.pk})

    @cached_property
    def questions(self):
        return self.question_set.as_dict()

    @cached_property
    def answers(self):
        return self.answer_set.as_dict()

    class Meta:
        verbose_name = _('exercise')
        verbose_name_plural = _('exercises')


def set_matter_and_subject_from_category(sender, instance, **kwargs):
    instance.subject = instance.category.subject
    instance.matter = instance.category.matter
models.signals.pre_save.connect(set_matter_and_subject_from_category,
                                sender=Exercise
                                )


class Question(models.Model):
    exercise = models.ForeignKey(Exercise, verbose_name=_('exercise'))
    type = models.CharField(_('type'), max_length=20, choices=QUESTION_TYPES)
    position = models.PositiveIntegerField(_('position'), default=0)
    group = models.SlugField(_('group'), max_length=20)
    char_value = models.CharField(_('one line text'),
                                  max_length=100,
                                  blank=True
                                  )
    boolean_value = models.NullBooleanField(_('boolean value'),
                                            blank=True,
                                            null=True
                                            )
    text_value = models.TextField(_('multiline text'), blank=True)
    image_value = models.ImageField(_('image'),
                                    upload_to='exercises/question/image_value',
                                    blank=True
                                    )
    objects = MultiDictManager()

    class Meta:
        ordering = ('group', '-position',)
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def get_value(self):
        if self.type == 'char':
            return self.char_value
        if self.type == 'boolean':
            return self.boolean_value
        elif self.type == 'text':
            return self.text_value
        elif self.type == 'image':
            return self.image_value
        else:
            raise ValueError('Wrong question type')

    def set_value(self, value):
        if self.type == 'char':
            self.char_value = value
        elif self.type == 'boolean':
            try:
                self.boolean_value = bool(int(value))
            except ValueError:
                self.boolean_value = True
        elif self.type == 'text':
            self.text_value = value
        elif self.type == 'image':
            raise ValueError('Assign an image value directly in his attribute')
        else:
            raise ValueError('Wrong question type')

    value = property(get_value, set_value)


class Answer(models.Model):
    exercise = models.ForeignKey(Exercise, verbose_name=_('exercise'))
    type = models.CharField(_('type'), max_length=20, choices=ANSWER_TYPES)
    position = models.PositiveIntegerField(_('position'), default=0)
    tabindex = models.IntegerField(_('tabindex'), default=1)
    group = models.SlugField(_('group'), max_length=20)
    value = models.DecimalField(_('value'),
                                max_digits=17,
                                decimal_places=9,
                                blank=True,
                                null=True
                                )
    error_limit = models.DecimalField(_('error limit'),
                                      max_digits=17,
                                      decimal_places=9,
                                      blank=True,
                                      null=True
                                      )
    choices_map = models.TextField(_('choices'),
                                   blank=True,
                                   help_text=_('Set a choice per line, '
                                               'start with a plus sign (+) '
                                               'for a correct choice and a '
                                               'minus sign (-) for a '
                                               'incorrect choice.')
                                   )
    choices_sample = models.IntegerField(_('choices samples'),
                                         blank=True,
                                         null=True,
                                         help_text=_('How many choices to '
                                                     'pick from all choices '
                                                     'map?')
                                         )
    objects = MultiDictManager()

    class Meta:
        ordering = ('group', '-position',)
        verbose_name = _('answer')
        verbose_name_plural = _('answers')

    def get_random_choices(self):
        """
        Returns as many random choices as choices_sample, certifying that all
        correct choices are in this list. We don't want to use database
        randoming as it does not scale well.
        """
        correct = []
        incorrect = []
        for choice in self.choice_set.all():
            if choice.is_correct:
                correct.append(choice)
            else:
                incorrect.append(choice)

        if len(correct) + len(incorrect) == self.choices_sample:
            choices = correct + incorrect
        else:
            limit = self.choices_sample - len(correct)
            if len(incorrect) > limit:
                incorrect = random.sample(incorrect, limit)
            choices = correct + incorrect
        random.shuffle(choices)
        return choices


def create_answer_choices(sender, instance, **kwargs):
    """
    Creates choice instances based on the textual choices filled by the user.
    """
    instance.choice_set.all().delete()
    lines = instance.choices_map.split('\n')
    choices = []
    for line in filter(None, lines):  # blank lines ignored
        sign = line[0:1]
        description = line[1:].strip()
        if sign == '+':
            is_correct = True
        elif sign == '-':
            is_correct = False
        else:
            raise ValueError('Start the answer by a plus sign for a correct '
                             'answer or a minus sign for an incorrect one.')
        choices.append(Choice(answer=instance,
                              description=description,
                              is_correct=is_correct))
    Choice.objects.bulk_create(choices)
models.signals.post_save.connect(create_answer_choices,
                                 sender=Answer,
                                 dispatch_uid='create-choices'
                                 )


class ChoiceManager(models.Manager):
    def correct(self):
        return self.filter(is_correct=True)

    def incorrect(self):
        return self.filter(is_correct=False)


class Choice(models.Model):
    answer = models.ForeignKey(Answer, verbose_name=_('answer'))
    description = models.TextField(_('description'))
    is_correct = models.BooleanField(_('is correct?'))
    objects = ChoiceManager()

    def __unicode__(self):
        return self.description

    class Meta:
        ordering = ('id',)
        verbose_name = _('choice')
        verbose_name_plural = _('choices')


class Program(models.Model):
    matter = models.ForeignKey(Matter, verbose_name=_('matter'))
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    batteries_count = models.IntegerField(_('batteries count'),
                                          default=0,
                                          editable=False,
                                          help_text=_('Would reflect the '
                                                      'number of activity '
                                                      'days.')
                                          )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('exercises program')
        verbose_name_plural = _('exercises programs')


class Module(models.Model):
    program = models.ForeignKey(Program, verbose_name=_('exercises program'))
    name = models.CharField(_('name'), max_length=255)
    batteries_count = models.IntegerField(_('batteries count'),
                                          default=0,
                                          editable=False,
                                          help_text=_('Would reflect the '
                                                      'number of activity '
                                                      'days.')
                                          )

    position = models.PositiveSmallIntegerField('Position')
    syllabus = models.TextField(_('syllabus'), blank=True)

    class Meta:
        ordering = ('position',)
        verbose_name = _('exercises program\'s module')
        verbose_name_plural = _('exercises program\'s modules')

    def __unicode__(self):
        return self.name


class Battery(models.Model):
    module = models.ForeignKey(Module,
                               verbose_name=_('exercises program\'s module')
                               )
    categories = models.ManyToManyField(Category,
                                        blank=True,
                                        null=True, through='CategoryUsage',
                                        help_text=_('Choose categories to '
                                                    'use exercises from')
                                        )
    name = models.CharField(_('optional name'),
                            max_length=255,
                            blank=True, help_text=_('Set an optional name '
                                                    'for the battery.')
                            )

    position = models.PositiveSmallIntegerField(_('position'))

    # denormalization:
    matters_names = models.CharField(_('matters'),
                                     max_length=255,
                                     blank=True,
                                     editable=False
                                     )
    subjects_names = models.CharField(_('subjects'),
                                      max_length=255,
                                      blank=True,
                                      editable=False)
    categories_names = models.TextField(_('categories'),
                                        blank=True,
                                        editable=False)

    class Meta:
        ordering = ('module', 'position',)
        verbose_name = _('exercises battery')
        verbose_name_plural = _('exercises batteries')

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            if self.id:
                return '; '.join([unicode(c) for c in self.categories.all()])
            else:
                return unicode(_('battery'))  # the object don't exist yet,
                                              # we don't have m2m relationships

    @property
    def exercises_count(self):
        return sum([x.exercises_count for x in self.categoryusage_set.all()])


def count_batteries(sender, instance, **kwargs):
    """
    Cache the number of batteries in a module and his program.
    """
    program = instance.module.program
    program_batteries = Battery.objects.filter(module__program=program)
    program.batteries_count = program_batteries.count()
    program.save()

    module = instance.module
    module.batteries_count = module.battery_set.count()
    module.save()
models.signals.post_save.connect(count_batteries, sender=Battery)


class CategoryUsage(models.Model):
    """
    A battery/day may have one or more category usages.
    """
    battery = models.ForeignKey(Battery, verbose_name=_('battery'))
    category = models.ForeignKey(Category, verbose_name=_('category'))
    exercises_count = models.IntegerField(_('exercises count'))
    random_sorting = models.BooleanField(_('sorting'),
                                         choices=[(False, _('Sequential')),
                                                  (True, _('Random'))]
                                         )

    filter1_lower = models.DecimalField(_('filter 1 lower limit'), max_digits=17, decimal_places=9, blank=True, null=True, db_index=True)
    filter1_upper = models.DecimalField(_('filter 1 upper limit'), max_digits=17, decimal_places=9, blank=True, null=True, db_index=True)
    filter2_lower = models.DecimalField(_('filter 2 lower limit'), max_digits=17, decimal_places=9, blank=True, null=True, db_index=True)
    filter2_upper = models.DecimalField(_('filter 2 upper limit'), max_digits=17, decimal_places=9, blank=True, null=True, db_index=True)
    tags = models.CharField(_('tags'), max_length=255, blank=True, db_index=True,
        help_text=_('Comma separated list of tags to be more specific than category'))

    class Meta:
        ordering = ('battery', 'id')
        verbose_name = _('battery\'s category usage')
        verbose_name_plural = _('battery\'s categories usage')

    def __unicode__(self):
        return _('{count} exercises from {category}').format(
            count=self.exercises_count,
            category=self.category
        )

    def get_tags(self):
        return [t.strip() for t in self.tags.split(',')]

    def get_clauses(self):
        """
        Returns a list of clauses to select exercises.

        The clauses includes the upper limits, lower limits and all tags joined
        through and AND operator.
        """
        clauses = []
        if self.filter1_lower is not None and self.filter1_upper is not None:
            if self.filter1_lower == self.filter1_upper:
                clauses.append(models.Q(filter1=self.filter1_lower))
            else:
                clauses.append(models.Q(filter1__gte=self.filter1_lower))
                clauses.append(models.Q(filter1__lte=self.filter1_upper))
        if self.filter2_lower is not None and self.filter2_upper is not None:
            if self.filter2_lower == self.filter2_upper:
                clauses.append(models.Q(filter2=self.filter2_lower))
            else:
                clauses.append(models.Q(filter2__gte=self.filter2_lower))
                clauses.append(models.Q(filter2__lte=self.filter2_upper))
        if self.tags:
            for tag in self.get_tags():
                clauses.append(models.Q(tags__contains=tag))
        if clauses:
            return reduce(lambda a, b: a & b, clauses)
        else:
            return None


def cache_matters_and_subjects_names(sender, instance, **kwargs):
    battery = instance.battery

    categories = battery.categories.all()
    battery.categories_names = ', '.join([c.name for c in categories])

    matters = Matter.objects.filter(category__in=categories).distinct()
    battery.matters_names = ', '.join([m.name for m in matters])

    subjects = Subject.objects.filter(category__in=categories).distinct()
    battery.subjects_names = ', '.join([s.name for s in subjects])

    battery.save()
models.signals.post_save.connect(cache_matters_and_subjects_names, sender=CategoryUsage)


class ProgramUsage(models.Model):
    """
    A program usage is the application of a program for the users of a client.
    """
    klass = models.OneToOneField(Klass, verbose_name=_('class'), related_name='program_usage')
    program = models.ForeignKey(Program, verbose_name=_('exercises program'))
    start_date = models.DateField(_('start date'), default=datetime.datetime.today)
    end_date = models.DateField(_('end date'), help_text=_('E.g.: the end of school year.'))

    # denormalization:
    client = models.ForeignKey(Client, verbose_name=_('client'), editable=False)
    contract = models.ForeignKey(Contract, verbose_name=_('contract'), editable=False)

    class Meta:
        verbose_name = _('program usage')
        verbose_name_plural = _('program usages')

    def __unicode__(self):
        return _('%(program)s usage by %(client)s') % {'program': self.program, 'client': self.client}

    def get_excluded_dates(self, how_many, starting_at):
        """
        Gives a number of excluded dates starting at some date. If the program
        has 100 days, we get 100 excluded dates to be ignored during filling.
        """
        client = self.klass.contract.client
        teacher = self.klass.teacher.teacher_set.get(client=client)

        base_querysets = [
            SystemDate.objects.all(),
            client.clientdate_set.all(),
            teacher.teacherdate_set.all(),
        ]

        querysets = [qs.filter(date__gte=starting_at)[:how_many] for qs in base_querysets]

        dates = [set(qs.values_list('date', flat=True)) for qs in querysets]

        # symmetric different is a set method that returns items in A or B but
        # not in both. We are comparing 3 sets:
        #
        # - if the date appears once, it is excluded
        # - if appears twice, it is included by the client or teacher
        # - if appears three times, it is excluded by teacher
        return reduce(lambda a, b: a.symmetric_difference(b), dates)

    def distribute_batteries(self, modules_sequence=None):
        """
        Create a battery schedule for each battery in the choosen program
        modules.
        """
        one_day = datetime.timedelta(days=1)  # cache for reuse

        i = 0
        battery_date = self.start_date
        if isinstance(battery_date, datetime.datetime):
            battery_date = battery_date.date()
        excluded_dates = []

        modules = list(self.program.module_set.all())
        if modules_sequence:
            modules.sort(key=lambda module: modules_sequence.index(module.pk))
        batteries = []

        while 1:
            # get excluded dates on demand as needed
            if not excluded_dates:
                excluded_dates = self.get_excluded_dates(
                    how_many=self.program.batteries_count - i,
                    starting_at=battery_date
                )

            if battery_date in excluded_dates:
                excluded_dates.remove(battery_date)  # waste the date if excluded
            else:
                # get the next battery from the current module or get the next module
                # note that battery schedules aren't grouped by module, once a
                # class is started, it nevermind
                if batteries:
                    battery = batteries.pop(0)
                else:
                    if not modules:
                        break  # we ended the batteries and modules!
                    else:
                        module = modules.pop(0)
                        batteries = list(module.battery_set.all())
                        battery = batteries.pop(0)
                battery.batteryschedule_set.create(program_usage=self,
                                                   date=battery_date)

                i += 1  # update counter to know how many excluded dates to take
            battery_date = battery_date + one_day

            # Stops the battery creation when exhaust available dates
            if battery_date > self.end_date:
                break


def cache_program_usage_client(sender, instance, **kwargs):
    instance.contract = instance.klass.contract
    instance.client = instance.klass.contract.client
models.signals.pre_save.connect(cache_program_usage_client, sender=ProgramUsage)


class BatteryScheduleManager(models.Manager):
    def pending(self, ref=None):
        """
        Tells what are the next schedules for a klass based in the date.
        """
        if not ref:
            ref = timezone.now().date()
        return self.filter(date__gte=ref)

    def pending_for_user(self, user, ref=None):
        """
        Tells what is the schedules not done or not started for the given user.
        """
        qs =  self.pending(ref).filter(program_usage__klass__students=user)

        late_klasses = user.took_klasses.late_payment()
        qs = qs.exclude(program_usage__klass__in=late_klasses)

        qs = qs.extra(
            where=['select not count(is_done) from exercises_userbattery where ' \
                   'battery_schedule_id = exercises_batteryschedule.id and ' \
                   'user_id = %s and is_done = %s'],
            params=[user.pk, True],
        )
        return qs.distinct()


class BatterySchedule(models.Model):
    """
    The batteries must be done according to a predefined schedule. This
    schedule is defined here.
    """
    program_usage = models.ForeignKey(ProgramUsage, verbose_name=_('program usage'))
    battery = models.ForeignKey(Battery, verbose_name=_('battery'))
    date = models.DateField(_('date'))
    attempts = models.IntegerField(_('attempts count'), default=1,
            help_text=_('How many attempts the user will have for each exercise of this battery?'))
    objects = BatteryScheduleManager()

    class Meta:
        ordering = ('date',)
        verbose_name = _('battery schedule')
        verbose_name_plural = _('batteries schedule')

    def __unicode__(self):
        return unicode(self.battery)

    def is_past(self):
        return self.date <= timezone.now().date()


class UserBattery(models.Model):
    """
    A user battery is the application of a battery for some user. The user must
    be part of the client owner of the program (of the battery). The exercises
    will be the flat list of battery's categories exercises plus the manually
    selected ones. If the battery has more exercises than needed, they will be
    randomized.
    """
    user = models.ForeignKey(User, verbose_name=_('user'))
    battery_schedule = models.ForeignKey(BatterySchedule, verbose_name=_('battery schedule'), blank=True, null=True)
    exercises = models.ManyToManyField(Exercise, through='UserBatteryExercise', blank=True, verbose_name=_('exercises'))
    is_done = models.BooleanField(_('is done?'), default=False)

    # denormalization
    battery = models.ForeignKey(Battery, verbose_name=_('battery'), editable=False)

    correct_answers = models.IntegerField(_('correct answers count'), default=0)
    exercises_count = models.IntegerField(_('exercises count'), default=0)
    attempts_spent = models.DecimalField(_('attempts spent'), max_digits=6,
        decimal_places=5, default=0, help_text=_('Average attempts count.'))
    time_spent = models.IntegerField(_('time spent'), default=0,
        help_text=_('Sum of the overall time spent.'))

    class Meta:
        ordering = ('battery__position',)
        verbose_name = _('user battery')
        verbose_name_plural = _('user batteries')

    @property
    def attempts(self):
        return self.battery_schedule.attempts

    @property
    def score(self):
        return self.correct_answers / Decimal(self.exercises_count) * 10


def copy_battery_from_schedule(sender, instance, **kwargs):
    instance.battery = instance.battery_schedule.battery
models.signals.pre_save.connect(copy_battery_from_schedule, sender=UserBattery)


def fill_user_battery(sender, instance, **kwargs):
    """
    Copies the list of battery exercises to the user battery when created.

    Limits exercises of category with proper filter1, filter2 and tags
    configuration. Randomly sort them when needed and validates there is enough
    exercises (as planned in the battery).
    """
    if kwargs['created']:
        exercises = []
        for usage in instance.battery.categoryusage_set.all():
            qs = usage.category.exercise_set.all()
            clauses = usage.get_clauses()
            if clauses:
                qs = qs.filter(clauses)
            if usage.random_sorting:
                qs = qs.order_by('?')
            usage_exercises = qs[:usage.exercises_count]
            if len(usage_exercises) == usage.exercises_count:
                exercises.extend(usage_exercises)
            else:
                # Avoid a user do a battery with less than the exercises count
                # planned
                error = 'There is not {expected} exercises for the ' \
                        'category `{category}` with conditions ' \
                        '{conditions}. Found {found}.'
                raise ValueError(error.format(expected=usage.exercises_count,
                                              found=len(usage_exercises),
                                              category=usage.category,
                                              conditions=clauses))

        bulk = []
        for n, exercise in enumerate(exercises):
            bulk.append(UserBatteryExercise(user_battery=instance,
                                            exercise=exercise,
                                            position=n+1))
        UserBatteryExercise.objects.bulk_create(bulk)

        # denormalize the exercises count: make it after th bulk creation,
        # even if we know the number of exercises in the category usages,
        # we can't assert there is enough execises as planned
        instance.exercises_count = len(bulk)
        instance.save()
models.signals.post_save.connect(fill_user_battery, sender=UserBattery)


class UserBatteryExerciseManager(models.Manager):
    def correct(self):
        return self.filter(is_correct=True)

    def next(self, ref=None):
        """
        Gets the next exercise on the user battery. Get it as the first with a
        attempts available after the current one or the first from the list
        before it.
        """
        qs = self.all().filter(
            user_battery__battery_schedule__attempts__gt=models.F('attempts_spent')
        )
        if not ref:
            return qs[0]

        try:
            forward = qs.filter(position__gt=ref.position)
            return forward[0]
        except IndexError:
            try:
                backward = qs.filter(position__lt=ref.position)
                return backward[0]
            except IndexError:
                return None


class UserBatteryExercise(models.Model):
    """
    Intermediate table for the exercises many to many on the user battery. Adds
    a position field to let set a custom ordering for each user.
    """
    user_battery = models.ForeignKey(UserBattery, verbose_name=_('user battery'))
    exercise = models.ForeignKey(Exercise, verbose_name=_('exercise'))
    position = models.PositiveSmallIntegerField(_('position'))

    # fields denormalized from the attempts/chances
    is_correct = models.NullBooleanField(_('is correct?'), blank=True, null=True)
    attempts_spent = models.IntegerField(_('attempts left'), default=0)
    time_spent = models.IntegerField(_('time spent'), default=0)

    objects = UserBatteryExerciseManager()

    class Meta:
        ordering = ('position',)
        unique_together = ('user_battery', 'position')

    def next(self):
        return self.user_battery.userbatteryexercise_set.next(ref=self)


def denormalize_exercise_results(sender, instance, **kwargs):
    """
    When a user battery exercise is saved, updates the user battery to cache
    score, time spent and attempts.
    """
    user_battery = instance.user_battery
    qs = user_battery.userbatteryexercise_set.all()

    # done exercises is_correct or not. Not done ones don't know their state
    qs = qs.extra(select={'done': "SUM(is_correct IS NOT NULL)"})

    aggr = qs.aggregate(
        correct=models.Sum('is_correct'),
        attempts=models.Sum('attempts_spent'),
        time=models.Sum('time_spent'),
    )

    user_battery.correct_answers = int(aggr['correct'])
    user_battery.attempts_spent = int(aggr['attempts']) / Decimal(int(qs[0].done))
    user_battery.time_spent = int(aggr['time'])
    user_battery.save()
models.signals.post_save.connect(denormalize_exercise_results, sender=UserBatteryExercise)


class ChanceManager(models.Manager):
    def finished(self):
        return self.exclude(finished_at=None)

    def unfinished(self):
        return self.filter(finished_at=None)


class Chance(models.Model):
    """
    A chance is the application of an exercise on a user battery. It can be a
    standalone chance for testing purpouses.
    """
    user_battery_exercise = models.ForeignKey(UserBatteryExercise,
        verbose_name=_('user battery'), blank=True, null=True)
    number = models.IntegerField(_('number'), default=1)

    started_at = models.DateTimeField(_('started at'), default=timezone.now)
    finished_at = models.DateTimeField(_('finished at'), blank=True, null=True)

    # denormalization
    exercise = models.ForeignKey(Exercise, verbose_name=_('exercise'))
    user_battery = models.ForeignKey(UserBattery, verbose_name=_('user battery'),
        blank=True, null=True)

    objects = ChanceManager()

    class Meta:
        verbose_name = _('chance')
        verbose_name_plural = _('chances')
        unique_together = ('user_battery_exercise', 'number')

    @models.permalink
    def get_absolute_url(self):
        return ('student:chance-detail', (), {'user_battery': self.user_battery.pk,
                                              'position': self.user_battery_exercise.position,
                                              'number': self.number})

    @cached_property
    def answers(self):
        return self.chanceitem_set.as_dict()

    @property
    def attempts(self):
        """ Tells the attempts limit. """
        return self.user_battery.attempts

    @property
    def attempts_left(self):
        return self.attempts - self.user_battery_exercise.attempts_spent

    @property
    def time_spent(self):
        delta = self.finished_at - self.started_at
        return delta.seconds

    def is_finished(self):
        return self.finished_at is not None

    def is_correct(self):
        """ Tells if the chance is correct if all his parts are correct. """
        # TODO this is a bottleneck, use a better approach
        for item in self.chanceitem_set.all():
            if not item.is_correct():
                return False
        return True


def cache_exercise_and_user_battery(sender, instance, **kwargs):
    """
    When the user_battery_exercise is set, we must denormalize the related
    fields, otherwise, it may be a sample chance attached directly to an
    exercise, we don't need to bother with.
    """
    if instance.user_battery_exercise:
        instance.exercise = instance.user_battery_exercise.exercise
        instance.user_battery = instance.user_battery_exercise.user_battery
models.signals.pre_save.connect(cache_exercise_and_user_battery, sender=Chance)


def denormalize_chance_results(sender, instance, **kwargs):
    """
    Every time a chance is saved, count how many attempts where took, if the
    exercise is correct or not and how many time was spent and save it in the
    user exercise instance.

    This will be useful to tell the next exercise with available attempts.
    """
    user_exercise = instance.user_battery_exercise

    # ignore standalone chances (done through admin panel)
    if user_exercise is None:
        return

    attempts = list(user_exercise.chance_set.finished())
    if attempts:
        user_exercise.attempts_spent = len(attempts)
        user_exercise.is_correct = any([x.is_correct() for x in attempts])
        user_exercise.time_spent = sum([x.time_spent for x in attempts])
        user_exercise.save()
models.signals.post_save.connect(denormalize_chance_results, sender=Chance)


class ChanceItemManager(models.Manager):
    def as_dict(self):
        return MultiDict(self.all(), group_callback=lambda c: c.answer.group)


class ChanceItem(models.Model):
    chance = models.ForeignKey(Chance, verbose_name=_('chance'))
    answer = models.ForeignKey(Answer, verbose_name=_('answer'))
    value = models.DecimalField(_('value'), max_digits=17, decimal_places=9,
        blank=True, null=True)
    choices = models.ManyToManyField(Choice, verbose_name=_('choices'), blank=True, null=True)
    objects = ChanceItemManager()

    def has_choices(self):
        """ Tells when a chance item uses the choices to store the answer data. """
        return self.answer.type in ('radio', 'checkbox')

    def is_correct(self):
        if self.answer.type == 'boolean':
            # boolean answers are 0 for false and are 1 for true values, this
            # way, we can just compare the bool version of the values.
            return bool(self.value) == bool(self.answer.value)
        elif self.has_choices():
            # choiced answers must have the answer and the user data equal for
            # both the single choice and multiple choices
            answer_choices = set([x.id for x in self.answer.choice_set.correct()])
            chance_choices = set([x.id for x in self.choices.all()])
            return answer_choices == chance_choices
        else:
            if (self.answer.type.endswith('or_blank') and not self.answer.value
                    and not self.value):
                return True  # the value can be any false value (0, '', None)
            return self.value == self.answer.value

    @property
    def correct_value(self):
        value = self.answer.value
        if value is None:
            return ''
        elif not value and self.answer.type.endswith('or_blank'):
            return ''
        elif self.answer.type == 'boolean':
            return bool(value)
        elif self.answer.type.startswith('digit'):
            return floatformat(value, 0)  # avoid return 1.0
        else:
            return value

    class Meta:
        verbose_name = _('chance item')
        verbose_name_plural = _('chance items')
