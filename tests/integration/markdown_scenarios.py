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
Contains a list of lists that will be used as the DDT arguments for the markdown test.
"""
ddt_scenarios = [
    [
        "Poll Markdown", '.poll-question-container',
        """<h2>This is a test</h2>
<h1>This is only a &gt;&lt;test</h1>

<ul>
<li>One</li>
<li>Two</li>
<li>
<p>Three</p>
</li>
<li>
<p>First</p>
</li>
<li>Second</li>
<li>Third</li>
</ul>
<p>We shall find out if markdown is respected.</p>
<blockquote>
<p>"I have not yet begun to code."</p>
</blockquote>"""
    ],
    [
        "Poll Markdown", '.poll-feedback',
        """<h3>This is some feedback</h3>
<p><a href="http://www.example.com">This is a link</a></p>
<p><a href="http://www.example.com" target="_blank">This is also a link.</a></p>
<p>This is a paragraph with <em>emphasized</em> and <strong>bold</strong> text, and <strong><em>both</em></strong>.</p>""",
        False
    ],
    [
        "Poll Markdown", "label.poll-answer", "<p>I <em>feel</em> like this test will <strong>pass</strong><code>test</code>.</p>",
        True, False
    ],
    [
        "Poll Markdown", "label.poll-answer-label", "<p>I <em>feel</em> like this test will <strong>pass</strong><code>test</code>.</p>",
        False, True
    ],
    [
        "Survey Markdown", '.survey-question', "<p>I <em>feel</em> like this test will <strong>pass</strong><code>test</code>.</p>"
    ],
    [
        "Survey Markdown", '.poll-feedback',
        """<h3>This is some feedback</h3>
<p><a href="http://www.example.com">This is a link</a></p>
<p><a href="http://www.example.com" target="_blank">This is also a link.</a></p>
<p>This is a paragraph with <em>emphasized</em> and <strong>bold</strong> text, and <strong><em>both</em></strong>.</p>""",
        False
    ],
]
