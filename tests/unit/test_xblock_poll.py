import unittest
import json

from xblock.field_data import DictFieldData

from poll.poll import PollBlock, SurveyBlock
from ..utils import MockRuntime, make_request


class TestPollBlock(unittest.TestCase):
    """
    Tests for XBlock Poll.
    """
    def setUp(self):
        """
        Test case setup
        """
        super(TestPollBlock, self).setUp()
        self.runtime = MockRuntime()
        self.poll_data = {
            'display_name': 'My Poll',
            'question': 'What is your favorite color?',
            'answers': [
                ['R', {'label': 'Red'}],
                ['B', {'label': 'Blue'}],
                ['G', {'label': 'Green'}],
                ['O', {'label': 'Other'}],
            ],
            'submissions_count': 5,
        }
        self.poll_block = PollBlock(
            self.runtime,
            DictFieldData(self.poll_data),
            None
        )

    def test_student_view_data(self):
        """
        Test the student_view_data results.
        """
        expected_poll_data = {
            'question': self.poll_data['question'],
            'answers': self.poll_data['answers'],
        }

        student_view_data = self.poll_block.student_view_data()
        self.assertEqual(student_view_data, expected_poll_data)

    def test_student_view_user_state_handler(self):
        """
        Test the student_view_user_state handler results.
        """
        response = json.loads(
            self.poll_block.handle(
                'student_view_user_state',
                make_request('', method='GET')
            ).body
        )
        expected_response = {
            u'choice': None,
            u'submissions_count': 5,
            u'tally': {'R': 0, 'B': 0, 'G': 0, 'O': 0},
        }
        self.assertEqual(response, expected_response)


class TestSurveyBlock(unittest.TestCase):
    """
    Tests for XBlock Survey.
    """
    def setUp(self):
        """
        Test case setup
        """
        super(TestSurveyBlock, self).setUp()
        self.runtime = MockRuntime()
        self.survery_data = {
            'display_name': 'My Survey',
            'questions': [
                ['enjoy', {'label': 'Are you enjoying the course?'}],
                ['recommend', {'label': 'Would you recommend this course to your friends?'}],
                ['learn', {'label': 'Do you think you will learn a lot?'}]
            ],
            'answers': [
                ['Y', 'Yes'],
                ['N', 'No'],
                ['M', 'Maybe']
            ],
            'submissions_count': 5
        }
        self.survey_block = SurveyBlock(
            self.runtime,
            DictFieldData(self.survery_data),
            None
        )

    def test_student_view_data(self):
        """
        Test the student_view_data results.
        """
        expected_survery_data = {
            'questions': self.survery_data['questions'],
            'answers': self.survery_data['answers'],
        }

        student_view_data = self.survey_block.student_view_data()
        self.assertEqual(student_view_data, expected_survery_data)

    def test_student_view_user_state_handler(self):
        """
        Test the student_view_user_state handler results.
        """
        response = json.loads(
            self.survey_block.handle(
                'student_view_user_state',
                make_request('', method='GET')
            ).body
        )
        expected_response = {
            u'choices': None,
            u'submissions_count': 5,
            u'tally': {
                u'enjoy': {u'M': 0, u'N': 0, u'Y': 0},
                u'learn': {u'M': 0, u'N': 0, u'Y': 0},
                u'recommend': {u'M': 0, u'N': 0, u'Y': 0},
            },
        }
        self.assertEqual(response, expected_response)
