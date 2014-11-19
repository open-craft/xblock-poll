"""
Tests a realistic, configured Poll to make sure that everything works as it
should.
"""
from xblockutils.base_test import SeleniumBaseTest


class TestPollFunctions(SeleniumBaseTest):
    def test_first_load(self):
        """
        Checks first load.

        Verify that the poll loads with the expected choices, that feedback is
        not showing, that the submit button is disabled, and that it is enabled
        when a choice is selected.
        """

    def test_poll_submission(self):
        """
        Verify that the user can submit his or her vote, that the vote
        influences the tally, and that feedback is shown after the vote.
        """

    def test_no_duplicate_vote(self):
        """
        Verify that revisiting the page does not re-enable the submit button.
        """

    def test_no_ballot_stuffing(self):
        """
        Verify that the server rejects a well crafted attempt to force an
        additional vote.
        """