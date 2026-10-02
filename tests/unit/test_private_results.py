"""Private result permissions must apply to handlers, not only their UI."""
import unittest
from types import ModuleType
from unittest.mock import Mock, patch

from xblock.field_data import DictFieldData

from poll.poll import PollBlock, SurveyBlock

from ..utils import MockRuntime, make_request


class TestPrivateResults(unittest.TestCase):
    """Exercise both native providers through the runtime handler dispatcher."""

    @staticmethod
    def block(provider, staff=False, private=True):
        runtime = MockRuntime()
        if staff is not None:
            runtime.user_is_staff = staff
        data = {'display_name': 'Fixture', 'question': 'Fixture question', 'feedback': 'Fixture feedback',
                'block_name': 'Fixture block', 'private_results': private, 'submissions_count': 2}
        if provider is PollBlock:
            data.update(answers=[['yes', {'label': 'Yes', 'img': ''}]], choice='yes', tally={'yes': 7})
        else:
            data.update(questions=[['question', {'label': 'Question', 'img': ''}]], answers=[['yes', 'Yes']],
                        choices={'question': 'yes'}, tally={'question': {'yes': 7}})
        block = provider(runtime, DictFieldData(data), None)
        block.location = Mock()
        block.location.html_id.return_value = 'fixture-block'
        return block

    def test_unprivileged_export_handlers_refuse_before_side_effects(self):
        for provider in (PollBlock, SurveyBlock):
            for staff in (False, None):
                for private in (False, True):
                    for handler in ('csv_export', 'get_export_status'):
                        with self.subTest(provider=provider, staff=staff, private=private, handler=handler):
                            block = self.block(provider, staff=staff, private=private)
                            block.active_export_task_id = 'existing-task'
                            block.last_export_result = {'report_filename': 'private.csv', 'error': None}
                            block._get_export_status = Mock(return_value={'download_url': 'private-url'})
                            task = Mock()
                            tasks = ModuleType('poll.tasks')
                            tasks.export_csv_data = task
                            with patch.dict('sys.modules', {'poll.tasks': tasks}):
                                response = block.handle(handler, make_request('{}'))
                            self.assertEqual(response.status_int, 403)
                            self.assertEqual(response.json, {'error': 'Forbidden'})
                            task.delay.assert_not_called()
                            block._get_export_status.assert_not_called()
                            self.assertEqual(block.active_export_task_id, 'existing-task')
                            self.assertEqual(block.last_export_result['report_filename'], 'private.csv')

    def test_staff_export_handlers_preserve_native_task_and_status(self):
        for provider in (PollBlock, SurveyBlock):
            with self.subTest(provider=provider):
                block = self.block(provider, staff=True)
                status = {'export_pending': True, 'last_export_result': None, 'download_url': None}
                block._get_export_status = Mock(return_value=status)
                result = Mock(id='new-task')
                result.ready.return_value = False
                task = Mock()
                task.delay.return_value = result
                tasks = ModuleType('poll.tasks')
                tasks.export_csv_data = task
                with patch.dict('sys.modules', {'poll.tasks': tasks}):
                    response = block.handle('csv_export', make_request('{}'))
                self.assertEqual(response.status_int, 200)
                self.assertEqual(response.json, status)
                task.delay.assert_called_once()
                self.assertEqual(block.active_export_task_id, 'new-task')
                block._get_export_status.assert_called_once_with()
                block._get_export_status.reset_mock()
                response = block.handle('get_export_status', make_request('{}'))
                self.assertEqual(response.status_int, 200)
                self.assertEqual(response.json, status)
                block._get_export_status.assert_called_once_with()

    def test_export_uses_the_existing_permission_including_extra_roles(self):
        for provider in (PollBlock, SurveyBlock):
            with self.subTest(provider=provider):
                block = self.block(provider)
                block.can_view_private_results = Mock(return_value=True)
                block._get_export_status = Mock(return_value={'download_url': 'permitted-url'})
                response = block.handle('get_export_status', make_request('{}'))
                self.assertEqual(response.status_int, 200)
                self.assertEqual(response.json['download_url'], 'permitted-url')
                block.can_view_private_results.assert_called_once_with()

    def test_private_tally_hidden_without_losing_own_response(self):
        for provider in (PollBlock, SurveyBlock):
            for staff in (False, None):
                with self.subTest(provider=provider, staff=staff):
                    block = self.block(provider, staff=staff)
                    response = block.handle('student_view_user_state', make_request('', method='GET'))
                    self.assertEqual(response.status_int, 200)
                    self.assertEqual(response.json['tally'], {})
                    self.assertEqual(response.json['submissions_count'], 2)
                    self.assertEqual(response.json['choice' if provider is PollBlock else 'choices'],
                                     'yes' if provider is PollBlock else {'question': 'yes'})
                    self.assertEqual(block.tally, {'yes': 7} if provider is PollBlock else {'question': {'yes': 7}})

    def test_public_or_permitted_tally_remains_visible(self):
        for provider in (PollBlock, SurveyBlock):
            for staff, private in ((False, False), (True, True), (True, False)):
                with self.subTest(provider=provider, staff=staff, private=private):
                    block = self.block(provider, staff=staff, private=private)
                    response = block.handle('student_view_user_state', make_request('', method='GET'))
                    self.assertEqual(response.status_int, 200)
                    self.assertEqual(response.json['tally'], block.tally)

    def test_private_results_handler_returns_hidden_results_without_server_error(self):
        for provider in (PollBlock, SurveyBlock):
            with self.subTest(provider=provider):
                block = self.block(provider)
                response = block.handle('get_results', make_request('{}'))
                self.assertEqual(response.status_int, 200)
                self.assertEqual(response.json['tally'], {})
                self.assertIsNone(response.json['total'])
                self.assertIs(response.json['plural'], False)
