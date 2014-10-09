import datetime

from django.utils import timezone

from base import BaseStudentTestCase
from exercises import models
from utils.templatetags.utils_extras import format_minutes


class StudentTestCase(BaseStudentTestCase):
    def setUp(self):
        self.start_date = timezone.now() - datetime.timedelta(days=7)
        self.start_program(self.start_date)

    def get_pending_schedules(self, student):
        return models.BatterySchedule.objects.pending_for_user(student,
                                                               ref=self.start_date)

    def fill_battery(self, student, schedule):
        user_battery = schedule.userbattery_set.create(user=student)
        day_errors = 0
        time_spent = 0
        for user_exercise in user_battery.userbatteryexercise_set.all():
            chance = user_exercise.chance_set.create(number=1)
            for answer in chance.exercise.answer_set.all():
                if day_errors < self.errors:
                    value = None
                else:
                    value = answer.value
                chance.chanceitem_set.create(answer=answer,
                                             value=value)
            chance.finished_at = chance.started_at + datetime.timedelta(seconds=150)
            chance.save()
            day_errors += 1
            time_spent += 150

            user_exercise.is_done = True
            user_exercise.save()

        # we don't know how many exercises exists in the day/battery, so we
        # aggregate it and return for further usage
        return time_spent

    def test_analytics(self):
        """
        Make 3 interactions from students (as self.students has 3 users) and
        check the analytics.
        """
        self.errors = 0
        times = []
        for student in self.students:
            user_times = []
            for schedule in self.get_pending_schedules(student):
                user_times.append(self.fill_battery(student, schedule))

            # discover the avg time per day and format it to compare further
            time = sum(user_times) / float(len(user_times))
            times.append(format_minutes(time))
            self.errors += 1

        # login as teacher
        self.auth_user = self.teacher
        self.do_login()

        # go to the klass details
        self.assertTrue(self.browser.is_text_present('Programas e turmas'))
        self.browser.click_link_by_text('Detalhar')
        self.assertTrue(self.browser.is_text_present('Sample Class'))

        # we know what score we are expecting due or error rate
        scores = [
            ['first_name2 last_name2', '10'],
            ['first_name3 last_name3', '9,66'],
            ['first_name4 last_name4', '9,33']
        ]

        # check each row are present in the klass analytics
        rows = self.browser.find_by_css('.module tbody tr')
        for row, (name, score), time in zip(rows, scores, times):
            cols = row.find_by_css('td')
            self.assertEqual(cols[1].text, name)
            self.assertEqual(cols[3].text, score)
            self.assertEqual(cols[4].text, time)
