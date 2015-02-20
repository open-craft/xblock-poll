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
from tests.integration.base_test import PollBaseTest, DEFAULT_POLL_NAMES, DEFAULT_SURVEY_NAMES

scenarios_infinite = (
    ('Survey Max Submissions Infinite', DEFAULT_SURVEY_NAMES),
    ('Poll Max Submissions Infinite', DEFAULT_POLL_NAMES),
)

scenarios_max = (
    ('Survey Max Submissions', DEFAULT_SURVEY_NAMES),
    ('Poll Max Submissions', DEFAULT_POLL_NAMES),
)


@ddt
class TestPrivateResults(PollBaseTest):
    @unpack
    @data(*scenarios_infinite)
    def test_infinite_submissions(self, page, names):
        """
        We can't actually test infinite submissions, but we can be reasonably certain it will work
        if it has worked a few times more than we have allocated, which should be '0' according to the
        setting, which is actually code for 'as often as you like' rather than '0 attempts permitted'.

        Try this by staying on the page, and by loading it up again.
        """
        for __ in range(0, 2):
            self.go_to_page(page)
            for ___ in range(1, 5):
                self.do_submit(names)
            self.assertTrue(self.get_submit().is_enabled())

    @unpack
    @data(*scenarios_max)
    def test_max_submissions_one_view(self, page, names):
        """
        Verify that the user can't submit more than a certain number of times. Our XML allows two submissions.
        """
        self.go_to_page(page)
        for __ in range(0, 2):
            self.do_submit(names)
        self.assertFalse(self.get_submit().is_enabled())

    @unpack
    @data(*scenarios_max)
    def test_max_submissions_reload(self, page, names):
        """
        Same as above, but revisit the page between attempts.
        """
        self.go_to_page(page)
        self.do_submit(names)
        self.go_to_page(page)
        self.do_submit(names)
        self.assertFalse(self.get_submit().is_enabled())

    @unpack
    @data(*scenarios_max)
    def test_max_submissions_counter(self, page, names):
        """
        Verify a counter is displayed stating how many submissions have been used.
        Our XML allows two submissions, and we must mind the off-by-one for range.
        """
        self.go_to_page(page)
        counter_div = self.browser.find_element_by_css_selector('.poll-submissions-count')
        counter = self.browser.find_element_by_css_selector('.poll-current-count')
        self.assertFalse(counter_div.is_displayed())
        for i in range(1, 3):
            self.do_submit(names)
            self.assertTrue(counter_div.is_displayed())
            self.assertEqual(counter.text.strip(), str(i))
