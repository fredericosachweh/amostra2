# -*- encoding: utf-8 -*-
from lettuce import world, step


@step(ur'clic(?:o|ar) no link "([^"]*)"')
def click_link_by_name(step, name):
    """
    Clicks a link in the browser finding him by the specified text.
    """
    world.browser.click_link_by_text(name)


@step(ur'clic(?:o|ar) no botão "([^"]*)"')
def click_button_by_name(step, name):
    """
    Clicks a button in the browser finding him by the specified text.
    """
    xpath_query = '//button[text()="{0}"]'.format(name)
    world.browser.find_by_xpath(xpath_query).first.click()


@step(ur'clic(?:o|ar) em #[^ ]+')
def click_element_by_id(step, elem_id):
    """
    Clicks an element in the browser finding him by his ID.
    """
    world.browser.find_by_css('#' + elem_id).first.click()


@step(ur'estarei na página "([^"]*)"')
def check_page_by_text(step, text):
    """
    Asserts that the we are in a page with a text present in it.
    """
    assert world.browser.is_text_present(text)


@step(u'clic(?:o|ar) no checkbox "([^"]*)"')
def click_checkbox(step, text):
    """
    Clicks a label corresponding the an specified text, to activate a checkbox.
    """
    xpath = '//label[contains(normalize-space(.), "{0}")]'.format(text)
    world.browser.find_by_xpath(xpath).first.click()


@step(u'hoje for dia (\d{2})/(\d{2})/(\d{4})')
def set_predefined_date(step, *date_tuple):
    """
    Stores a date tuple to be used in a mock.patch call in further steps.
    """
    world.date_tuple = [int(d) for d in date_tuple[::-1]]  # reversed integers
