import optparse
import random

from django.core.management import base
from django.db import transaction
from exercises import models


class BaseCommand(base.BaseCommand):
    matter = None
    subject = None
    category = None
    bulk_create_answers = True

    option_list = base.BaseCommand.option_list + (
        optparse.make_option('--dummy',
            action='store_true', dest='dummy', default=False,
            help='Dummy operation?'),
        optparse.make_option('--operation',
            action='store', type='string', dest='operation', default='',
            help='Numbers to create the operation (e.g. 315+92)'),
        optparse.make_option('--limit',
            action='store', type='int', dest='limit',
            help='Generate exercises until what number?'),
        optparse.make_option('--randomize',
            action='store', type='int', dest='randomize', default=None,
            help='Randomize at each group of specified exercises to avoid stress the generation'),
        optparse.make_option('--just-count',
            action='store_true', dest='just_count',
            help='Flag to just count the exercises that will be generated for such limit'),
    )

    def get_matter_slug(self):
        if self.matter:
            return self.matter
        else:
            raise NotImplementedError

    def get_subject_slug(self):
        if self.subject:
            return self.subject
        else:
            raise NotImplementedError

    def get_category_slug(self):
        if self.category:
            return self.category
        else:
            raise NotImplementedError

    def split_terms(self, operation):
        """
        Given an operation textual description, extract the terms that will be
        converted in the exercise. E.g. 25+39 will generate the terms 25 and 39.
        """
        raise NotImplementedError

    def save_questions(self):
        models.Question.objects.bulk_create(self.questions)
        del self.questions[:]

    def save_answers(self):
        """
        Do not bulk create answers the post_save signal is needed to some
        exercise complement (like convertion of choices_map onto choices
        instances).

        Defaults to True.
        """
        if self.bulk_create_answers:
            models.Answer.objects.bulk_create(self.answers)
        else:
            for answer in self.answers:
                answer.save()
        del self.answers[:]

    def handle(self, dummy, operation, limit, verbosity, *args, **options):
        self.dummy = dummy
        self.limit = limit
        self.randomize_at = options.get('randomize')
        self.verbosity = int(verbosity)

        if options.get('just_count'):
            print 'It will be generated {0} exercises'.format(
                    len(list(self.generate_operations())))
            return

        self.matter = models.Matter.objects.get(slug=self.get_matter_slug())
        self.subject = self.matter.subject_set.get(slug=self.get_subject_slug())
        self.category = self.subject.category_set.get(slug=self.get_category_slug())

        # instead of save each question and answer, store them to bulk create
        # in the last step. Exercises are created in the loop as they are
        # needed by questions and answers
        self.questions = []
        self.answers = []

        # create the exercise and bulk create stored questions and answers per
        # iteration to avoid memory flood
        if operation:
            if self.verbosity > 1:
                print 'Generating', operation, self.verbosity

            terms = self.split_terms(operation)
            self.create_exercise(*terms)
            self.save_questions()
            self.save_answers()
        else:

            self.counter = 0

            if self.verbosity > 1:
                print 'Generating several exercises'

            if self.randomize_at:
                randomized = random.randint(1, self.randomize_at)
            else:
                randomized = None
            for terms in self.generate_operations():
                if not self.randomize_at or randomized == self.counter:
                    with transaction.commit_manually():
                        try:
                            exercise = self.create_exercise(*terms)
                            self.save_questions()
                            self.save_answers()
                        except Exception:
                            transaction.rollback()
                            raise

                        if self.dummy:
                            transaction.rollback()
                        else:
                            transaction.commit()
                else:
                    exercise = None

                self.counter += 1
                if self.randomize_at and (self.counter % self.randomize_at == 0):
                    randomized = self.counter + random.randint(1, self.randomize_at)

                # calculate the conclusion rate and show it when change dozens
                if self.verbosity > 1:
                    if not self.counter % 100:
                        print '{0} exercises - {1}'.format(self.counter, exercise)
