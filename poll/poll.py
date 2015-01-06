"""TO-DO: Write a description of what this XBlock is."""
from collections import OrderedDict

from django.template import Template, Context
from markdown import markdown

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, String, Dict, List
from xblock.fragment import Fragment
from xblockutils.publish_event import PublishEventMixin
from xblockutils.resources import ResourceLoader


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

    def send_vote_event(self, choice_data):
        # Let the LMS know the user has answered the poll.
        self.runtime.publish(self, 'progress', {})
        self.runtime.publish(self, 'grade', {
            'value': 1,
            'max_value': 1,
            }
        )
        self.publish_event_from_dict(
            self.event_namespace + '.submitted',
            choice_data,
        )

    @staticmethod
    def any_image(field):
        """
        Find out if any answer has an image, since it affects layout.
        """
        return any(value['img'] for value in dict(field).values())

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
                        "{0} has no text or img. Please make sure all {0}s "
                        "have one or the other, or both.".format(noun))
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

        if not len(items) > 1:
            result['errors'].append(
                "You must include at least two {0}s.".format(noun.lower()))
            result['success'] = False

        return items


class PollBlock(PollBase):
    """
    Poll XBlock. Allows a teacher to poll users, and presents the results so
    far of the poll to the user when finished.
    """
    display_name = String(default='Poll')
    question = String(default='What is your favorite color?')
    # This will be converted into an OrderedDict.
    # Key, (Label, Image path)
    answers = List(
        default=(('R', {'label': 'Red', 'img': None}), ('B', {'label': 'Blue', 'img': None}),
                 ('G', {'label': 'Green', 'img': None}), ('O', {'label': 'Other', 'img': None})),
        scope=Scope.settings, help="The answer options on this poll."
    )
    feedback = String(default='', help="Text to display after the user votes.")
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
        answers = OrderedDict(self.answers)
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
            'answers': self.answers,
            'question': markdown(self.question),
            # Mustache is treating an empty string as true.
            'feedback': markdown(self.feedback) or False,
            'js_template': js_template,
            'any_img': self.any_image(self.answers),
            # The SDK doesn't set url_name.
            'url_name': getattr(self, 'url_name', ''),
            "display_name": self.display_name,
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
            'feedback': self.feedback,
            'js_template': js_template
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
        if self.get_choice() is not None:
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

        self.clean_tally()
        self.choice = choice
        self.tally[choice] = self.tally.get(choice, 0) + 1

        result['success'] = True

        self.send_vote_event({'choice': self.choice})

        return result

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        # I wonder if there's something for live validation feedback already.

        result = {'success': True, 'errors': []}
        question = data.get('question', '').strip()
        feedback = data.get('feedback', '').strip()
        display_name = data.get('display_name', '').strip()
        if not question:
            result['errors'].append("You must specify a question.")
            result['success'] = False

        if not result['success']:
            return result

        answers = self.gather_items(data, result, 'Answer', 'answers')

        self.answers = answers
        self.question = question
        self.feedback = feedback
        self.display_name = display_name

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
             <vertical_demo>
                 <poll />
             </vertical_demo>
             """),
            ("Customized Poll",
             """
             <vertical_demo>
                 <poll url_name="poll_functions" question="## How long have you been studying with us?"
                     feedback="### Thank you&#10;&#10;for being a valued student."
                     tally="{'long': 20, 'short': 29, 'not_saying': 15, 'longer' : 35}"
                     answers="[['long', 'A very long time'], ['short', 'Not very long'], ['not_saying', 'I shall not say'], ['longer', 'Longer than you']]"/>
            </vertical_demo>
             """),
        ]


class SurveyBlock(PollBase):
    display_name = String(default='Survey')
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
    feedback = String(default='', help="Text to display after the user votes.")
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

        context.update({
            'choices': self.get_choices(),
            # Offset so choices will always be True.
            'answers': self.answers,
            'js_template': js_template,
            'questions': self.questions,
            'any_img': self.any_image(self.questions),
            # Mustache is treating an empty string as true.
            'feedback': markdown(self.feedback) or False,
            # The SDK doesn't set url_name.
            'url_name': getattr(self, 'url_name', ''),
            "display_name": self.display_name,
        })

        return self.create_fragment(
            context, "public/html/survey.html", "public/css/poll.css",
            "public/js/poll.js", "SurveyBlock")

    def studio_view(self, context=None):
        if not context:
            context = {}

        js_template = self.resource_string('/public/handlebars/poll_studio.handlebars')
        context.update({
            'feedback': self.feedback,
            'display_name': self.display_name,
            'js_template': js_template,
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
        questions = OrderedDict(self.questions)
        default_answers = OrderedDict([(answer, 0) for answer, __ in self.answers])
        choices = self.get_choices()
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
                'text': value['label'],
                'answers': [
                    {
                        'count': count, 'choice': False,
                        'key': answer_key, 'top': False
                    }
                    for answer_key, count in answer_set.items()],
                'key': key,
                'choice': False,
            })

        for question in tally:
            highest = 0
            top_index = None
            for index, answer in enumerate(question['answers']):
                if answer['key'] == choices[question['key']]:
                    answer['choice'] = True
                # Find the most popular choice.
                if answer['count'] > highest:
                    top_index = index
                    highest = answer['count']
                try:
                    answer['percent'] = round(answer['count'] / float(total) * 100)
                except ZeroDivisionError:
                    answer['percent'] = 0
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
                for existing_key in new_answers:
                    if existing_key not in default_answers:
                        del new_answers[existing_key]
                self.tally[key] = new_answers

    def get_choices(self):
        """
        Gets the user's choices, if they're still valid.
        """
        questions = dict(self.questions)
        answers = dict(self.answers)
        if self.choices is None:
            return None
        # TODO: Remove user's existing votes when this happens.
        if sorted(questions.keys()) != sorted(self.choices.keys()):
            return None
        for value in self.choices.values():
            if value not in answers:
                return None
        return self.choices

    @XBlock.json_handler
    def get_results(self, data, suffix=''):
        self.publish_event_from_dict(self.event_namespace + '.view_results', {})
        detail, total = self.tally_detail()
        return {
            'answers': [
                value for value in OrderedDict(self.answers).values()],
            'tally': detail, 'total': total, 'feedback': markdown(self.feedback),
            'plural': total > 1, 'display_name': self.display_name,
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
        if choices:
            result['success'] = False
            result['errors'].append("You have already voted in this poll.")

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
            return result

        # Record the vote!
        self.choices = data
        self.clean_tally()
        for key, value in self.choices.items():
            self.tally[key][value] += 1

        self.send_vote_event({'choices': choices})

        return result

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        # I wonder if there's something for live validation feedback already.

        result = {'success': True, 'errors': []}
        feedback = data.get('feedback', '').strip()
        display_name = data.get('display_name', '').strip()

        answers = self.gather_items(data, result, 'Answer', 'answers', image=False)
        questions = self.gather_items(data, result, 'Question', 'questions')

        if not result['success']:
            return result

        self.answers = answers
        self.questions = questions
        self.feedback = feedback
        self.display_name = display_name

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
             <vertical_demo>
                 <survey />
             </vertical_demo>
             """),
            ("Survey Functions",
             """
             <vertical_demo>
                 <survey tally='{"q1": {"sa": 5, "a": 5, "n": 3, "d": 2, "sd": 5}, "q2": {"sa": 3, "a": 2, "n": 3, "d": 10, "sd": 2}, "q3": {"sa": 2, "a": 7, "n": 1, "d": 4, "sd": 6}, "q4": {"sa": 1, "a": 2, "n": 8, "d": 4, "sd": 5}}'
                     questions='[["q1", "I feel like this test will pass."], ["q2", "I like testing software"], ["q3", "Testing is not necessary"], ["q4", "I would fake a test result to get software deployed."]]'
                     answers='[["sa", {"label": "Strongly Agree"}], ["a", {"label": "Agree"}], ["n", {"label": "Neutral"}], ["d", {"label": "Disagree"}], ["sd", {"label": "Strongly Disagree"}]]'
                     feedback="### Thank you&#10;&#10;for running the tests."/>
             </vertical_demo>
             """)
        ]
