"""TO-DO: Write a description of what this XBlock is."""
from collections import OrderedDict

from django.template import Template, Context

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, List, String, Dict
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader

from .utils import process_markdown


class PollBlock(XBlock):
    """
    Poll XBlock. Allows a teacher to poll users, and presents the results so
    far of the poll to the user when finished.
    """
    question = String(default='What is your favorite color?')
    answers = List(
        default=(('Red', 'Red'), ('Blue', 'Blue'), ('Green', 'Green'),
                 ('Other', 'Other')),
        scope=Scope.settings, help="The question on this poll."
    )
    feedback = String(default='', help="Text to display after the user votes.")
    tally = Dict(default={'Red': 0, 'Blue': 0, 'Green': 0, 'Other': 0},
                 scope=Scope.user_state_summary,
                 help="Total tally of answers from students.")
    choice = String(scope=Scope.user_state, help="The student's answer")

    loader = ResourceLoader(__name__)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    @XBlock.json_handler
    def get_results(self, data, suffix=''):
        detail, total = self.tally_detail()
        return {
            'question': process_markdown(self.question), 'tally': detail,
            'total': total, 'feedback': process_markdown(self.feedback),
        }

    def tally_detail(self):
        """
        Tally all results.
        """
        tally = []
        answers = OrderedDict(self.answers)
        choice = self.get_choice()
        total = 0
        for key, value in answers.items():
            tally.append({
                'count': int(self.tally.get(key, 0)),
                'answer': value,
                'key': key,
                'top': False,
                'choice': False,
                'last': False,
            })
            total += tally[-1]['count']

        for answer in tally:
            try:
                percent = (answer['count'] / float(total))
                answer['percent'] = int(percent * 100)
                if answer['key'] == choice:
                    answer['choice'] = True
            except ZeroDivisionError:
                answer['percent'] = 0

        tally.sort(key=lambda x: x['count'], reverse=True)
        # This should always be true, but on the off chance there are
        # no answers...
        if tally:
            # Mark the top item to make things easier for Handlebars.
            tally[0]['top'] = True
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

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the PollBlock, shown to students
        when viewing courses.
        """
        if not context:
            context = {}

        js_template = self.resource_string(
            '/public/handlebars/results.handlebars')

        choice = self.get_choice()

        context.update({
            'choice': choice,
            # Offset so choices will always be True.
            'answers': self.answers,
            'question': process_markdown(self.question),
            # Mustache is treating an empty string as true.
            'feedback': process_markdown(self.feedback) or False,
            'js_template': js_template,
        })

        if self.choice:
            detail, total = self.tally_detail()
            context.update({'tally': detail, 'total': total})

        context = Context(context)
        html = self.resource_string("public/html/poll.html")
        html = Template(html).render(context)
        frag = Fragment(html)
        frag.add_css(self.resource_string("public/css/poll.css"))
        frag.add_javascript_url(
            self.runtime.local_resource_url(
                self, 'public/js/vendor/handlebars.js'))
        frag.add_javascript(self.resource_string("public/js/poll.js"))
        frag.initialize_js('PollBlock')
        return frag

    @XBlock.json_handler
    def load_answers(self, data, suffix=''):
        return {'answers': [{'key': key, 'text': answer}
                            for key, answer in self.answers
        ]}

    def studio_view(self, context=None):
        if not context:
            context = {}

        js_template = self.resource_string('/public/handlebars/studio.handlebars')
        context.update({
            'question': self.question,
            'feedback': self.feedback,
            'js_template': js_template
        })
        context = Context(context)
        html = self.resource_string("public/html/poll_edit.html")
        html = Template(html).render(context)
        frag = Fragment(html)
        frag.add_javascript_url(
            self.runtime.local_resource_url(
                self, 'public/js/vendor/handlebars.js'))
        frag.add_css(self.resource_string('/public/css/poll_edit.css'))
        frag.add_javascript(self.resource_string("public/js/poll_edit.js"))
        frag.initialize_js('PollEditBlock')

        return frag

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        # I wonder if there's something for live validation feedback already.
        result = {'success': True, 'errors': []}
        if 'question' not in data or not data['question']:
            result['errors'].append("You must specify a question.")
            result['success'] = False
        else:
            question = data['question'][:4096]
        if 'feedback' not in data or not data['feedback']:
            feedback = ''
        else:
            feedback = data['feedback'][:4096]

        # Need this meta information, otherwise the questions will be
        # shuffled by Python's dictionary data type.
        poll_order = [key.strip().replace('answer-', '')
                      for key in data.get('poll_order', [])
        ]
        # Aggressively clean/sanity check answers list.
        answers = []
        for key, value in data.items():
            if not key.startswith('answer-'):
                continue
            key = key.replace('answer-', '')
            if not key or key.isspace():
                continue
            value = value.strip()[:250]
            if not value or value.isspace():
                continue
            if key in poll_order:
                answers.append((key, value))

        if not len(answers) > 1:
            result['errors'].append(
                "You must include at least two answers.")
            result['success'] = False

        if not result['success']:
            return result

        # Need to sort the answers.
        answers.sort(key=lambda x: poll_order.index(x[0]), reverse=True)

        self.answers = answers
        self.question = question
        self.feedback = feedback

        tally = self.tally

        answers = OrderedDict(answers)
        # Update tracking schema.
        for key, value in answers.items():
            if key not in tally:
                tally[key] = 0

        for key, value in tally.items():
            if key not in answers:
                del tally[key]

        return result

    @XBlock.json_handler
    def vote(self, data, suffix=''):
        """
        An example handler, which increments the data.
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

        self.choice = choice
        running_total = self.tally.get(choice, 0)
        self.tally[choice] = running_total + 1
        # Let the LMS know the user has answered the poll.
        self.runtime.publish(self, 'progress', {})
        result['success'] = True

        return result

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("PollBlock",
             """<vertical_demo>
                <poll/>
                </vertical_demo>
             """),
        ]