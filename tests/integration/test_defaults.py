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
        names = ['enjoy', 'recommend', 'learn']

        # Select the first answer for each.
        for name in names:
            self.browser.find_element_by_css_selector('input[name="%s"]' % name).click()

        submit = self.get_submit()
        submit.click()

        self.wait_until_exists('.survey-percentage')

        # Should now be on the results page.
        for element in self.browser.find_elements_by_css_selector('table > tr'):
            # First element is question, second is first answer result.
            self.assertEqual(element.find_elements_by_css_selector('td')[1].text, '100%')

        # No feedback section.
        self.assertRaises(NoSuchElementException, self.browser.find_element_by_css_selector, '.poll-feedback')
