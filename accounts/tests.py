from django.test import TestCase
from clients.factories import ClientFactory
from factories import UserFactory
import models

from utils.tests import BaseTestCase


class UnitTestCase(TestCase):
    def test_user_account_maps_to_user(self):
        """
        Asserts that selecting a user account and getting the user through his
        property "user" returns the same user.
        """
        # first create a new user
        new_user = UserFactory.create(email='user@email.com', password='123456')

        # get it from a user account instance
        user_account = models.UserAccount.objects.get(email='user@email.com')
        user = user_account.user                # internally, just copy the
        self.assertEqual(user, new_user)        # user_account.__dict__


class IntegrationTestCase(BaseTestCase):
    def setUp(self):
        self.auth_user = UserFactory.create(email='user@email.com', password='123456')
        self.client = ClientFactory.create()

    def test_login_as_manager(self):
        """
        Tests that a user that becomes manager of any client will fall in the
        contract-list after login.
        """
        self.client.managers.add(self.auth_user)
        self.do_login()
        self.assertEqual(self.browser.url, self.live_server_url + '/contratos/')

    def test_login_as_teacher(self):
        """
        Tests that a user that becomes teacher of any client will fall in the
        klass-list after login.
        """
        self.client.teacher_set.create(teacher=self.auth_user)
        self.do_login()
        self.assertEqual(self.browser.url, self.live_server_url + '/turmas/')

    def test_login_hybrid(self):
        """
        Tests that a user that becomes teacher and manager of any client will
        fall in a desambiguation page to choose where to go.
        """
        self.client.managers.add(self.auth_user)
        self.client.teacher_set.create(teacher=self.auth_user)
        self.do_login()
        self.assertEqual(self.browser.url, self.live_server_url + '/escolha-perfil/')
