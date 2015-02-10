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
from tests.integration.base_test import PollBaseTest


class TestLayout(PollBaseTest):
    """
    Do tests to verify that the layout of elements makes sense depeneding on
    the number of images.
    """

    def test_all_images(self):
        """
        Verify img tags are created for answers when they're all set.
        """
        self.go_to_page('Poll All Pictures')
        pics = self.browser.find_elements_by_css_selector('.poll-image')
        self.assertEqual(len(pics), 4)

        # Pics should be within labels.
        pics[0].find_element_by_css_selector('img').click()
        self.get_submit().click()

        self.wait_until_exists('.poll-image')

        self.assertEqual(len(self.browser.find_elements_by_css_selector('.poll-image')), 4)

    def test_one_image(self):
        """
        Verify layout is sane when only one answer has an image.
        """
        self.go_to_page('Poll One Picture')
        pics = self.browser.find_elements_by_css_selector('.poll-image')
        # On the polling page, there should only be one pics div.
        self.assertEqual(len(pics), 1)

        pics[0].find_element_by_css_selector('img').click()

        self.get_submit().click()

        self.wait_until_exists('.poll-image.result-image')
        # ...But on the results page, we need four, for table layout.
        self.assertEqual(len(self.browser.find_elements_by_css_selector('.poll-image')), 4)
