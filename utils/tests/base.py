from django.conf import settings
from django.test import LiveServerTestCase
from django.utils.dateformat import format
from django.utils import translation
from splinter.browser import Browser

from clients import factories


class BaseTestCase(LiveServerTestCase):
    fixtures = [
        'auth_groups.json',
    ]

    @classmethod
    def setUpClass(cls):
        translation.activate('pt-br')
        cls.browser = Browser(settings.SPLINTER_TEST_DRIVER)
        super(BaseTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        translation.deactivate()
        super(BaseTestCase, cls).tearDownClass()

    def setUp(self):
        self.auth_user = self.manager = factories.UserFactory.create(username='gestor', password='123456')
        self.client = factories.ClientFactory.create(managers=[self.manager])

    def do_login(self):
        """
        Opens the login form section (that is hidden by default) and do login.
        """
        self.browser.visit(self.live_server_url + '/')
        container = self.browser.find_by_css('#login section + section').first
        container.find_by_css('.title a').first.click()
        container.find_by_css('[name=username]').fill(self.auth_user.email)
        container.find_by_css('[name=password]').fill('123456')
        container.find_by_css('button[type=submit]').first.click()

    def select_date(self, name, date):
        # the container is a datepicker div after the named input
        selector = 'input[name="{0}"] + .datepicker'.format(name)
        container = self.browser.find_by_css(selector).first

        # navigate to month in the datepicker
        month_name = format(date, 'M')
        while 1:
            name = container.find_by_css('.months .name').first
            if name.text == month_name:
                break
            container.find_by_css('.months .next').first.click()

        # click the end date
        date_str = format(date, 'Y-m-d')
        date_widget = container.find_by_css('td[date="{0}"]'.format(date_str))
        date_widget.first.click()
