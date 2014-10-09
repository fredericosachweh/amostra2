# -*- encoding: utf-8 -*-
from django.utils import timezone

from clients import factories
from exercises.models import Program
from utils.tests import BaseTestCase


class ProgramTestMixin(object):
    """
    Offer method to start a program through factories. Needs categories and
    sample exercises.
    """
    def start_program(self, start_date=None):
        self.manager = factories.UserFactory.create(email='manager@email.com')
        self.client = factories.ClientFactory.create(managers=[self.manager])
        self.contract = factories.ContractFactory.create(client=self.client)

        teacher = factories.TeacherFactory.create(email='teacher@email.com',
                                                  client=self.client)
        self.teacher = teacher.teacher

        self.klass = factories.KlassFactory.create(contract=self.contract,
                                                   teacher=self.teacher)

        emails = ['student{0}@email.com'.format(i + 1) for i in range(3)]
        self.students = [factories.UserFactory.create(email=e) for e in emails]
        self.klass.students = self.students

        # pick a program got from the fixtures
        program = Program.objects.all()[0]
        if not start_date:
            start_date = timezone.now()
        program_usage = program.programusage_set.create(klass=self.klass,
                                                        start_date=start_date,
                                                        end_date=self.klass.end_date)
        program_usage.distribute_batteries()

        # The klass must have the passwords printed to be used
        self.klass.password_list_printed_at = timezone.now()
        self.klass.save()


class BaseStudentTestCase(ProgramTestMixin, BaseTestCase):
    """
    Base class for tests with student interaction.
    """
    fixtures = BaseTestCase.fixtures + [
        'auth_groups.json',
        'exercises_categories.json',
        'exercises_programs.json',
        'exercises_sample.json',
    ]

    def login_to_klass(self, student):
        """
        Given a user instance, login it into the class login url.
        """
        self.browser.visit(self.live_server_url)
        self.browser.fill('klass', self.klass.key)
        self.browser.find_by_xpath('//button[text()="Continuar"]').first.click()
        self.assertTrue(self.browser.is_text_present(u'Acesse seus exercícios'))

        self.browser.choose('username', student.username)
        self.assertTrue(self.browser.is_text_present('Digite sua senha'))

        self.browser.fill('password', '123456')
        self.browser.find_by_xpath('//button[text()="Enviar"]').first.click()
