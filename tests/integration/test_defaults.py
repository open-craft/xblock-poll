"""
Tests to verify a default poll XBlock is a functional demo.

Deeper investigation should be tested in test_poll_functions.
"""
from xblockutils.base_test import SeleniumBaseTest


class TestDefaults(SeleniumBaseTest):
    def test_default_poll(self):
        """
        Verifies that a default poll loads, that it can be voted on, and that
        the tally displays afterward. Verifies that the feedback section does
        not load since it is not enabled by default.
        """