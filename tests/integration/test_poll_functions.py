"""
Tests a realistic, configured Poll to make sure that everything works as it
should.
"""
from selenium.common.exceptions import NoSuchElementException
import time
from .base_test import PollBaseTest


class TestPollFunctions(PollBaseTest):
    def test_first_load(self):
        """
        Checks first load.

        Verify that the poll loads with the expected choices, that feedback is
        not showing, and that the submit button is disabled.
        """
        self.go_to_page('Poll Functions')
        answer_elements = self.browser.find_elements_by_css_selector('label.poll-answer')
        answers = [element.text for element in answer_elements]
        self.assertEqual(['A very long time', 'Not very long', 'I shall not say', 'Longer than you'], answers)

        self.assertRaises(NoSuchElementException, self.browser.find_element_by_css_selector, '.poll-feedback')

        submit_button = self.get_submit()
        self.assertFalse(submit_button.is_enabled())

    def test_submit_enabled(self):
        """
        Makes sure the submit button is enabled when selecting an answer.
        """
        self.go_to_page('Poll Functions')
        answer_elements = self.browser.find_elements_by_css_selector('label.poll-answer')
        answer_elements[0].click()

        # When an answer is selected, make sure submit is enabled.
        self.wait_until_exists('input[name=poll-submit]:enabled')

    def test_poll_submission(self):
        """
        Verify that the user can submit his or her vote and that the vote counts.

        Also check that feedback is displayed afterward.
        """
        self.go_to_page('Poll Functions')
        answer_elements = self.browser.find_elements_by_css_selector('label.poll-answer')

        # 'Not very long'
        answer_elements[1].click()

        self.get_submit().click()

        # Not a good way to wait here, since all the elements we care about
        # tracking don't exist yet.
        time.sleep(1)

        self.assertTrue(self.browser.find_element_by_css_selector('.poll-feedback').text,
                        "Thank you\nfor being a valued student.")

        self.assertEqual(self.browser.find_element_by_css_selector('.poll-footnote').text,
                         'Results gathered from 100 respondent(s).')

        self.assertFalse(self.browser.find_element_by_css_selector('input[name=poll-submit]').is_enabled())

    def test_submit_not_enabled_on_revisit(self):
        """
        Verify that revisiting the page post-vote does not re-enable the submit button.
        """
        self.go_to_page('Poll Functions')

        answer_elements = self.browser.find_elements_by_css_selector('label.poll-answer')

        # Not very long
        answer_elements[1].click()

        self.get_submit().click()

        # Button will be reaplaced with a new disabled copy, not just disabled.
        self.wait_until_exists('input[name=poll-submit]:disabled')

        self.go_to_page('Poll Functions')
        self.assertFalse(self.get_submit().is_enabled())