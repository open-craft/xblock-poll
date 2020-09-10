from __future__ import absolute_import
import unittest
import json

from xblock.field_data import DictFieldData
from mock import Mock

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
            'max_submissions': 1,
            'private_results': False,
            'feedback': 'My Feedback',
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
            'max_submissions': self.poll_data['max_submissions'],
            'private_results': self.poll_data['private_results'],
            'feedback': self.poll_data['feedback'],
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
            ).body.decode('utf-8')
        )
        expected_response = {
            u'choice': None,
            u'submissions_count': 5,
            u'tally': {'R': 0, 'B': 0, 'G': 0, 'O': 0},
        }
        self.assertEqual(response, expected_response)

    @classmethod
    def mock_user_states(cls):
        return (
            Mock(username='edx', state={'submissions_count': 1, 'choice': 'R'}),
            Mock(username='verified', state={'submissions_count': 1, 'choice': 'G'}),
            Mock(username='staff', state={'submissions_count': 1, 'choice': 'B'}),
            Mock(username='honor', state={'submissions_count': 1, 'choice': 'O'}),
            Mock(username='audit', state={'submissions_count': 1}),
            Mock(username='student', state={'submissions_count': 1, 'choice': None}),
        )

    def test_generate_report_data_dont_limit_responses(self):
        """
        Test generate_report_data iterator with no limit.
        """
        user_states = self.mock_user_states()
        report_data = self.poll_block.generate_report_data(user_states)
        report_data = list(report_data)
        self.assertEqual(len(report_data), 4)
        self.assertEqual(report_data[0],
                         ('edx', {'Question': self.poll_block.question,
                                  'Answer': 'Red',
                                  'Submissions count': 1}))
        self.assertNotIn('audit', [username for username, _ in report_data])
        self.assertNotIn('student', [username for username, _ in report_data])

    def test_generate_report_data_limit_responses(self):
        """
        Test generate_report_data iterator with limit.
        """
        user_states = self.mock_user_states()
        report_data = self.poll_block.generate_report_data(user_states, limit_responses=2)
        report_data = list(report_data)
        self.assertEqual(len(report_data), 2)
        self.assertEqual(report_data[0],
                         ('edx', {'Question': self.poll_block.question,
                                  'Answer': 'Red',
                                  'Submissions count': 1}))

        report_data = self.poll_block.generate_report_data(user_states, limit_responses=0)
        report_data = list(report_data)
        self.assertEqual(len(report_data), 0)

    def test_indexing(self):
        self.assertEqual(
            self.poll_block.index_dictionary(),
            {
                'content': {
                    'display_name': 'My Poll',
                    'question': 'What is your favorite color?',
                    'option_0': 'Red',
                    'option_1': 'Blue',
                    'option_2': 'Green',
                    'option_3': 'Other',
                },
                'content_type': 'Poll'
            }
        )
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
            'submissions_count': 5,
            'max_submissions': 1,
            'private_results': False,
            'feedback': 'My Feedback',
            'block_name': 'My Block Name',
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
            'max_submissions': self.survery_data['max_submissions'],
            'private_results': self.survery_data['private_results'],
            'feedback': self.survery_data['feedback'],
            'block_name': self.survery_data['block_name'],
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
            ).body.decode('utf-8')
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

    @classmethod
    def mock_user_states(cls):
        return (
            Mock(
                username='edx',
                state={
                    'submissions_count': 1,
                    'choices': {'enjoy': 'Y', 'recommend': 'N', 'learn': 'M'}
                }
            ),
            Mock(
                username='verified',
                state={
                    'submissions_count': 1,
                    'choices': {'enjoy': 'M', 'recommend': 'N', 'learn': 'Y'}
                }
            ),
            Mock(
                username='staff',
                state={
                    'submissions_count': 1,
                    'choices': {'enjoy': 'N', 'recommend': 'N', 'learn': 'N'}
                }
            ),
            Mock(
                username='honor',
                state={
                    'submissions_count': 1,
                    'choices': {'enjoy': 'Y', 'recommend': 'N', 'learn': 'M'}
                }
            ),
            Mock(
                username='audit',
                state={
                    'submissions_count': 1,
                }
            ),
            Mock(
                username='student',
                state={
                    'submissions_count': 1,
                    'choices': None,
                }
            ),
        )

    def test_generate_report_data_dont_limit_responses(self):
        """
        Test generate_report_data iterator with no limit.
        """
        user_states = self.mock_user_states()
        report_data = self.survey_block.generate_report_data(user_states)
        report_data = list(report_data)
        self.assertEqual(len(report_data), 12)
        # each choice of a user gets its own row
        # so the first three rows should be edx's choices
        self.assertEqual(['edx', 'edx', 'edx', 'verified'],
                         [username for username, _ in report_data[:4]])
        self.assertEqual(
            set(['Yes', 'No', 'Maybe']),
            set([data['Answer'] for _, data in report_data[:4]])
        )
        self.assertNotIn('audit', [username for username, _ in report_data])
        self.assertNotIn('student', [username for username, _ in report_data])

    def test_generate_report_data_limit_responses(self):
        """
        Test generate_report_data iterator with limit.
        """
        user_states = self.mock_user_states()
        report_data = self.survey_block.generate_report_data(user_states, limit_responses=2)
        report_data = list(report_data)
        self.assertEqual(len(report_data), 2)
        # each choice of a user gets its own row
        # so the first two rows should be edx's choices
        self.assertEqual(['edx', 'edx'],
                         [username for username, _ in report_data])
        self.assertTrue(
            set([data['Answer'] for _, data in report_data[:3]]) <= set(['Yes', 'No', 'Maybe'])
        )

        report_data = self.survey_block.generate_report_data(user_states, limit_responses=0)
        report_data = list(report_data)
        self.assertEqual(len(report_data), 0)

    def test_indexing(self):
        self.assertEqual(
            self.survey_block.index_dictionary(),
            {
                'content': {
                    'display_name': 'My Survey',
                    'question_0': 'Are you enjoying the course?',
                    'question_1': 'Would you recommend this course to your friends?',
                    'question_2': 'Do you think you will learn a lot?',
                    'option_0': 'Yes',
                    'option_1': 'No',
                    'option_2': 'Maybe',
                },
                'content_type': 'Survey'
            }
        )
