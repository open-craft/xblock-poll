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
Test to make sure the layout for results is sane when taking images into
account.
"""
from __future__ import absolute_import
from ddt import ddt, unpack, data
from tests.integration.base_test import PollBaseTest


@ddt
class TestLayout(PollBaseTest):
    """
    Do tests to verify that the layout of elements makes sense depeneding on
    the number of images.
    """

    @unpack
    @data(('Poll All Pictures', 4), ('Poll One Picture', 4), ('Poll No Pictures', 0))
    def test_images(self, scenario, count):
        """
        Verify the poll-image divs only appear when they need to.
        """
        self.go_to_page(scenario)
        pics = self.browser.find_elements_by_css_selector('.poll-image')
        self.assertEqual(len(pics), count)

        if not count:
            self.browser.find_element_by_css_selector('.poll-answer-text').click()
        else:
            # Pics should be within labels.
            self.browser.find_element_by_css_selector('.poll-image img').click()
        self.get_submit().click()

        self.wait_until_exists('.percentage-gauge')

        self.assertEqual(len(self.browser.find_elements_by_css_selector('.poll-image')), count)

    @data('Poll Size Check', 'Poll Size Check Image')
    def test_poll_size(self, scenario):
        self.go_to_page(scenario)
        width = self.browser.get_window_size()['width']
        poll = self.browser.find_element_by_css_selector('.poll-block')
        self.assertLess(poll.__getattribute__('rect')['width'], width)

        self.browser.find_element_by_css_selector('.poll-answer-text').click()
        self.get_submit().click()

        self.wait_until_exists('.percentage-gauge')

        poll = self.browser.find_element_by_css_selector('.poll-block')
        self.assertLess(poll.__getattribute__('rect')['width'], width)
