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

from __future__ import absolute_import
from tests.integration.base_test import PollBaseTest

from unittest import skip

class TestSubmitButton(PollBaseTest):

    @skip("Flaky test")
    def test_submit_button(self):
        """
        Goal: We have to make sure that submit button gets disabled right
        after it is clicked. We cannot test with 100% assurance by adding a
        method in other tests such as test_functions.py because in that case
        submit button is anyway disabled after the ajax request.

        We can utilize infinite submission feature and check if the submit
        button was disabled (because of js) and then re-enabled (because of
        ajax request).
        """
        self.go_to_page('Poll Submit Button')
        # Find all the radio choices
        answer_elements = self.browser.find_elements_by_css_selector('label.poll-answer-text')
        # Select the first choice
        answer_elements[1].click()
        # When an answer is selected, make sure submit is enabled.
        self.wait_until_exists('button.submit:enabled')

        submit_button = self.get_submit()
        submit_button.click()

        # Make sure that submit button is disabled right away
        self.assertFalse(submit_button.is_enabled())

        self.wait_until_clickable(self.browser.find_element_by_css_selector('.poll-voting-thanks'))
        # Wait until the ajax request is finished and submit button is enabled
        self.assertTrue(self.get_submit().is_enabled())
