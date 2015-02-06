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

from ddt import ddt, unpack, data
from selenium.common.exceptions import NoSuchElementException
from base_test import PollBaseTest


scenarios = ('Survey Private', ['enjoy', 'recommend', 'learn']), ('Poll Private', ['choice'])

@ddt
class TestPrivateResults(PollBaseTest):
    """
    Check the functionality of private results.
    """

    def make_selections(self, names):
        """
        Selects the first option for each named input.
        """
        for name in names:
            self.browser.find_element_by_css_selector('input[name="%s"]' % name).click()

    def do_submit(self, names):
        """
        Do selection and submit.
        """
        self.make_selections(names)
        submit = self.get_submit()
        submit.click()
        self.wait_until_clickable(self.browser.find_element_by_css_selector('.poll-voting-thanks'))

    @unpack
    @data(*scenarios)
    def test_form_remains(self, page_name, names):
        """
        User should still have a form presented after submitting so they can resubmit.
        """
        self.go_to_page(page_name)
        # Form should be there to begin with, of course.
        self.browser.find_element_by_css_selector('div.poll-block form')
        self.do_submit(names)

    @unpack
    @data(*scenarios)
    def test_no_results(self, page_name, names):
        """
        The handlebars template for results should never be called, and the form should persist.
        """
        self.go_to_page(page_name)
        self.do_submit(names)

        # No results should be showing.
        self.assertNotIn(self.browser.find_element_by_css_selector('div.poll-block').get_attribute('innerHTML'), 'poll-top-choice')
        self.assertRaises(NoSuchElementException, self.browser.find_element_by_css_selector, '.poll-footnote')

    @unpack
    @data(*scenarios)
    def test_submit_button(self, page_name, names):
        self.go_to_page(page_name)
        submit = self.get_submit()
        self.assertIn('Submit', submit.get_attribute('outerHTML'))

        self.make_selections(names)
        submit.click()
        self.wait_until_clickable(self.browser.find_element_by_css_selector('.poll-voting-thanks'))

        self.assertIn('Resubmit', submit.get_attribute('outerHTML'), 'Resubmit')

        # This should persist on page reload.
        self.go_to_page(page_name)
        submit = self.get_submit()
        self.assertIn('Resubmit', submit.get_attribute('outerHTML'), 'Resubmit')

    @unpack
    @data(*scenarios)
    def test_feedback_display(self, page_name, names):
        self.go_to_page(page_name)
        self.assertFalse(self.browser.find_element_by_css_selector('.poll-feedback').is_displayed())
        self.do_submit(names)
        self.assertTrue(self.browser.find_element_by_css_selector('.poll-feedback').is_displayed())
