"""
Tests to make sure that markdown is both useful and secure.
"""
from .base_test import PollBaseTest


class MarkdownTestCase(PollBaseTest):
    """
    Tests for the Markdown functionality.
    """
    def test_question_markdown(self):
        """
        Ensure Markdown is parsed for questions.
        """
        self.go_to_page("Markdown")
        self.assertEqual(
            self.browser.find_element_by_css_selector('.poll-question-container').text,
            """This is a test
This is only a ><test
One
Two
Three
First
Second
Third
We shall find out if markdown is respected.
"I have not yet begun to code.\"""")

    def test_feedback_markdown(self):
        """
        Ensure Markdown is parsed for feedback.
        """
        self.go_to_page("Markdown")
        self.browser.find_element_by_css_selector('input[type=radio]').click()
        self.browser.find_element_by_css_selector('input[name="poll-submit"]').click()

        self.assertEqual(
            self.browser.find_element_by_css_selector('.poll-feedback').text,
            """This is some feedback
This is a link
This is also a link.
This is a paragraph with emphasized and bold text, and both.""")