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

from unittest import TestCase

from markdown import markdown


class ProcessMarkdownTest(TestCase):
    def test_markdown_escapes(self):
        start_string = (
"""
## This is an H2.

<h3>This is an H3</h3>

<a href="http://example.com">This link should be preserved.</a>
[This link should be converted.](http://www.example.com)

This is a paragraph of text, despite being just one sentence.

&lt; This should be a less-than symbol.

< So should this, since it's not attached to anything.

> This is going to be a blockquote.

<script type="text/javascript">breakstuff();</script>
"""
        )
        end_string = (
"""<h2>This is an H2.</h2>
<h3>This is an H3</h3>

<p><a href="http://example.com">This link should be preserved.</a>
<a href="http://www.example.com">This link should be converted.</a></p>
<p>This is a paragraph of text, despite being just one sentence.</p>
<p>&lt; This should be a less-than symbol.</p>
<p>&lt; So should this, since it's not attached to anything.</p>
<blockquote>
<p>This is going to be a blockquote.</p>
</blockquote>
<script type="text/javascript">breakstuff();</script>"""
        )
        self.assertEqual(end_string, markdown(start_string))
