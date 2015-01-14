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
