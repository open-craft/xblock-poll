# pylint: disable=too-many-lines
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
from __future__ import absolute_import

import functools
import json
import time
from collections import OrderedDict

import pkg_resources
import six
from django import utils
from markdown import markdown
from webob import Response
from xblock.completable import XBlockCompletionMode
from xblock.core import XBlock
from xblock.fields import Boolean, Dict, Integer, List, Scope, String
from web_fragments.fragment import Fragment
from xblockutils.publish_event import PublishEventMixin
from xblockutils.resources import ResourceLoader
from xblockutils.settings import ThemableXBlockMixin, XBlockWithSettingsMixin

from .utils import DummyTranslationService, _, remove_markdown_and_html_tags

try:
    # pylint: disable=import-error, bad-option-value, ungrouped-imports
    from django.conf import settings
    from api_manager.models import GroupProfile
    HAS_GROUP_PROFILE = True
except ImportError:
    HAS_GROUP_PROFILE = False

try:
    # pylint: disable=import-error
    from common.djangoapps.static_replace import replace_static_urls
    HAS_STATIC_REPLACE = True
except ImportError:
    HAS_STATIC_REPLACE = False


class ResourceMixin(XBlockWithSettingsMixin, ThemableXBlockMixin):
    loader = ResourceLoader(__name__)

    block_settings_key = 'poll'
    default_theme_config = {
        'package': 'poll',
        'locations': ["public/css/themes/lms.css"]
    }

    @staticmethod
    def resource_string(path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    @property
    def i18n_service(self):
        """ Obtains translation service """
        return self.runtime.service(self, "i18n") or DummyTranslationService()

    def get_translation_content(self):
        try:
            return self.resource_string('public/js/translations/{lang}/textjs.js'.format(
                lang=utils.translation.to_locale(utils.translation.get_language()),
            ))
        except IOError:
            return self.resource_string('public/js/translations/en/textjs.js')

    def create_fragment(self, context, template, css, js, js_init):
        frag = Fragment()
        frag.add_content(self.loader.render_django_template(
            template,
            context=context,
            i18n_service=self.i18n_service,
        ))
        frag.add_javascript_url(
            self.runtime.local_resource_url(self, 'public/js/vendor/handlebars.js')
        )

        frag.add_css(self.resource_string(css))

        frag.add_javascript(self.get_translation_content())
        frag.add_javascript(self.resource_string('public/js/poll_common.js'))
        frag.add_javascript(self.resource_string(js))
        frag.initialize_js(js_init)
        self.include_theme_files(frag)
        return frag


class CSVExportMixin(object):
    """
    Allows Poll or Surveys XBlocks to support CSV downloads of all users'
    details per block.
    """
    active_export_task_id = String(
        # The UUID of the celery AsyncResult for the most recent export,
        # IF we are sill waiting for it to finish
        default="",
        scope=Scope.user_state_summary,
    )
    last_export_result = Dict(
        # The info dict returned by the most recent successful export.
        # If the export failed, it will have an "error" key set.
        default=None,
        scope=Scope.user_state_summary,
    )

    @XBlock.json_handler
    def csv_export(self, data, suffix=''):
        """
        Asynchronously export given data as a CSV file.
        """
        # Launch task
        from .tasks import export_csv_data  # Import here since this is edX LMS specific

        # Make sure we nail down our state before sending off an asynchronous task.
        async_result = export_csv_data.delay(
            six.text_type(getattr(self.scope_ids, 'usage_id', None)),
            six.text_type(getattr(self.runtime, 'course_id', 'course_id')),
        )
        if not async_result.ready():
            self.active_export_task_id = async_result.id
        else:
            self._store_export_result(async_result)

        return self._get_export_status()

    @XBlock.json_handler
    def get_export_status(self, data, suffix=''):
        """
        Return current export's pending status, previous result,
        and the download URL.
        """
        return self._get_export_status()

    def _get_export_status(self):
        self.check_pending_export()
        return {
            'export_pending': bool(self.active_export_task_id),
            'last_export_result': self.last_export_result,
            'download_url': self.download_url_for_last_report,
        }

    def check_pending_export(self):
        """
        If we're waiting for an export, see if it has finished, and if so, get the result.
        """
        from .tasks import export_csv_data  # Import here since this is edX LMS specific
        if self.active_export_task_id:
            async_result = export_csv_data.AsyncResult(self.active_export_task_id)
            if async_result.ready():
                self._store_export_result(async_result)

    @property
    def download_url_for_last_report(self):
        """ Get the URL for the last report, if any """
        from lms.djangoapps.instructor_task.models import ReportStore  # pylint: disable=import-error

        # Unfortunately this is a bit inefficient due to the ReportStore API
        if not self.last_export_result or self.last_export_result['error'] is not None:
            return None

        report_store = ReportStore.from_config(config_name='GRADES_DOWNLOAD')
        course_key = getattr(self.scope_ids.usage_id, 'course_key', None)
        return dict(report_store.links_for(course_key)).get(self.last_export_result['report_filename'])

    def student_module_queryset(self):
        try:
            from lms.djangoapps.courseware.models import StudentModule  # pylint: disable=import-error
        except RuntimeError:
            from courseware.models import StudentModule
        return StudentModule.objects.select_related('student').filter(
            course_id=self.runtime.course_id,
            module_state_key=self.scope_ids.usage_id,
        ).order_by('-modified')

    def _store_export_result(self, task_result):
        """ Given an AsyncResult or EagerResult, save it. """
        self.active_export_task_id = ''
        if task_result.successful():
            if isinstance(task_result.result, dict) and not task_result.result.get('error'):
                self.last_export_result = task_result.result
            else:
                self.last_export_result = {'error': u'Unexpected result: {}'.format(repr(task_result.result))}
        else:
            self.last_export_result = {'error': six.text_type(task_result.result)}

    def prepare_data(self):
        """
        Return a two-dimensional list containing cells of data ready for CSV export.
        """
        raise NotImplementedError

    def get_filename(self):
        """
        Return a string to be used as the filename for the CSV export.
        """
        raise NotImplementedError


class PollBase(XBlock, ResourceMixin, PublishEventMixin):
    """
    Base class for Poll-like XBlocks.
    """
    completion_mode = XBlockCompletionMode.COMPLETABLE
    has_custom_completion = True  # manually submits completion event in send_vote_event

    has_author_view = True

    event_namespace = 'xblock.pollbase'
    private_results = Boolean(default=False, help=_("Whether or not to display results to the user."))
    max_submissions = Integer(default=1, help=_("The maximum number of times a user may send a submission."))
    submissions_count = Integer(
        default=0, help=_("Number of times the user has sent a submission."), scope=Scope.user_state
    )
    feedback = String(default='', help=_("Text to display after the user votes."))

    def send_vote_event(self, choice_data):
        # Let the LMS know the user has answered the poll.
        self.runtime.publish(self, 'completion', {'completion': 1.0})
        # The SDK doesn't set url_name.
        event_dict = {'url_name': getattr(self, 'url_name', '')}
        event_dict.update(choice_data)
        self.publish_event_from_dict(
            self.event_namespace + '.submitted',
            event_dict,
        )

    @staticmethod
    def any_image(field):
        """
        Find out if any answer has an image, since it affects layout.
        """
        return any(value['img'] for key, value in field)

    @staticmethod
    def markdown_items(items):
        """
        Convert all items' labels into markdown.
        """
        return [(key, {'label': markdown(value['label']), 'img': value['img'], 'img_alt': value.get('img_alt')})
                for key, value in items]

    def _get_block_id(self):
        """
        Return unique ID of this block. Useful for HTML ID attributes.

        Works both in LMS/Studio and workbench runtimes:
        - In LMS/Studio, use the location.html_id method.
        - In the workbench, use the usage_id.
        """
        if hasattr(self, 'location'):
            return self.location.html_id()  # pylint: disable=no-member

        return six.text_type(self.scope_ids.usage_id)

    def img_alt_mandatory(self):
        """
        Determine whether alt attributes for images are configured to be mandatory.  Defaults to True.
        """
        settings_service = self.runtime.service(self, "settings")
        if not settings_service:
            return True
        xblock_settings = settings_service.get_settings_bucket(self)
        return xblock_settings.get('IMG_ALT_MANDATORY', True)

    def gather_items(self, data, result, noun, field, image=True):
        """
        Gathers a set of label-img pairs from a data dict and puts them in order.
        """
        items = []
        if field not in data or not isinstance(data[field], list):
            source_items = []
            result['success'] = False
            error_message = self.ugettext(
                # Translators: {field} is either "answers" or "questions".
                "'{field}' is not present, or not a JSON array."
            ).format(field=field)
            result['errors'].append(error_message)
        else:
            source_items = data[field]

        # Make sure all components are present and clean them.
        for item in source_items:
            if not isinstance(item, dict):
                result['success'] = False
                error_message = self.ugettext(
                    # Translators: {noun} is either "Answer" or "Question". {item} identifies the answer or question.
                    "{noun} {item} not a javascript object!"
                ).format(noun=noun, item=item)
                result['errors'].append(error_message)
                continue
            key = item.get('key', '').strip()
            if not key:
                result['success'] = False
                error_message = self.ugettext(
                    # Translators: {noun} is either "Answer" or "Question". {item} identifies the answer or question.
                    "{noun} {item} contains no key."
                ).format(noun=noun, item=item)
                result['errors'].append(error_message)
            image_link = item.get('img', '').strip()
            image_alt = item.get('img_alt', '').strip()
            label = item.get('label', '').strip()
            if not label:
                if image and not image_link:
                    result['success'] = False
                    error_message = self.ugettext(
                        # Translators: {noun} is either "Answer" or "Question".
                        # {noun_lower} is the lowercase version of {noun}.
                        "{noun} has no text or img. Please make sure all {noun_lower}s have one or the other, or both."
                    ).format(noun=noun, noun_lower=noun.lower())
                    result['errors'].append(error_message)
                elif not image:
                    result['success'] = False
                    # If there's a bug in the code or the user just forgot to relabel a question,
                    # votes could be accidentally lost if we assume the omission was an
                    # intended deletion.
                    error_message = self.ugettext(
                        # Translators: {noun} is either "Answer" or "Question".
                        # {noun_lower} is the lowercase version of {noun}.
                        "{noun} was added with no label. All {noun_lower}s must have labels. Please check the form. "
                        "Check the form and explicitly delete {noun_lower}s if not needed."
                    ).format(noun=noun, noun_lower=noun.lower())
                    result['errors'].append(error_message)
            if image_link and not image_alt and self.img_alt_mandatory():
                result['success'] = False
                result['errors'].append(
                    self.ugettext(
                        "All images must have an alternative text describing the image in a way "
                        "that would allow someone to answer the poll if the image did not load."
                    )
                )
            if image:
                items.append((key, {'label': label, 'img': image_link, 'img_alt': image_alt}))
            else:
                items.append([key, label])

        if not items:
            error_message = self.ugettext(
                # Translators: "{noun_lower} is either "answer" or "question".
                "You must include at least one {noun_lower}."
            ).format(noun_lower=noun.lower())
            result['errors'].append(error_message)
            result['success'] = False

        return items

    def can_vote(self):
        """
        Checks to see if the user is permitted to vote. This may not be the case if they used up their max_submissions.
        """
        return self.max_submissions == 0 or self.submissions_count < self.max_submissions

    def can_view_private_results(self):
        """
        Checks to see if the user has permissions to view private results.
        This only works inside the LMS.
        """
        if not hasattr(self.runtime, 'user_is_staff'):
            return False

        # Course staff users have permission to view results.
        if self.runtime.user_is_staff:
            return True

        # Check if user is member of a group that is explicitly granted
        # permission to view the results through django configuration.
        if not HAS_GROUP_PROFILE:
            return False
        group_names = getattr(settings, 'XBLOCK_POLL_EXTRA_VIEW_GROUPS', [])
        if not group_names:
            return False
        user = self.runtime.get_real_user(self.runtime.anonymous_student_id)
        group_ids = user.groups.values_list('id', flat=True)
        return GroupProfile.objects.filter(group_id__in=group_ids, name__in=group_names).exists()

    @staticmethod
    def get_max_submissions(ugettext, data, result, private_results):
        """
        Gets the value of 'max_submissions' from studio submitted AJAX data, and checks for conflicts
        with private_results, which may not be False when max_submissions is not 1, since that would mean
        the student could change their answer based on other students' answers.
        """
        try:
            max_submissions = int(data['max_submissions'])
        except (ValueError, KeyError):
            max_submissions = 1
            result['success'] = False
            result['errors'].append(ugettext('Maximum Submissions missing or not an integer.'))

        # Better to send an error than to confuse the user by thinking this would work.
        if (max_submissions != 1) and not private_results:
            result['success'] = False
            result['errors'].append(ugettext("Private results may not be False when Maximum Submissions is not 1."))
        return max_submissions

    @classmethod
    def static_replace_json_handler(cls, func):
        """A JSON handler that replace all static pseudo-URLs by the actual paths.

        The object returned by func is JSON-serialised, and the resulting string is passed to
        replace_static_urls() to perform regex-based URL replacing.

        We would prefer to explicitly call an API function on single image URLs, but such a function
        is not exposed by the LMS API, so we have to fall back to this slightly hacky implementation.
        """

        @cls.json_handler
        @functools.wraps(func)
        def wrapper(self, request_json, suffix=''):
            response = json.dumps(func(self, request_json, suffix))
            response = replace_static_urls(response, course_id=self.runtime.course_id)
            return Response(response, content_type='application/json', charset='utf8')

        if HAS_STATIC_REPLACE:
            # Only use URL translation if it is available
            return wrapper
        # Otherwise fall back to a standard JSON handler
        return cls.json_handler(func)


@XBlock.wants('settings')
@XBlock.needs('i18n')
class PollBlock(PollBase, CSVExportMixin):
    """
    Poll XBlock. Allows a teacher to poll users, and presents the results so
    far of the poll to the user when finished.
    """
    # pylint: disable=too-many-instance-attributes

    display_name = String(default=_('Poll'))
    question = String(default=_('What is your favorite color?'))
    # This will be converted into an OrderedDict.
    # Key, (Label, Image path)
    answers = List(
        default=[
            ('R', {'label': _('Red'), 'img': None, 'img_alt': None}),
            ('B', {'label': _('Blue'), 'img': None, 'img_alt': None}),
            ('G', {'label': _('Green'), 'img': None, 'img_alt': None}),
            ('O', {'label': _('Other'), 'img': None, 'img_alt': None}),
        ],
        scope=Scope.settings, help=_("The answer options on this poll.")
    )
    tally = Dict(default={'R': 0, 'B': 0, 'G': 0, 'O': 0},
                 scope=Scope.user_state_summary,
                 help=_("Total tally of answers from students."))
    choice = String(scope=Scope.user_state, help=_("The student's answer"))
    event_namespace = 'xblock.poll'

    def clean_tally(self):
        """
        Cleans the tally. Scoping prevents us from modifying this in the studio
        and in the LMS the way we want to without undesirable side effects. So
        we just clean it up on first access within the LMS, in case the studio
        has made changes to the answers.
        """
        answers = dict(self.answers)
        for key in answers:
            if key not in self.tally:
                self.tally[key] = 0

        for key in list(self.tally):
            if key not in answers:
                del self.tally[key]

    def tally_detail(self):
        """
        Return a detailed dictionary from the stored tally that the
        Handlebars template can use.
        """
        tally = []
        answers = OrderedDict(self.markdown_items(self.answers))
        choice = self.get_choice()
        total = 0
        self.clean_tally()
        source_tally = self.tally
        highest_count = None
        for key, value in answers.items():
            count = int(source_tally[key])
            if highest_count is None or count > highest_count:
                highest_count = count
            tally.append({
                'count': count,
                'answer': value['label'],
                'img': value['img'],
                'img_alt': value.get('img_alt'),
                'key': key,
                'first': False,
                'choice': False,
                'last': False,
            })
            total += count

        for answer in tally:
            if answer['key'] == choice:
                answer['choice'] = True
            try:
                answer['percent'] = round(answer['count'] / float(total) * 100)
            except ZeroDivisionError:
                answer['percent'] = 0

            answer['leader'] = answer['count'] == highest_count

        # This should always be true, but on the off chance there are
        # no answers...
        if tally:
            # Mark the first and last items to make things easier for Handlebars.
            tally[0]['first'] = True
            tally[-1]['last'] = True
        return tally, total

    def get_choice(self):
        """
        It's possible for the choice to have been removed since
        the student answered the poll. We don't want to take away
        the user's progress, but they should be able to vote again.
        """
        if self.choice and self.choice in dict(self.answers):
            return self.choice

        return None

    def author_view(self, context=None):
        """
        Used to hide CSV export in Studio view
        """
        context['studio_edit'] = True
        return self.student_view(context)

    @XBlock.supports("multi_device")  # Mark as mobile-friendly
    def student_view(self, context=None):
        """
        The primary view of the PollBlock, shown to students
        when viewing courses.
        """
        if not context:
            context = {}
        js_template = self.resource_string('public/handlebars/poll_results.handlebars')

        choice = self.get_choice()

        context.update({
            'choice': choice,
            'answers': self.markdown_items(self.answers),
            'question': markdown(self.question),
            'private_results': self.private_results,
            # Mustache is treating an empty string as true.
            'feedback': markdown(self.feedback) or False,
            'js_template': js_template,
            'any_img': self.any_image(self.answers),
            'display_name': self.display_name,
            'can_vote': self.can_vote(),
            'max_submissions': self.max_submissions,
            'submissions_count': self.submissions_count,
            'can_view_private_results': self.can_view_private_results(),
            # a11y: Transfer block ID to enable creating unique ids for questions and answers in the template
            'block_id': self._get_block_id(),
        })

        if self.choice:
            detail, total = self.tally_detail()
            context.update({'tally': detail, 'total': total, 'plural': total > 1})

        return self.create_fragment(
            context,
            template="public/html/poll.html",
            css="public/css/poll.css",
            js="public/js/poll.js",
            js_init="PollBlock"
        )

    def student_view_data(self, context=None):
        """
        Returns a JSON representation of the poll Xblock, that can be retrieved
        using Course Block API.
        """
        return {
            'question': self.question,
            'answers': self.answers,
            'max_submissions': self.max_submissions,
            'private_results': self.private_results,
            'feedback': self.feedback,
        }

    @XBlock.handler
    def student_view_user_state(self, data, suffix=''):
        """
        Returns a JSON representation of the student data for Poll Xblock
        """
        response = {
            'choice': self.get_choice(),
            'tally': self.tally,
            'submissions_count': self.submissions_count,
        }

        return Response(
            json.dumps(response),
            content_type='application/json',
            charset='utf8'
        )

    def studio_view(self, context=None):
        if not context:
            context = {}

        js_template = self.resource_string('public/handlebars/poll_studio.handlebars')
        context.update({
            'question': self.question,
            'display_name': self.display_name,
            'private_results': self.private_results,
            'feedback': self.feedback,
            'js_template': js_template,
            'max_submissions': self.max_submissions,
        })
        return self.create_fragment(
            context,
            template="public/html/poll_edit.html",
            css="public/css/poll_edit.css",
            js="public/js/poll_edit.js",
            js_init="PollEdit"
        )

    @XBlock.json_handler
    def load_answers(self, data, suffix=''):
        return {
            'items': [
                {
                    'key': key, 'text': value['label'], 'img': value['img'], 'img_alt': value.get('img_alt'),
                    'noun': 'answer', 'image': True,
                }
                for key, value in self.answers
            ],
        }

    @PollBase.static_replace_json_handler
    def get_results(self, data, suffix=''):
        if self.private_results and not self.can_view_private_results():
            detail, total = {}, None
        else:
            self.publish_event_from_dict(self.event_namespace + '.view_results', {})
            detail, total = self.tally_detail()
        return {
            'question': markdown(self.question),
            'tally': detail,
            'total': total,
            'feedback': markdown(self.feedback),
            'plural': total > 1,
            'display_name': self.display_name,
            'any_img': self.any_image(self.answers),
            # a11y: Transfer block ID to enable creating unique ids for questions and answers in the template
            'block_id': self._get_block_id(),
        }

    @XBlock.json_handler
    def vote(self, data, suffix=''):
        """
        Sets the user's vote.
        """
        result = {'success': False, 'errors': []}
        old_choice = self.get_choice()
        if (old_choice is not None) and not self.private_results:
            result['errors'].append(self.ugettext('You have already voted in this poll.'))
            return result
        try:
            choice = data['choice']
        except KeyError:
            result['errors'].append(self.ugettext('Answer not included with request.'))
            return result
        # Just to show data coming in...
        try:
            OrderedDict(self.answers)[choice]
        except KeyError:
            result['errors'].append(
                self.ugettext(
                    # Translators: {choice} uniquely identifies a specific answer belonging to a poll or survey.
                    'No key "{choice}" in answers table.'
                ).format(choice=choice))
            return result

        if old_choice is None:
            # Reset submissions count if old choice is bogus.
            self.submissions_count = 0

        if not self.can_vote():
            result['errors'].append(self.ugettext('You have already voted as many times as you are allowed.'))
            return result

        self.clean_tally()
        if old_choice is not None:
            self.tally[old_choice] -= 1
        self.choice = choice
        self.tally[choice] += 1
        self.submissions_count += 1

        result['success'] = True
        result['can_vote'] = self.can_vote()
        result['submissions_count'] = self.submissions_count
        result['max_submissions'] = self.max_submissions

        self.send_vote_event({'choice': self.choice})

        return result

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        result = {'success': True, 'errors': []}
        question = data.get('question', '').strip()
        feedback = data.get('feedback', '').strip()
        private_results = bool(data.get('private_results', False))

        max_submissions = self.get_max_submissions(self.ugettext, data, result, private_results)

        display_name = data.get('display_name', '').strip()
        if not question:
            result['errors'].append(self.ugettext("You must specify a question."))
            result['success'] = False

        answers = self.gather_items(data, result, self.ugettext('Answer'), 'answers')

        if not result['success']:
            return result

        self.answers = answers
        self.question = question
        self.feedback = feedback
        self.private_results = private_results
        self.display_name = display_name
        self.max_submissions = max_submissions

        # Tally will not be updated until the next attempt to use it, per
        # scoping limitations.

        return result

    @XBlock.json_handler
    def student_voted(self, data, suffix=''):
        return {
            'voted': self.get_choice() is not None,
            'private_results': self.private_results
        }

    @staticmethod
    def workbench_scenarios():
        """
        Canned scenarios for display in the workbench.
        """
        return [
            ("Default Poll",
             """
             <poll />
             """),
            ("Customized Poll",
             """
             <poll tally="{'long': 20, 'short': 29, 'not_saying': 15, 'longer' : 35}"
                 question="## How long have you been studying with us?"
                 answers='[["longt", {"label": "A very long time", "img": null, "img_alt": null}],
                           ["short", {"label": "Not very long", "img": null, "img_alt": null}],
                           ["not_saying", {"label": "I shall not say", "img": null, "img_alt": null}],
                           ["longer", {"label": "Longer than you", "img": null, "img_alt": null}]]'
                 feedback="### Thank you&#10;&#10;for being a valued student."/>
             """),
        ]

    def get_filename(self):
        return u"poll-data-export-{}.csv".format(time.strftime("%Y-%m-%d-%H%M%S", time.gmtime(time.time())))

    def prepare_data(self):
        header_row = ['user_id', 'username', 'user_email', 'question', 'answer']
        data = {}
        answers_dict = dict(self.answers)
        for sm in self.student_module_queryset():
            choice = json.loads(sm.state)['choice']
            if sm.student.id not in data:
                data[sm.student.id] = [
                    sm.student.id,
                    sm.student.username,
                    sm.student.email,
                    self.question,
                    answers_dict[choice]['label'],
                ]
        return [header_row] + list(data.values())

    def generate_report_data(self, user_state_iterator, limit_responses=None):
        """
        Return a list of student responses to this block in a readable way.

        Arguments:
            user_state_iterator: iterator over UserStateClient objects.
                E.g. the result of user_state_client.iter_all_for_block(block_key)

            limit_responses (int|None): maximum number of responses to include.
                Set to None (default) to include all.

        Returns:
            each call returns a tuple like:
            ("username", {
                           "Question": "What's your favorite color?"
                           "Answer": "Red",
                           "Submissions count": 1
            })
        """
        count = 0
        answers_dict = dict(self.answers)
        for user_state in user_state_iterator:

            if limit_responses is not None and count >= limit_responses:
                # End the iterator here
                return

            choice = user_state.state.get('choice')  # {u'submissions_count': 1, u'choice': u'R'}
            if choice is None:
                continue
            report = {
                self.ugettext('Question'): self.question,
                self.ugettext('Answer'): answers_dict.get(choice, {}).get('label',
                                                                          "[Removed Poll Option {}]".format(choice)),
                self.ugettext('Submissions count'): user_state.state['submissions_count']
            }
            count += 1
            yield (user_state.username, report)

    def index_dictionary(self):
        """
        Return dictionary prepared with module content and type for indexing.
        """
        # return key/value fields in a Python dict object
        # values may be numeric / string or dict
        # default implementation is an empty dict
        xblock_body = super(PollBlock, self).index_dictionary()
        answers = {
            "option_{}".format(answer_i): remove_markdown_and_html_tags(answer[1]['label'])
            for answer_i, answer in enumerate(self.answers)
            if len(answer) == 2 and 'label' in answer[1] and answer[1]['label']
        }
        image_alt_text = {
            "image_alt_{}".format(answer_i): answer[1]['img_alt']
            for answer_i, answer in enumerate(self.answers)
            if len(answer) == 2 and 'img_alt' in answer[1] and answer[1]['img_alt']
        }

        index_body = {
            "display_name": self.display_name,
            "question": remove_markdown_and_html_tags(self.question),
        }
        index_body.update(answers)
        index_body.update(image_alt_text)

        if "content" in xblock_body:
            xblock_body["content"].update(index_body)
        else:
            xblock_body["content"] = index_body

        xblock_body["content_type"] = "Poll"

        return xblock_body


@XBlock.wants('settings')
@XBlock.needs('i18n')
class SurveyBlock(PollBase, CSVExportMixin):
    # pylint: disable=too-many-instance-attributes

    display_name = String(default=_('Survey'))
    # The display name affects how the block is labeled in the studio,
    # but either way we want it to say 'Poll' by default on the page.
    block_name = String(default=_('Poll'))
    answers = List(
        default=[
            ('Y', _('Yes')),
            ('N', _('No')),
            ('M', _('Maybe'))
        ],
        scope=Scope.settings, help=_("Answer choices for this Survey")
    )
    questions = List(
        default=[
            ('enjoy', {'label': _('Are you enjoying the course?'), 'img': None, 'img_alt': None}),
            ('recommend', {
                'label': _('Would you recommend this course to your friends?'),
                'img': None,
                'img_alt': None
            }),
            ('learn', {'label': _('Do you think you will learn a lot?'), 'img': None, 'img_alt': None}),
        ],
        scope=Scope.settings, help=_("Questions for this Survey")
    )
    tally = Dict(
        default={
            'enjoy': {'Y': 0, 'N': 0, 'M': 0}, 'recommend': {'Y': 0, 'N': 0, 'M': 0},
            'learn': {'Y': 0, 'N': 0, 'M': 0}},
        scope=Scope.user_state_summary,
        help=_("Total tally of answers from students.")
    )
    choices = Dict(help=_("The user's answers"), scope=Scope.user_state)
    event_namespace = 'xblock.survey'

    def author_view(self, context=None):
        """
        Used to hide CSV export in Studio view
        """
        context['studio_edit'] = True
        return self.student_view(context)

    @XBlock.supports("multi_device")  # Mark as mobile-friendly
    def student_view(self, context=None):
        """
        The primary view of the SurveyBlock, shown to students
        when viewing courses.
        """
        if not context:
            context = {}

        js_template = self.resource_string('public/handlebars/survey_results.handlebars')

        choices = self.get_choices()

        context.update({
            'choices': choices,
            # Offset so choices will always be True.
            'answers': self.answers,
            'js_template': js_template,
            'questions': self.renderable_answers(self.questions, choices),
            'private_results': self.private_results,
            'any_img': self.any_image(self.questions),
            # Mustache is treating an empty string as true.
            'feedback': markdown(self.feedback) or False,
            'block_name': self.block_name,
            'can_vote': self.can_vote(),
            'submissions_count': self.submissions_count,
            'max_submissions': self.max_submissions,
            'can_view_private_results': self.can_view_private_results(),
            # a11y: Transfer block ID to enable creating unique ids for questions and answers in the template
            'block_id': self._get_block_id(),
            'usage_id': six.text_type(self.scope_ids.usage_id),
        })
        return self.create_fragment(
            context,
            template="public/html/survey.html",
            css="public/css/poll.css",
            js="public/js/poll.js",
            js_init="SurveyBlock"
        )

    def student_view_data(self, context=None):
        """
        Returns a JSON representation of survey XBlock, that can be retrieved
        using Course Block API.
        """
        return {
            'questions': self.questions,
            'answers': self.answers,
            'max_submissions': self.max_submissions,
            'private_results': self.private_results,
            'block_name': self.block_name,
            'feedback': self.feedback,
        }

    @XBlock.handler
    def student_view_user_state(self, data, suffix=''):
        """
        Returns a JSON representation of the student data for Survey Xblock
        """
        response = {
            'choices': self.get_choices(),
            'tally': self.tally,
            'submissions_count': self.submissions_count,
        }

        return Response(
            json.dumps(response),
            content_type='application/json',
            charset='utf8'
        )

    def renderable_answers(self, questions, choices):
        """
        Render markdown for questions, and annotate with answers
        in the case of private_results.
        """
        choices = choices or {}
        markdown_questions = self.markdown_items(questions)
        for key, value in markdown_questions:
            value['choice'] = choices.get(key, None)
        return markdown_questions

    def studio_view(self, context=None):
        if not context:
            context = {}

        js_template = self.resource_string('public/handlebars/poll_studio.handlebars')
        context.update({
            'feedback': self.feedback,
            'display_name': self.block_name,
            'private_results': self.private_results,
            'js_template': js_template,
            'max_submissions': self.max_submissions,
            'multiquestion': True,
        })
        return self.create_fragment(
            context,
            template="public/html/poll_edit.html",
            css="public/css/poll_edit.css",
            js="public/js/poll_edit.js",
            js_init="SurveyEdit"
        )

    def tally_detail(self):
        """
        Return a detailed dictionary from the stored tally that the
        Handlebars template can use.
        """
        tally = []
        questions = OrderedDict(self.markdown_items(self.questions))
        default_answers = OrderedDict([(answer, 0) for answer, __ in self.answers])
        choices = self.choices or {}
        total = 0
        self.clean_tally()
        source_tally = self.tally

        # The result should always be the same-- just grab the first one.
        for key, value in source_tally.items():
            total = sum(value.values())
            break

        for key, value in questions.items():
            # Order matters here.
            answer_set = OrderedDict(default_answers)
            answer_set.update(source_tally[key])
            tally.append({
                'label': value['label'],
                'img': value['img'],
                'img_alt': value.get('img_alt'),
                'answers': [
                    {
                        'count': count, 'choice': False,
                        'key': answer_key, 'top': False,
                    }
                    for answer_key, count in answer_set.items()],
                'key': key,
                'choice': False,
            })

        for question in tally:
            highest = 0
            top_index = None
            for index, answer in enumerate(question['answers']):
                if answer['key'] == choices.get(question['key']):
                    answer['choice'] = True
                # Find the most popular choice.
                if answer['count'] > highest:
                    top_index = index
                    highest = answer['count']
                try:
                    answer['percent'] = round(answer['count'] / float(total) * 100)
                except ZeroDivisionError:
                    answer['percent'] = 0
            if top_index is not None:
                question['answers'][top_index]['top'] = True

        return tally, total

    def clean_tally(self):
        """
        Cleans the tally. Scoping prevents us from modifying this in the studio
        and in the LMS the way we want to without undesirable side effects. So
        we just clean it up on first access within the LMS, in case the studio
        has made changes to the answers.
        """
        questions = dict(self.questions)
        answers = dict(self.answers)
        # pylint: disable=bad-option-value, consider-iterating-dictionary
        default_answers = {answer: 0 for answer in answers.keys()}
        for key in questions.keys():  # pylint: disable=bad-option-value, consider-iterating-dictionary
            if key not in self.tally:
                self.tally[key] = dict(default_answers)
            else:
                # Answers may have changed, requiring an update for each
                # question.
                new_answers = dict(default_answers)
                new_answers.update(self.tally[key])
                for existing_key in self.tally[key]:
                    if existing_key not in default_answers:
                        del new_answers[existing_key]
                self.tally[key] = new_answers
        # Keys for questions that no longer exist can break calculations.
        for key in list(self.tally):
            if key not in questions:
                del self.tally[key]

    def remove_vote(self):
        """
        If the poll has changed after a user has voted, remove their votes
        from the tally.

        This can only be done lazily-- once a user revisits, since we can't
        edit the tally in the studio due to scoping issues.

        This means a user's old votes may still count indefinitely after a
        change, should they never revisit.
        """
        questions = dict(self.questions)
        answers = dict(self.answers)
        for key, value in self.choices.items():
            if key in questions:
                if value in answers:
                    self.tally[key][value] -= 1
        self.choices = None
        self.save()

    def get_choices(self):
        """
        Gets the user's choices, if they're still valid.
        """
        questions = dict(self.questions)
        answers = dict(self.answers)
        if self.choices is None:
            return None
        if sorted(questions.keys()) != sorted(self.choices.keys()):
            self.remove_vote()
            return None
        for value in self.choices.values():
            if value not in answers:
                self.remove_vote()
                return None
        return self.choices

    @PollBase.static_replace_json_handler
    def get_results(self, data, suffix=''):
        if self.private_results and not self.can_view_private_results():
            detail, total = {}, None
        else:
            self.publish_event_from_dict(self.event_namespace + '.view_results', {})
            detail, total = self.tally_detail()
        return {
            'answers': [
                {'key': key, 'label': label} for key, label in self.answers
            ],
            'tally': detail,
            'total': total,
            'feedback': markdown(self.feedback),
            'plural': total > 1,
            'block_name': self.block_name,
            # a11y: Transfer block ID to enable creating unique ids for questions and answers in the template
            'block_id': self._get_block_id()
        }

    @XBlock.json_handler
    def load_answers(self, data, suffix=''):
        return {
            'items': [
                {
                    'key': key, 'text': value,
                    'noun': 'answer', 'image': False,
                }
                for key, value in self.answers
            ],
        }

    @XBlock.json_handler
    def load_questions(self, data, suffix=''):
        return {
            'items': [
                {
                    'key': key, 'text': value['label'], 'img': value['img'], 'img_alt': value.get('img_alt'),
                    'noun': 'question', 'image': True,
                }
                for key, value in self.questions
            ]
        }

    @XBlock.json_handler
    def vote(self, data, suffix=''):
        questions = dict(self.questions)
        answers = dict(self.answers)
        result = {'success': True, 'errors': []}
        choices = self.get_choices()
        if choices and not self.private_results:
            result['success'] = False
            result['errors'].append(self.ugettext("You have already voted in this poll."))

        if not choices:
            # Reset submissions count if choices are bogus.
            self.submissions_count = 0

        if not self.can_vote():
            result['success'] = False
            result['errors'].append(self.ugettext('You have already voted as many times as you are allowed.'))

        # Make sure the user has included all questions, and hasn't included
        # anything extra, which might indicate the questions have changed.
        if not sorted(data.keys()) == sorted(questions.keys()):
            result['success'] = False
            result['errors'].append(
                self.ugettext(
                    "Not all questions were included, or unknown questions were included. "
                    "Try refreshing and trying again."
                )
            )

        # Make sure the answer values are sane.
        for key, value in data.items():
            if value not in answers:
                result['success'] = False
                result['errors'].append(
                    self.ugettext(
                        # Translators: {answer_key} uniquely identifies a specific answer belonging to a poll or survey.
                        # {question_key} uniquely identifies a specific question belonging to a poll or survey.
                        "Found unknown answer '{answer_key}' for question key '{question_key}'"
                    ).format(answer_key=key, question_key=value))

        if not result['success']:
            result['can_vote'] = self.can_vote()
            return result

        # Record the vote!
        if self.choices:
            self.remove_vote()
        self.choices = data
        self.clean_tally()
        for key, value in self.choices.items():
            self.tally[key][value] += 1
        self.submissions_count += 1

        self.send_vote_event({'choices': self.choices})
        result['can_vote'] = self.can_vote()
        result['submissions_count'] = self.submissions_count
        result['max_submissions'] = self.max_submissions

        return result

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        # I wonder if there's something for live validation feedback already.

        result = {'success': True, 'errors': []}
        feedback = data.get('feedback', '').strip()
        block_name = data.get('display_name', '').strip()
        private_results = bool(data.get('private_results', False))
        max_submissions = self.get_max_submissions(self.ugettext, data, result, private_results)

        answers = self.gather_items(data, result, self.ugettext('Answer'), 'answers', image=False)
        questions = self.gather_items(data, result, self.ugettext('Question'), 'questions')

        if not result['success']:
            return result

        self.answers = answers
        self.questions = questions
        self.feedback = feedback
        self.private_results = private_results
        self.max_submissions = max_submissions
        self.block_name = block_name

        # Tally will not be updated until the next attempt to use it, per
        # scoping limitations.

        return result

    @XBlock.json_handler
    def student_voted(self, data, suffix=''):
        return {
            'voted': self.get_choices() is not None,
            'private_results': self.private_results
        }

    @staticmethod
    def workbench_scenarios():
        """
        Canned scenarios for display in the workbench.
        """
        return [
            ("Default Survey",
             """
             <survey />
             """),
            ("Survey Functions",
             """
             <survey tally='{"q1": {"sa": 5, "a": 5, "n": 3, "d": 2, "sd": 5},
                             "q2": {"sa": 3, "a": 2, "n": 3, "d": 10, "sd": 2},
                             "q3": {"sa": 2, "a": 7, "n": 1, "d": 4, "sd": 6},
                             "q4": {"sa": 1, "a": 2, "n": 8, "d": 4, "sd": 5}}'
                 questions='[["q1", {"label": "I feel like this test will pass.", "img": null, "img_alt": null}],
                             ["q2", {"label": "I like testing software", "img": null, "img_alt": null}],
                             ["q3", {"label": "Testing is not necessary", "img": null, "img_alt": null}],
                             ["q4", {"label": "I would fake a test result to get software deployed.", "img": null,
                                     "img_alt": null}]]'
                 answers='[["sa", "Strongly Agree"], ["a", "Agree"], ["n", "Neutral"],
                           ["d", "Disagree"], ["sd", "Strongly Disagree"]]'
                 feedback="### Thank you&#10;&#10;for running the tests."/>
             """),
            ("Survey Multiple",
             """
             <vertical_demo>
                 <survey tally='{"q1": {"sa": 5, "a": 5, "n": 3, "d": 2, "sd": 5}}'
                     questions='[["q1", {"label": "I feel like this test will pass.", "img": null, "img_alt": null}]]'
                     answers='[["sa", "Strongly Agree"], ["a", "Agree"], ["n", "Neutral"],
                               ["d", "Disagree"], ["sd", "Strongly Disagree"]]'
                     feedback="### Thank you&#10;&#10;for running the tests."/>
                 <survey tally='{"q1": {"sa": 5, "a": 5, "n": 3, "d": 2, "sd": 5}}'
                     questions='[["q1", {"label": "Most likely to win the World Cup.", "img": null, "img_alt": null}]]'
                     answers='[["sa", "South Africa"], ["a", "Angola"], ["n", "Netherlands"],
                               ["d", "Deutschland"], ["sd", "Someone different"]]'
                     feedback="### Thank you&#10;&#10;for running the tests."/>
             </vertical_demo>
             """),
        ]

    def get_filename(self):
        return u"survey-data-export-{}.csv".format(time.strftime("%Y-%m-%d-%H%M%S", time.gmtime(time.time())))

    def prepare_data(self):
        header_row = ['user_id', 'username', 'user_email']
        sorted_questions = sorted(self.questions, key=lambda x: x[0])
        questions = [q[1]['label'] for q in sorted_questions]
        data = {}
        answers_dict = dict(self.answers)
        for sm in self.student_module_queryset():
            state = json.loads(sm.state)
            if sm.student.id not in data and state.get('choices'):
                row = [
                    sm.student.id,
                    sm.student.username,
                    sm.student.email,
                ]
                for q in sorted_questions:
                    choices = state.get('choices')
                    if choices:
                        choice = choices[q[0]]
                        row.append(answers_dict[choice])
                data[sm.student.id] = row
        return [header_row + questions] + list(data.values())

    def generate_report_data(self, user_state_iterator, limit_responses=None):
        """
        Return a list of student responses to this block in a readable way.

        Arguments:
            user_state_iterator: iterator over UserStateClient objects.
                E.g. the result of user_state_client.iter_all_for_block(block_key)

            limit_responses (int|None): maximum number of responses to include.
                Set to None (default) to include all.

        Returns:
            each call returns a tuple like:
            ("username", {
                           "Question": "Are you having fun?"
                           "Answer": "Yes",
                           "Submissions count": 1
            })
        """
        answers_dict = dict(self.answers)
        questions_dict = dict(self.questions)
        count = 0
        for user_state in user_state_iterator:
            # user_state.state={'submissions_count': 1, 'choices': {u'enjoy': u'Y', u'recommend': u'N', u'learn': u'M'}}
            choices = user_state.state.get('choices') or {}
            for question_id, answer_id in choices.items():

                if limit_responses is not None and count >= limit_responses:
                    # End the iterator here
                    return

                question = questions_dict.get(question_id, {}).get('label',
                                                                   "[Removed Survey Question {}]".format(question_id))
                answer = answers_dict.get(answer_id) or "[Removed Survey Option {}]".format(answer_id)
                report = {
                    self.ugettext('Question'): question,
                    self.ugettext('Answer'): answer,
                    self.ugettext('Submissions count'): user_state.state['submissions_count']
                }
                count += 1
                yield (user_state.username, report)

    def index_dictionary(self):
        """
        Return dictionary prepared with module content and type for indexing.
        """
        # return key/value fields in a Python dict object
        # values may be numeric / string or dict
        # default implementation is an empty dict
        xblock_body = super(SurveyBlock, self).index_dictionary()

        questions = {
            "question_{}".format(question_i): remove_markdown_and_html_tags(question[1]['label'])
            for question_i, question in enumerate(self.questions)
            if len(question) == 2 and 'label' in question[1] and question[1]['label']
        }
        answers = {
            "option_{}".format(answer_i): remove_markdown_and_html_tags(answer[1])
            for answer_i, answer in enumerate(self.answers)
            if len(answer) == 2 and answer[1]
        }
        image_alt_text = {
            "image_alt_{}".format(question_i): question[1]['img_alt']
            for question_i, question in enumerate(self.questions)
            if len(question) == 2 and 'img_alt' in question[1] and question[1]['img_alt']
        }

        index_body = {
            "display_name": self.display_name,
        }
        index_body.update(questions)
        index_body.update(answers)
        index_body.update(image_alt_text)

        if "content" in xblock_body:
            xblock_body["content"].update(index_body)
        else:
            xblock_body["content"] = index_body

        xblock_body["content_type"] = "Survey"

        return xblock_body
