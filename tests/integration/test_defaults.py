"""
Tests to verify a default poll XBlock is a functional demo.

Deeper investigation should be tested in test_poll_functions.
"""
from selenium.common.exceptions import NoSuchElementException
from .base_test import PollBaseTest


class TestDefaults(PollBaseTest):
    def test_default_poll(self):
        """
        Verifies that a default poll loads, that it can be voted on, and that
        the tally displays afterward. Verifies that the feedback section does
        not load since it is not enabled by default.
        """
        self.go_to_page('Defaults')
        button = self.browser.find_element_by_css_selector('input[type=radio]')
        button.click()
        submit = self.browser.find_element_by_css_selector('input[name="poll-submit"]')
        submit.click()

        # Should now be on the results page.
        self.assertEqual(self.browser.find_element_by_css_selector('.poll-percent-display').text, '100%')

        # No feedback section.
        self.assertRaises(NoSuchElementException, self.browser.find_element_by_css_selector, '.poll-feedback')