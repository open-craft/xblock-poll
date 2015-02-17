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

from xblockutils.base_test import SeleniumBaseTest


# Default names for inputs for polls/surveys
DEFAULT_SURVEY_NAMES = ('enjoy', 'recommend', 'learn')
DEFAULT_POLL_NAMES = ('choice',)


class PollBaseTest(SeleniumBaseTest):
    default_css_selector = 'div.poll-block'
    module_name = __name__

    def get_submit(self):
        return self.browser.find_element_by_css_selector('input[name="poll-submit"]')

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
