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

from .base_test import PollBaseTest


ANSWER_SELECTOR = 'label.poll-answer-text'


class TestPollFunctions(PollBaseTest):
    def test_first_load(self):
        """
        Checks first load.

        Verify that the poll loads with the expected choices, that feedback is
        not showing, and that the submit button is disabled.
        """
        self.go_to_page('Poll Functions')
        answer_elements = self.browser.find_elements_by_css_selector(ANSWER_SELECTOR)
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
        answer_elements = self.browser.find_elements_by_css_selector(ANSWER_SELECTOR)
        answer_elements[0].click()

        # When an answer is selected, make sure submit is enabled.
        self.wait_until_exists('button.submit:enabled')

    def test_poll_submission(self):
        """
        Verify that the user can submit his or her vote and that the vote counts.

        Also check that feedback is displayed afterward.
        """
        self.go_to_page('Poll Functions')
        answer_elements = self.browser.find_elements_by_css_selector(ANSWER_SELECTOR)

        # 'Not very long'
        answer_elements[1].click()

        self.get_submit().click()

        self.wait_until_exists('.poll-footnote')

        self.assertTrue(self.browser.find_element_by_css_selector('.poll-feedback').text,
                        "Thank you\nfor being a valued student.")

        self.assertEqual(self.browser.find_element_by_css_selector('.poll-footnote').text,
                         'Results gathered from 100 respondents.')

        self.assertRaises(NoSuchElementException, self.browser.find_element_by_css_selector, 'button.submit')

    def test_submit_not_present_on_revisit(self):
        """
        Verify that revisiting the page post-vote does not show the submit button.
        """
        self.go_to_page('Poll Functions')

        answer_elements = self.browser.find_elements_by_css_selector(ANSWER_SELECTOR)

        # Not very long
        answer_elements[1].click()

        self.get_submit().click()

        self.wait_until_exists('.poll-results-wrapper')

        self.go_to_page('Poll Functions')
        self.assertRaises(NoSuchElementException, self.browser.find_element_by_css_selector, 'button.submit')

    def test_poll_options_a11y(self):
        """
        Checks if there is a programmatic relationship between the question text of a poll
        and the radio buttons representing poll options.

        - The entire poll should be wrapped in a <fieldset> element.
        - The question text of the poll should be wrapped in a <legend> element.
        """
        self.go_to_page('Poll Functions')

        poll = self.browser.find_element_by_css_selector('fieldset.poll-container')
        question = poll.find_element_by_css_selector('legend.poll-question')

        self.assertEqual(question.text, 'How long have you been studying with us?')


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

    def test_survey_options_a11y(self):
        """
        Checks if radio buttons representing survey options are linked to corresponding question and answer.

        This is to ensure that screen reader users can be certain that a given radio button
        is tied to a specific question and answer.
        """
        self.go_to_page('Survey Functions')
        questions = self.browser.find_elements_by_css_selector('.survey-question')
        answers = self.browser.find_elements_by_css_selector('.survey-answer')
        question_text = [question.text for question in questions]
        answer_text = [answer.text for answer in answers]
        rows = self.browser.find_elements_by_css_selector('.survey-row')
        self.assertEqual(len(rows), len(questions))
        for i, row in enumerate(rows):
            self.assertEqual(row.get_attribute('role'), 'group')
            options = row.find_elements_by_css_selector('.survey-option input')
            self.assertEqual(len(options), len(answers))
            for j, option in enumerate(options):
                self.assertIn(answer_text[j], option.get_attribute('aria-label'))
                self.assertIn(option.get_attribute('aria-label'), answer_text)

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

    def test_submit_not_present_on_revisit(self):
        """
        Verify that revisiting the page post-vote does not show the submit button.
        """
        self.go_to_page('Survey Functions')

        self.fill_survey()

        self.get_submit().click()

        self.wait_until_exists('.poll-results-wrapper')

        self.go_to_page('Survey Functions')
        self.assertRaises(NoSuchElementException, self.browser.find_element_by_css_selector, 'button.submit')

    def test_survey_radio_ids_unique(self):
        """
        Verify that multiple surveys on the same page with the same question
        IDs still produce unique HTML radio button IDs.
        """
        self.go_to_page('Survey Multiple')
        elements = self.browser.find_elements_by_css_selector('.survey-option input[type=radio]')
        all_ids = sorted([element.get_attribute('id') for element in elements])
        unique_ids = sorted(list(set(all_ids)))
        self.assertSequenceEqual(all_ids, unique_ids)
