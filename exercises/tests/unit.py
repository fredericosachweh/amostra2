from decimal import Decimal as D
import datetime

from django.test import TestCase
from django.utils import timezone

from base import ProgramTestMixin
from exercises import models, factories


class UnitTestCase(ProgramTestMixin, TestCase):
    """
    General exercises stuff test case.
    """
    fixtures = [
        'auth_groups.json',
        'exercises_categories.json',
        'exercises_programs.json',
        'exercises_sample.json',
    ]

    def test_choices_mapping(self):
        """
        Tests the conversion of a textual list of choices onto choice
        instances. The textual representation is given in the following syntax:

        + Choice 1
        - Choice 2
        + Choice 3
        - Choice 4

        The plus sign at the begging of a line indicates this choices is
        correct, the minus sign indicates it is incorrect.
        """
        category = factories.CategoryFactory.create()
        exercise = category.exercise_set.create(description='Sample exercise')
        choices = [
            {'is_correct': True, 'description': 'Choice 1'},
            {'is_correct': False, 'description': 'Choice 2'},
            {'is_correct': True, 'description': 'Choice 3'},
            {'is_correct': False, 'description': 'Choice 4'}
        ]
        choices_map = ''
        for choice in choices:
            if choice['is_correct']:
                choices_map += '+ '
            else:
                choices_map += '- '
            choices_map += choice['description'] + '\n'
        answer = exercise.answer_set.create(type='checkbox', choices_map=choices_map)
        for choice, choice_instance in zip(choices, answer.choice_set.all()):
            self.assertEqual(choice['description'], choice_instance.description)
            self.assertEqual(choice['is_correct'], choice_instance.is_correct)

        # check there is no duplications
        answer.save()
        self.assertEqual(answer.choice_set.count(), 4)

    def create_user_battery(self):
        start_date = timezone.now() - datetime.timedelta(days=7)
        self.start_program(start_date)
        student = self.students[0]
        qs = models.BatterySchedule.objects.pending_for_user(student,
                                                             ref=start_date)
        schedule = qs[0]
        user_battery = schedule.userbattery_set.create(user=student)
        return user_battery

    def try_exercise(self, exercise, number, correct, time):
        """
        Fill a chance with correct or incorrect values depending in the
        parameters.
        """
        chance = exercise.chance_set.create(number=number)
        for answer in chance.exercise.answer_set.all():
            if correct:
                value = answer.value
            else:
                value = None
            chance.chanceitem_set.create(answer=answer,
                                         value=value)
            chance.finished_at = chance.started_at + datetime.timedelta(seconds=time)
            chance.save()

    def check_user_battery(self, user_battery, correct, score, attempts, time):
        """
        Shortcuts to check user battery properties.
        """
        user_battery = models.UserBattery.objects.get(pk=user_battery.pk)
        self.assertEqual(user_battery.correct_answers, correct)
        self.assertAlmostEqual(user_battery.score, score, places=5)
        self.assertAlmostEqual(user_battery.attempts_spent, attempts, places=5)
        self.assertEqual(user_battery.time_spent, time)

    def check_exercise(self, exercise, is_correct, attempts, time):
        """
        Shortcuts to check user exercises properties.
        """
        exercise = models.UserBatteryExercise.objects.get(pk=exercise.pk)
        self.assertEqual(exercise.is_correct, is_correct)
        self.assertEqual(exercise.attempts_spent, attempts)
        self.assertEqual(exercise.time_spent, time)

    def test_sequence(self):
        """
        Check that the exercises follow a cyclic sequence inside an user battery.
        """
        user_battery = self.create_user_battery()
        user_exercises = list(user_battery.userbatteryexercise_set.all())

        first_exercise = user_exercises[0]
        second_exercise = user_exercises[1]
        self.assertEqual(first_exercise.position, 1)
        self.assertEqual(second_exercise.position, 2)
        self.assertEqual(first_exercise.next(), second_exercise)

        # We know there will be 10 exercises in the battery due the program
        # configuration
        last_exercise = user_exercises[-1]
        battery_exercises_count = user_battery.battery.exercises_count
        self.assertEqual(battery_exercises_count, 10)
        self.assertEqual(last_exercise.position, battery_exercises_count)
        self.assertEqual(last_exercise.next(), first_exercise)

    def test_score_denormalization(self):
        """
        Check the score and attempts number are properly denormalized when solving exercises.
        """
        user_battery = self.create_user_battery()

        # We know (from fixtures) there is 10 exercises for the first day and
        # all his analytics data is blank
        self.assertEqual(user_battery.exercises.count(), 10)
        self.assertEqual(user_battery.exercises_count, 10)  # denormalized!
        self.check_user_battery(user_battery, correct=0, score=0, attempts=0, time=0)

        user_exercises = user_battery.userbatteryexercise_set.all()

        # First chance in the first exercise
        first_exercise = user_exercises[0]
        self.try_exercise(first_exercise, number=1, correct=False, time=100)
        self.check_exercise(first_exercise, is_correct=False, attempts=1, time=100)
        self.check_user_battery(user_battery, correct=0, score=0, attempts=1, time=100)

        # Second chance in the first exercise
        self.try_exercise(first_exercise, number=2, correct=True, time=150)
        self.check_exercise(first_exercise, is_correct=True, attempts=2, time=250)
        self.check_user_battery(user_battery,
                                correct=1,
                                score=1/D(10) * 10,  # score from 0 to 10
                                attempts=2,
                                time=250)

        # First chance in the second exercise
        second_exercise = user_exercises[1]
        self.try_exercise(second_exercise, number=1, correct=True, time=100)
        self.check_exercise(second_exercise, is_correct=True, attempts=1, time=100)
        self.check_user_battery(user_battery,
                                correct=2,
                                score=2/D(10) * 10,  # score from 0 to 10
                                attempts=D('1.5'),
                                time=350)
