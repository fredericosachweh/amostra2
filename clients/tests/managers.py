# -*- encoding: utf-8 -*-
import datetime

from django.contrib.auth.models import User

from clients import factories
from clients import models
from utils.tests import BaseTestCase


class ManagerTestCase(BaseTestCase):
    # emails for teacher creating tests
    new_user_email = 'new@email.com.br'
    existing_user_email = 'existing@email.com.br'

    def test_login(self):
        """
        Tests that when login as manager user, get redirected to the proper url.
        """
        self.do_login()
        self.assertEqual(self.browser.url, self.live_server_url + '/contratos/')

    def open_teacher_create_form(self, do_login=True):
        """
        Opens the modal for adding a new teacher instance.
        """
        if do_login:
            self.do_login()

        self.browser.visit(self.live_server_url + '/contratos/professores/')

        # opens the lightbox to add a new teacher
        self.browser.click_link_by_partial_text('Adicionar professor')
        self.assertTrue(self.browser.is_text_present('Novo professor'))
        return self.browser.find_by_css('.reveal-modal').first

    def test_create_new_teacher(self, do_login=True):
        """
        Creates a new teacher with an unexistant user email.
        """
        # ensure, the user doesn't exist yet
        self.assertEqual(User.objects.filter(email=self.new_user_email).count(), 0)

        # send the lightbox's form
        modal = self.open_teacher_create_form(do_login)
        modal.find_by_name('name').fill('User')
        modal.find_by_name('email').fill(self.new_user_email)
        modal.find_by_tag('button').click()

        # the teacher should be available now...
        self.assertTrue(self.browser.is_text_present(self.new_user_email))
        teacher = models.User.objects.get(email=self.new_user_email)
        self.assertEqual(teacher.involved_to_clients.count(), 1)

        # as we have 1 client, the edit button don't need to be available
        self.assertTrue(self.browser.is_text_not_present('Editar'))

        # TODO test the teacher got an email with his password

        return teacher

    def test_create_teacher_for_existing_user(self):
        """
        Creates a new teacher with an already existing user email.
        """
        existing_user = factories.UserFactory.create(email=self.existing_user_email)

        # the user aren't related to any client
        self.assertEqual(existing_user.involved_to_clients.count(), 0)

        modal = self.open_teacher_create_form()
        modal.find_by_name('name').fill('User')
        modal.find_by_name('email').fill(self.existing_user_email)
        modal.find_by_tag('button').click()

        # the user is the same but now it has a client attached to
        self.assertTrue(self.browser.is_text_present(self.existing_user_email))
        self.assertEqual(existing_user.involved_to_clients.count(), 1)

    def test_remove_teacher(self):
        """
        Removing the teacher, in fact, removes the link between the teacher
        user and client but keeps the user instance.
        """
        # opens the confirmation lightbox
        teacher = self.test_create_new_teacher()
        self.browser.click_link_by_partial_text('Remover')

        self.assertTrue(self.browser.is_text_present('deseja remover o professor ' + teacher.get_full_name()))
        self.browser.find_by_name('teacher-remove').first.click()

        # check if the user is still here and is not related
        # to the client anymore
        self.assertTrue(self.browser.is_text_not_present(teacher.email))
        self.assertEqual(User.objects.filter(pk=teacher.pk).count(), 1)
        self.assertEqual(teacher.involved_to_clients.filter(pk=self.client.pk).count(), 0)

    def test_create_new_teacher_with_two_clients(self):
        """
        Creates a new teacher when there is more than one client to choose.
        """
        another_client = factories.ClientFactory.create(managers=[self.manager])

        # send the lightbox's form
        modal = self.open_teacher_create_form()
        modal.find_by_name('name').fill('User')
        modal.find_by_name('email').fill(self.new_user_email)
        modal.find_by_css('input[name=clients]')[1].check()
        modal.find_by_tag('button').click()

        # the teacher should be available now...
        self.assertTrue(self.browser.is_text_present(self.new_user_email))
        teacher = models.User.objects.get(email=self.new_user_email)
        teacher_clients = list(teacher.involved_to_clients.all())
        self.assertEqual(len(teacher_clients), 1)
        self.assertTrue(another_client in teacher_clients)
        self.assertTrue(self.client not in teacher_clients)

        # as we have 2 clients, the edit button must be available
        # TODO don't know why but splinter is lowering the text case, I was waiting for an Editar label
        self.assertTrue(self.browser.is_text_present('editar'))

        # TODO reload the teachers list and make sure the edit button is
        # available even when comming outside ajax

    def test_create_klass(self):
        """
        Tests the creation of a class without teacher.
        """
        contract = factories.ContractFactory.create(client=self.client)

        self.do_login()

        # create a class with no teacher
        self.browser.find_link_by_text('Ações')[1].click()  # the first button is in top menu
        self.browser.click_link_by_text('Adicionar turma')

        self.browser.is_text_present('Nova turma')
        self.browser.fill('name', 'Sample Class')

        # select an end_date in datepicker (the end of the year)
        today = datetime.date.today()
        end_date = datetime.date(today.year, 12, 23)
        self.select_date('end_date', end_date)

        # saves
        self.browser.find_by_name('klass-create').first.click()

        self.assertTrue(self.browser.is_text_present('Sample Class'))
        self.assertTrue(self.browser.is_text_present('sem professor'))

    def test_update_klass(self):
        """
        Test the update of a class by adding a teacher to it.
        """
        self.test_create_klass()
        self.test_create_new_teacher(do_login=False)

        self.browser.visit(self.live_server_url + '/')
        self.browser.click_link_by_partial_text('Ver turmas')  # open the accordion

        self.assertTrue(self.browser.is_text_present('Sample Class'))
        self.browser.click_link_by_text('Editar')

        self.assertTrue(self.browser.is_text_present('Alterar turma'))
        user = User.objects.get(email=self.new_user_email)
        self.browser.select('teacher', user.pk)
        self.browser.find_by_name('klass-create').first.click()

        self.assertTrue(self.browser.is_text_present('User'))

        # TODO assert the teacher receives an email telling his is owner of
        # class

    def test_remove_klass(self):
        self.test_create_klass()

        # we don't need to open the klass accordion once it must be opened
        # after create a klass
        self.browser.click_link_by_text('Remover')

        self.assertTrue(self.browser.is_text_present('Remover turma'))
        self.browser.find_by_xpath('//button[text()="Sim"]').first.click()

        # the class should be removed from DOM
        self.assertTrue(self.browser.is_text_not_present('Sample Class'))
