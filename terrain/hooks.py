# -*- encoding: utf-8 -*-
from django.conf import settings
from django.core.management import call_command
from django.core.urlresolvers import reverse
from lettuce import before, after, world
from splinter.browser import Browser

from nose.tools import assert_true


@before.harvest
def prepare_harvest(context):
    server = context['server']

    # Absorbed functions that relies in the django_url/server.url are not
    # working in the terrain file, so we define the absorbed functions in the
    # pre-harvest, when the server is already defined
    @world.absorb
    def do_login(username, password):
        """
        Reusable login mechanism.

        Opens the home page, changes to the second login form tab for
        credentials login (the first tab has login by klass key), fills in the
        given credentials and procede.
        """
        world.browser.visit(server.url(reverse('home')))

        # Opens the second section with the login by credentials tab
        container = world.browser.find_by_css('#login section + section').first
        container.find_by_css('.title a').first.click()

        container.find_by_name('username').fill(username)
        container.find_by_name('password').fill(password)
        container.find_by_css('button[type=submit]').first.click()

    @world.absorb
    def do_login_as_student(klass_key, password):
        world.browser.visit(server.url(reverse('home')))

        container = world.browser.find_by_css('#login section').first
        container.find_by_name('klass').fill(klass_key)
        container.find_by_css('button[type=submit]').first.click()

        assert_true(world.browser.is_text_present(u'Clique no seu nome'))

        world.browser.find_by_name('username').first.click()
        assert_true(world.browser.is_text_present(u'Olá'))
        world.browser.find_by_name('password').fill(password)
        world.browser.find_by_css('button[type=submit]').first.click()

@before.runserver
def initial_setup(server):
    world.browser = Browser(settings.SPLINTER_TEST_DRIVER)
    if settings.SPLINTER_TEST_DRIVER == 'phantomjs':
        world.browser.driver.set_window_size(800, 600)

@before.each_scenario
def reset_data(scenario):
    call_command('flush', interactive=False, verbosity=0)
    call_command('loaddata', 'auth_groups.json', verbosity=0)

@after.all
def teardown_browser(total):
    world.browser.quit()
