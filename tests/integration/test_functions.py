# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 McKinsey Academy
#
# Authors:
#          Jonathan Piacenti <jonathan@opencraft.com>
#
# This software's license gives you freedom; you can copy, convey,
# propagate, redistribute and/or modify this program under the terms of
# the GNU Affero General Public License (AGPL) as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version of the AGPL published by the FSF.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program in a file in the toplevel directory called
# "AGPLv3".  If not, see <http://www.gnu.org/licenses/>.
#
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

        self.assertFalse(self.browser.find_element_by_css_selector('.poll-feedback').is_displayed())

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

        self.wait_until_exists('.poll-footnote')

        self.assertTrue(self.browser.find_element_by_css_selector('.poll-feedback').text,
                        "Thank you\nfor being a valued student.")

        self.assertEqual(self.browser.find_element_by_css_selector('.poll-footnote').text,
                         'Results gathered from 100 respondents.')

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

        # Button will be replaced with a new disabled copy, not just disabled.
        self.wait_until_exists('input[name=poll-submit]:disabled')

        self.go_to_page('Poll Functions')
        self.assertFalse(self.get_submit().is_enabled())


class TestSurveyFunctions(PollBaseTest):

    @staticmethod
    def chunk_list(chunkable, max_size):
        """
        Subdivides a list into several smaller lists.
        """
        result = []
        in_list = False
        for index, item in enumerate(chunkable, start=1):
            if not in_list:
                result.append([])
                in_list = True
            result[-1].append(item)
            if not index % max_size:
                in_list = False
        return result

    def test_first_load(self):
        """
        Checks the first load of the survey.

        Verifies that the poll loads with the expected questions,
        that the answers are shown in the expected order, that feedback is
        not showing, and that the submit button is disabled.
        """
        self.go_to_page('Survey Functions')

        self.assertEqual(
            [element.text for element in self.browser.find_elements_by_css_selector('.survey-question')],
            [
                "I feel like this test will pass.", "I like testing software", "Testing is not necessary",
                "I would fake a test result to get software deployed."
            ]
        )
        self.assertEqual(
            [element.text for element in self.browser.find_elements_by_css_selector('.survey-answer')],
            [
                "Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"
            ]
        )

        self.assertFalse(self.browser.find_element_by_css_selector('.poll-feedback').is_displayed())

        submit_button = self.get_submit()
        self.assertFalse(submit_button.is_enabled())

    def fill_survey(self, assert_submit=False):
        """
        Fills out the survey. Optionally checks if the submit button is
        in the right state along the way.
        """
        elements = self.browser.find_elements_by_css_selector('.survey-option input[type=radio]')
        # Answers should be in sets of five.
        questions = self.chunk_list(elements, 5)

        # Disabled to start...
        submit_button = self.get_submit()
        if assert_submit:
            self.assertFalse(submit_button.is_enabled())

        # Strongly Agree: I feel like this test will pass.
        questions[0][0].click()
        if assert_submit:
            self.assertFalse(submit_button.is_enabled())

        # Disagree: Testing is not necessary
        questions[2][3].click()
        if assert_submit:
            self.assertFalse(submit_button.is_enabled())

        # Agree: I like testing software
        questions[1][1].click()
        if assert_submit:
            self.assertFalse(submit_button.is_enabled())

        # Strongly Disagree: I would fake a test result to get software deployed.
        questions[3][4].click()

        if assert_submit:
            # Submit button should now be enabled!
            self.assertTrue(submit_button.is_enabled())

    def test_submit_enabled(self):
        """
        Verify that the submit button is enabled only when every question
        has an answer.
        """
        self.go_to_page('Survey Functions')
        self.fill_survey(assert_submit=True)

    def test_survey_submission(self):
        """
        Verify that the user can submit his or her vote and that the vote counts.

        Also check that feedback is displayed afterward.
        """
        self.go_to_page('Survey Functions')
        self.fill_survey()
        self.get_submit().click()

        self.wait_until_exists('.poll-footnote')

        self.assertEqual(self.browser.find_element_by_css_selector('.poll-footnote').text,
                         'Results gathered from 21 respondents.')

        self.assertTrue(self.browser.find_element_by_css_selector('.poll-feedback').text,
                        "Thank you\nfor running the tests.")

    def test_submit_not_enabled_on_revisit(self):
        """
        Verify that revisiting the page post-vote does not re-enable the submit button.
        """
        self.go_to_page('Survey Functions')

        self.fill_survey()

        self.get_submit().click()

        # Button will be replaced with a new disabled copy, not just disabled.
        self.wait_until_exists('input[name=poll-submit]:disabled')

        self.go_to_page('Poll Functions')
        self.assertFalse(self.get_submit().is_enabled())
