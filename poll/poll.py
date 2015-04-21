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

from collections import OrderedDict

from django.template import Template, Context
from markdown import markdown

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, String, Dict, List, Boolean, Integer
from xblock.fragment import Fragment
from xblockutils.publish_event import PublishEventMixin
from xblockutils.resources import ResourceLoader

HAS_EDX_ACCESS = False
try:
    # pylint: disable=import-error
    from django.conf import settings
    from courseware.access import has_access
    from api_manager.models import GroupProfile
    HAS_EDX_ACCESS = True
except ImportError:
    pass


class ResourceMixin(object):
    loader = ResourceLoader(__name__)

    @staticmethod
    def resource_string(path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def create_fragment(self, context, template, css, js, js_init):
        html = Template(
            self.resource_string(template)).render(Context(context))
        frag = Fragment(html)
        frag.add_javascript_url(
            self.runtime.local_resource_url(
                self, 'public/js/vendor/handlebars.js'))
        frag.add_css(self.resource_string(css))
        frag.add_javascript(self.resource_string(js))
        frag.initialize_js(js_init)
        return frag


class PollBase(XBlock, ResourceMixin, PublishEventMixin):
    """
    Base class for Poll-like XBlocks.
    """
    event_namespace = 'xblock.pollbase'
    private_results = Boolean(default=False, help="Whether or not to display results to the user.")
    max_submissions = Integer(default=1, help="The maximum number of times a user may send a submission.")
    submissions_count = Integer(
        default=0, help="Number of times the user has sent a submission.", scope=Scope.user_state
    )
    feedback = String(default='', help="Text to display after the user votes.")

    def send_vote_event(self, choice_data):
        # Let the LMS know the user has answered the poll.
        self.runtime.publish(self, 'progress', {})
        self.runtime.publish(self, 'grade', {
            'value': 1,
            'max_value': 1,
            }
        )
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
        return any(value['img'] for value in dict(field).values())

    @staticmethod
    def markdown_items(items):
        """
        Convert all items' labels into markdown.
        """
        return [[key, {'label': markdown(value['label']), 'img': value['img']}]
                for key, value in items]

    @staticmethod
    def gather_items(data, result, noun, field, image=True):
        """
        Gathers a set of label-img pairs from a data dict and puts them in order.
        """
        items = []
        if field not in data or not isinstance(data[field], list):
            source_items = []
            result['success'] = False
            result['errors'].append(
                "'{0}' is not present, or not a JSON array.".format(field))
        else:
            source_items = data[field]

        # Make sure all components are present and clean them.
        for item in source_items:
            if not isinstance(item, dict):
                result['success'] = False
                result['errors'].append(
                    "{0} {1} not a javascript object!".format(noun, item))
                continue
            key = item.get('key', '').strip()
            if not key:
                result['success'] = False
                result['errors'].append(
                    "{0} {1} contains no key.".format(noun, item))
            image_link = item.get('img', '').strip()
            label = item.get('label', '').strip()
            if not label:
                if image and not image_link:
                    result['success'] = False
                    result['errors'].append(
                        "{0} has no text or img. Please make sure all {1}s "
                        "have one or the other, or both.".format(noun, noun.lower()))
                elif not image:
                    result['success'] = False
                    # If there's a bug in the code or the user just forgot to relabel a question,
                    # votes could be accidentally lost if we assume the omission was an
                    # intended deletion.
                    result['errors'].append("{0} was added with no label. "
                                            "All {1}s must have labels. Please check the form. "
                                            "Check the form and explicitly delete {1}s "
                                            "if not needed.".format(noun, noun.lower()))
            if image:
                # Labels might have prefixed space for markdown, though it's unlikely.
                items.append((key, {'label': label, 'img': image_link.strip()}))
            else:
                items.append([key, label])

        if not items:
            result['errors'].append(
                "You must include at least one {0}.".format(noun.lower()))
            result['success'] = False

        return items

    def can_vote(self):
        """
        Checks to see if the user is permitted to vote. This may not be the case if they used up their max_submissions.
        """
        if self.max_submissions == 0:
            return True
        if self.max_submissions > self.submissions_count:
            return True
        return False

    def can_view_private_results(self):
        """
        Checks to see if the user has permissions to view private results.
        This only works inside the LMS.
        """
        if HAS_EDX_ACCESS and hasattr(self.runtime, 'user') and hasattr(self.runtime, 'course_id'):
            # Course staff users have permission to view results.
            if has_access(self.runtime.user, 'staff', self, self.runtime.course_id):
                return True
            else:
                # Check if user is member of a group that is explicitly granted
                # permission to view the results through django configuration.
                group_names = getattr(settings, 'XBLOCK_POLL_EXTRA_VIEW_GROUPS', [])
                if group_names:
                    group_ids = self.runtime.user.groups.values_list('id', flat=True)
                    return GroupProfile.objects.filter(group_id__in=group_ids, name__in=group_names).exists()
        else:
            return False

    @staticmethod
    def get_max_submissions(data, result, private_results):
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
            result['errors'].append('Maximum Submissions missing or not an integer.')

        # Better to send an error than to confuse the user by thinking this would work.
        if (max_submissions != 1) and not private_results:
            result['success'] = False
            result['errors'].append("Private results may not be False when Maximum Submissions is not 1.")
        return max_submissions


class PollBlock(PollBase):
    """
    Poll XBlock. Allows a teacher to poll users, and presents the results so
    far of the poll to the user when finished.
    """
    # pylint: disable=too-many-instance-attributes

    display_name = String(default='Poll')
    question = String(default='What is your favorite color?')
    # This will be converted into an OrderedDict.
    # Key, (Label, Image path)
    answers = List(
        default=(('R', {'label': 'Red', 'img': None}), ('B', {'label': 'Blue', 'img': None}),
                 ('G', {'label': 'Green', 'img': None}), ('O', {'label': 'Other', 'img': None})),
        scope=Scope.settings, help="The answer options on this poll."
    )
    tally = Dict(default={'R': 0, 'B': 0, 'G': 0, 'O': 0},
                 scope=Scope.user_state_summary,
                 help="Total tally of answers from students.")
    choice = String(scope=Scope.user_state, help="The student's answer")
    event_namespace = 'xblock.poll'

    def clean_tally(self):
        """
        Cleans the tally. Scoping prevents us from modifying this in the studio
        and in the LMS the way we want to without undesirable side effects. So
        we just clean it up on first access within the LMS, in case the studio
        has made changes to the answers.
        """
        answers = OrderedDict(self.answers)
        for key in answers.keys():
            if key not in self.tally:
                self.tally[key] = 0

        for key in self.tally.keys():
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
        any_img = self.any_image(self.answers)
        for key, value in answers.items():
            count = int(source_tally[key])
            tally.append({
                'count': count,
                'answer': value['label'],
                'img': value['img'],
                'key': key,
                'first': False,
                'choice': False,
                'last': False,
                'any_img': any_img,
            })
            total += count

        for answer in tally:
            if answer['key'] == choice:
                answer['choice'] = True
            try:
                answer['percent'] = round(answer['count'] / float(total) * 100)
            except ZeroDivisionError:
                answer['percent'] = 0

        tally.sort(key=lambda x: x['count'], reverse=True)
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
        if self.choice and self.choice in OrderedDict(self.answers):
            return self.choice
        else:
            return None

    def student_view(self, context=None):
        """
        The primary view of the PollBlock, shown to students
        when viewing courses.
        """
        if not context:
            context = {}
        js_template = self.resource_string(
            '/public/handlebars/poll_results.handlebars')

        choice = self.get_choice()

        context.update({
            'choice': choice,
            # Offset so choices will always be True.
            'answers': self.markdown_items(self.answers),
            'question': markdown(self.question),
            'private_results': self.private_results,
            # Mustache is treating an empty string as true.
            'feedback': markdown(self.feedback) or False,
            'js_template': js_template,
            'any_img': self.any_image(self.answers),
            # The SDK doesn't set url_name.
            'url_name': getattr(self, 'url_name', ''),
            'display_name': self.display_name,
            'can_vote': self.can_vote(),
            'max_submissions': self.max_submissions,
            'submissions_count': self.submissions_count,
            'can_view_private_results': self.can_view_private_results(),
        })

        if self.choice:
            detail, total = self.tally_detail()
            context.update({'tally': detail, 'total': total, 'plural': total > 1})

        return self.create_fragment(
            context, "public/html/poll.html", "public/css/poll.css",
            "public/js/poll.js", "PollBlock")

    def studio_view(self, context=None):
        if not context:
            context = {}

        js_template = self.resource_string('/public/handlebars/poll_studio.handlebars')
        context.update({
            'question': self.question,
            'display_name': self.display_name,
            'private_results': self.private_results,
            'feedback': self.feedback,
            'js_template': js_template,
            'max_submissions': self.max_submissions,
        })
        return self.create_fragment(
            context, "public/html/poll_edit.html",
            "/public/css/poll_edit.css", "public/js/poll_edit.js", "PollEdit")

    @XBlock.json_handler
    def load_answers(self, data, suffix=''):
        return {
            'items': [
                {
                    'key': key, 'text': value['label'], 'img': value['img'],
                    'noun': 'answer', 'image': True,
                    }
                for key, value in self.answers
            ],
        }

    @XBlock.json_handler
    def get_results(self, data, suffix=''):
        if self.private_results and not self.can_view_private_results():
            detail, total = {}, None
        else:
            self.publish_event_from_dict(self.event_namespace + '.view_results', {})
            detail, total = self.tally_detail()
        return {
            'question': markdown(self.question), 'tally': detail,
            'total': total, 'feedback': markdown(self.feedback),
            'plural': total > 1, 'display_name': self.display_name,
        }

    @XBlock.json_handler
    def vote(self, data, suffix=''):
        """
        Sets the user's vote.
        """
        result = {'success': False, 'errors': []}
        old_choice = self.get_choice()
        if (old_choice is not None) and not self.private_results:
            result['errors'].append('You have already voted in this poll.')
            return result
        try:
            choice = data['choice']
        except KeyError:
            result['errors'].append('Answer not included with request.')
            return result
        # Just to show data coming in...
        try:
            OrderedDict(self.answers)[choice]
        except KeyError:
            result['errors'].append('No key "{choice}" in answers table.'.format(choice=choice))
            return result

        if old_choice is None:
            # Reset submissions count if old choice is bogus.
            self.submissions_count = 0

        if not self.can_vote():
            result['errors'].append('You have already voted as many times as you are allowed.')
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

        max_submissions = self.get_max_submissions(data, result, private_results)

        display_name = data.get('display_name', '').strip()
        if not question:
            result['errors'].append("You must specify a question.")
            result['success'] = False

        answers = self.gather_items(data, result, 'Answer', 'answers')

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
                 answers='[["longt", {"label": "A very long time", "img": null}],
                           ["short", {"label": "Not very long", "img": null}],
                           ["not_saying", {"label": "I shall not say", "img": null}],
                           ["longer", {"label": "Longer than you", "img": null}]]'
                 feedback="### Thank you&#10;&#10;for being a valued student."/>
             """),
        ]


class SurveyBlock(PollBase):
    # pylint: disable=too-many-instance-attributes

    display_name = String(default='Survey')
    # The display name affects how the block is labeled in the studio,
    # but either way we want it to say 'Poll' by default on the page.
    block_name = String(default='Poll')
    answers = List(
        default=(
            ('Y', 'Yes'), ('N', 'No'),
            ('M', 'Maybe')),
        scope=Scope.settings, help="Answer choices for this Survey"
    )
    questions = List(
        default=(
            ('enjoy', {'label': 'Are you enjoying the course?', 'img': None}),
            ('recommend', {'label': 'Would you recommend this course to your friends?', 'img': None}),
            ('learn', {'label': 'Do you think you will learn a lot?', 'img': None})
        ),
        scope=Scope.settings, help="Questions for this Survey"
    )
    tally = Dict(
        default={
            'enjoy': {'Y': 0, 'N': 0, 'M': 0}, 'recommend': {'Y': 0, 'N': 0, 'M': 0},
            'learn': {'Y': 0, 'N': 0, 'M': 0}},
        scope=Scope.user_state_summary,
        help="Total tally of answers from students."
    )
    choices = Dict(help="The user's answers", scope=Scope.user_state)
    event_namespace = 'xblock.survey'

    def student_view(self, context=None):
        """
        The primary view of the PollBlock, shown to students
        when viewing courses.
        """
        if not context:
            context = {}

        js_template = self.resource_string(
            '/public/handlebars/survey_results.handlebars')

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
            # The SDK doesn't set url_name.
            'url_name': getattr(self, 'url_name', ''),
            'block_name': self.block_name,
            'can_vote': self.can_vote(),
            'submissions_count': self.submissions_count,
            'max_submissions': self.max_submissions,
            'can_view_private_results': self.can_view_private_results(),
        })

        return self.create_fragment(
            context, "public/html/survey.html", "public/css/poll.css",
            "public/js/poll.js", "SurveyBlock")

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

        js_template = self.resource_string('/public/handlebars/poll_studio.handlebars')
        context.update({
            'feedback': self.feedback,
            'display_name': self.block_name,
            'private_results': self.private_results,
            'js_template': js_template,
            'max_submissions': self.max_submissions,
            'multiquestion': True,
        })
        return self.create_fragment(
            context, "public/html/poll_edit.html",
            "/public/css/poll_edit.css", "public/js/poll_edit.js", "SurveyEdit")

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
        questions = OrderedDict(self.questions)
        answers = OrderedDict(self.answers)
        default_answers = {answer: 0 for answer in answers.keys()}
        for key in questions.keys():
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
        for key in self.tally.keys():
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

    @XBlock.json_handler
    def get_results(self, data, suffix=''):
        if self.private_results and not self.can_view_private_results():
            detail, total = {}, None
        else:
            self.publish_event_from_dict(self.event_namespace + '.view_results', {})
            detail, total = self.tally_detail()
        return {
            'answers': [
                value for value in OrderedDict(self.answers).values()],
            'tally': detail, 'total': total, 'feedback': markdown(self.feedback),
            'plural': total > 1, 'block_name': self.block_name,
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
                    'key': key, 'text': value['label'], 'img': value['img'],
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
            result['errors'].append("You have already voted in this poll.")

        if not choices:
            # Reset submissions count if choices are bogus.
            self.submissions_count = 0

        if not self.can_vote():
            result['success'] = False
            result['errors'].append('You have already voted as many times as you are allowed.')

        # Make sure the user has included all questions, and hasn't included
        # anything extra, which might indicate the questions have changed.
        if not sorted(data.keys()) == sorted(questions.keys()):
            result['success'] = False
            result['errors'].append(
                "Not all questions were included, or unknown questions were "
                "included. Try refreshing and trying again."
            )

        # Make sure the answer values are sane.
        for key, value in data.items():
            if value not in answers.keys():
                result['success'] = False
                result['errors'].append(
                    "Found unknown answer '%s' for question key '%s'" % (key, value))

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
        max_submissions = self.get_max_submissions(data, result, private_results)

        answers = self.gather_items(data, result, 'Answer', 'answers', image=False)
        questions = self.gather_items(data, result, 'Question', 'questions')

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
                 questions='[["q1", {"label": "I feel like this test will pass.", "img": null}],
                             ["q2", {"label": "I like testing software", "img": null}],
                             ["q3", {"label": "Testing is not necessary", "img": null}],
                             ["q4", {"label": "I would fake a test result to get software deployed.", "img": null}]]'
                 answers='[["sa", "Strongly Agree"], ["a", "Agree"], ["n", "Neutral"],
                           ["d", "Disagree"], ["sd", "Strongly Disagree"]]'
                 feedback="### Thank you&#10;&#10;for running the tests."/>
             """)
        ]
