# -*- encoding: utf-8 -*-
from base import BaseStudentTestCase


class StudentTestCase(BaseStudentTestCase):
    def setUp(self):
        self.start_program()

    def test_jump_exercises(self):
        """
        Test a student can jump through exercises without solve them.
        """
        self.login_to_klass(self.students[0])

        # choose an exercise in the available list
        self.assertTrue(self.browser.is_text_present('Minhas tarefas'))
        self.browser.click_link_by_text('Iniciar')

        # start it in the initial page
        self.assertTrue(self.browser.is_text_present(u'Atenção'))
        self.browser.click_link_by_text('Iniciar')

        first_day = self.students[0].userbattery_set.all()[0]
        self.assertTrue(first_day.exercises.count(), 30)

        # start at first
        self.assertTrue(self.browser.is_text_present('1 de 30'))
        self.assertEqual(self.browser.url, self.live_server_url + '/tarefas/1/exercicio-1/')

        # jump to second
        self.browser.click_link_by_text('Pular')
        self.assertTrue(self.browser.is_text_present('2 de 30'))
        self.assertEqual(self.browser.url, self.live_server_url + '/tarefas/1/exercicio-2/')

        # manually go the the last
        self.browser.visit(self.live_server_url + '/tarefas/1/exercicio-30/')
        self.assertTrue(self.browser.is_text_present('30 de 30'))

        # and jump to the first
        self.browser.click_link_by_text('Pular')
        self.assertTrue(self.browser.is_text_present('1 de 30'))
        self.assertEqual(self.browser.url, self.live_server_url + '/tarefas/1/exercicio-1/')
