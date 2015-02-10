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
Tests to make sure that markdown is both useful and secure.
"""
from ddt import ddt, unpack, data
from .markdown_scenarios import ddt_scenarios
from .base_test import PollBaseTest


@ddt
class MarkdownTestCase(PollBaseTest):
    """
    Tests for the Markdown functionality.
    """

    def get_selector_text(self, selector):
        return self.browser.find_element_by_css_selector(selector).get_attribute('innerHTML').strip()

    @data(*ddt_scenarios)
    @unpack
    def test_markdown(self, page, selector, result, front=True, back=True):
        """
        Test Markdown for a field.

        selector is a CSS selector to check for markdown results
        result is the desired result string
        front means the check will be done before the form is submitted
        back means it will be done afterward.

        Both are checked by default.
        """
        self.go_to_page(page)
        if front:
            self.assertEqual(self.get_selector_text(selector), result)
        if back:
            self.browser.find_element_by_css_selector('input[type=radio]').click()
            self.get_submit().click()
            self.wait_until_exists('.poll-footnote')
            self.assertEqual(self.get_selector_text(selector), result)
