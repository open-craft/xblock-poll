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

from poll.poll import PollBase
from base_test import PollBaseTest, DEFAULT_SURVEY_NAMES, DEFAULT_POLL_NAMES


scenarios = ('Survey Private', DEFAULT_SURVEY_NAMES), ('Poll Private', DEFAULT_POLL_NAMES)

def stub_view_permission(can_view):
    """
    Patches the 'can_view_private_results' function to return specified answer.
    """
    def stub_view_permissions_decorator(test_fn):
        def test_patched(self, page_name, names):
            original = PollBase.can_view_private_results
            try:
                PollBase.can_view_private_results = lambda self: can_view
                test_fn(self, page_name, names)
            finally:
                PollBase.can_view_private_results = original
        return test_patched
    return stub_view_permissions_decorator


@ddt
class TestPrivateResults(PollBaseTest):
    """
    Check the functionality of private results.
    """

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
        self.assertRaises(NoSuchElementException, self.browser.find_element_by_css_selector, '.poll-results')
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

    @unpack
    @data(*scenarios)
    @stub_view_permission(False)
    def test_results_button_visibility_without_permission(self, page_name, names):
        self.go_to_page(page_name)
        self.assertRaises(NoSuchElementException, self.browser.find_element_by_css_selector, '.view-results-button')

    @unpack
    @data(*scenarios)
    @stub_view_permission(True)
    def test_results_button_visibility_with_permission(self, page_name, names):
        self.go_to_page(page_name)
        self.browser.find_element_by_css_selector('.view-results-button')

    @unpack
    @data(*scenarios)
    @stub_view_permission(True)
    def test_results_button(self, page_name, names):
        self.go_to_page(page_name)
        button = self.browser.find_element_by_css_selector('a.view-results-button')
        button.click()
        self.wait_until_exists('.poll-results')
        self.wait_until_exists('.poll-footnote')
