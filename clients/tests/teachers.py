# -*- encoding: utf-8 -*-
import datetime

from clients import factories
from exercises.models import Program
from utils.tests import BaseTestCase


class TeacherTestCase(BaseTestCase):
    fixtures = BaseTestCase.fixtures + [
        'exercises_categories.json',
        'exercises_programs.json',
        'exercises_sample.json',
    ]

    def setUp(self):
        """
        Creates a client/contract and his manager, a teacher and his class and
        pre-select a program.
        """
        self.manager = factories.UserFactory.create(email='manager@email.com')
        self.client = factories.ClientFactory.create(managers=[self.manager])
        self.contract = factories.ContractFactory.create(client=self.client)

        teacher = factories.TeacherFactory.create(email='teacher@email.com',
                                                  client=self.client)
        self.auth_user = self.teacher = teacher.teacher  # use the user instance!

        self.klass = factories.KlassFactory.create(contract=self.contract,
                                                   teacher=self.teacher)

        # pick a program got from the fixtures
        self.program = Program.objects.latest('pk')

    def start_klass(self, students):
        self.do_login()
        self.browser.click_link_by_partial_text('Iniciar')

        # step 1 - select the dates
        start_date = datetime.date.today()
        self.select_date('start_date', start_date)
        self.browser.find_by_css('a[href="#programa"]').first.click()

        # step 2 - select a program
        self.browser.choose('program', str(self.program.pk))
        self.browser.find_by_css('a[href="#modulos"]').first.click()

        # step 3 - reorder modules
        self.browser.find_by_css('a[href="#alunos"]').first.click()

        # step 4 - fill students
        self.browser.fill('students', students)
        self.browser.find_by_xpath('//button[text()="Iniciar"]').first.click()

    def test_duplicated_names(self):
        """
        Tests that is not possible to add duplicated names for students in the
        same class.
        """
        students = '''
        Name 1
        Name 3
        Name 2
        Name 1
        '''
        self.start_klass(students)

        self.browser.find_by_css('.title a[href="#alunos"]').first.click()
        self.assertTrue(self.browser.is_text_present(u'Name 1 é usado mais de uma vez'))

    def test_students_limit(self):
        """
        Tests that the teacher cannot set more than the students limit of the
        class, defined in the max_students attribute, 50 by default.
        """
        limit = self.klass.max_students
        self.assertEqual(limit, 50)

        students = '\n'.join(['Name {0}'.format(n) for n in range(limit + 1)])
        self.start_klass(students)

        self.browser.find_by_css('.title a[href="#alunos"]').first.click()
        self.assertTrue(self.browser.is_text_present(u'não pode definir mais que {0} alunos'.format(limit)))

    def test_initialize_klass(self):
        """
        Tests the initialization of class by the logged in teacher.
        """
        # its ok to have blank lines and white space wrapping the names in the
        # students list: white spaces will be stripped out
        students = '''
        Bob Esponja
        Patrick Estrela

        Lula Molusco
        '''
        self.start_klass(students)

        self.assertTrue(self.browser.is_text_present(self.klass.name + ' foi inicializada'))

        # The blank line was ignored! We must have only 3 students
        self.assertEqual(self.klass.students.count(), 3)

        # until print passwords, user can't continue, the button would be hidden
        self.assertFalse(self.browser.find_by_css('#continue').first.visible)

        # even when goes to klass list and detail this klass, still can't do anything but print passwords
        current_url = self.live_server_url + '/turmas/{0}/iniciada/'.format(self.klass.pk)
        self.assertEqual(self.browser.url, current_url)
        self.browser.visit(self.live_server_url + '/')
        self.browser.click_link_by_partial_text('Detalhar')
        self.assertEqual(self.browser.url, current_url)

        # if the user close the window (clear the session) and don't print the
        # passwords, he will be redirect to a view to reschedule the class. 
        self.browser.cookies.delete()
        self.do_login()
        self.browser.click_link_by_partial_text('Detalhar')
        self.assertEqual(self.browser.url, self.live_server_url + '/turmas/{0}/reconfigurar/'.format(self.klass.pk))
