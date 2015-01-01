"""
Tests to verify a default poll XBlock is a functional demo.

Deeper investigation should be tested in test_poll_functions.
"""
from selenium.common.exceptions import NoSuchElementException
from .base_test import PollBaseTest


class TestDefault(PollBaseTest):
    """
    Tests to run against the default XBlock configurations.
    """
    def test_default_poll(self):
        """
        Verifies that a default poll loads, that it can be voted on, and that
        the tally displays afterward. Verifies that the feedback section does
        not load since it is not enabled by default.
        """
        self.go_to_page('Poll Defaults')
        button = self.browser.find_element_by_css_selector('input[type=radio]')
        button.click()
        submit = self.get_submit()
        submit.click()

        self.wait_until_exists('.poll-percent-display')

        # Should now be on the results page.
        self.assertEqual(self.browser.find_element_by_css_selector('.poll-percent-display').text, '100%')

        # No feedback section.
        self.assertRaises(NoSuchElementException, self.browser.find_element_by_css_selector, '.poll-feedback')

    def test_default_survey(self):
        """
        Verifies that a default survey loads, that it can be voted on, and
        that the tally displays afterward. Verifies that the feedback section
        does not load since it is not enabled by default.
        """
        self.go_to_page('Survey Defaults')
