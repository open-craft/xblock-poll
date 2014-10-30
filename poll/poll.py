"""TO-DO: Write a description of what this XBlock is."""
from collections import OrderedDict
from django.template import Template, Context

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, List, Integer, String, Dict
from xblock.fragment import Fragment


class PollBlock(XBlock):
    """
    Poll XBlock. Allows a teacher to poll users, and presents the results so
    far of the poll to the user when finished.
    """
    question = String(default='What is your favorite color?')
    answers = List(
        default=(('Red', 'Red'), ('Blue', 'Blue'), ('Green', 'Green'),
                 ('Other', 'Other')),
        scope=Scope.settings, help="The questions on this poll."
    )
    tally = Dict(default={'Red': 0, 'Blue': 0, 'Green': 0, 'Other': 0},
                 scope=Scope.user_state_summary,
                 help="Total tally of answers from students.")
    # No default. Hopefully this will yield 'None', or do something
    # distinctive when queried.
    # Choices are always one above their place in the index so that choice
    # is never false if it's provided.
    choice = String(scope=Scope.user_state, help="The student's answer")

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    @XBlock.json_handler
    def get_results(self, data, suffix=''):
        return {'question': self.question, 'tally': self.tally_detail()}

    def tally_detail(self):
        """
        Tally all results.
        """
        tally = []
        answers = OrderedDict(self.answers)
        total = 0
        for key, value in answers.items():
            tally.append({
                'count': int(self.tally.get(key, 0)),
                'answer': value,
                'key': key,
                'top': False
            })
            total += tally[-1]['count']

        for answer in tally:
            try:
                percent = (answer['count'] / float(total))
                answer['percent'] = int(percent * 100)
            except ZeroDivisionError:
                answer['percent'] = 0

        tally.sort(key=lambda x: x['count'], reverse=True)
        # This should always be true, but on the off chance there are
        # no answers...
        if tally:
            # Mark the top item to make things easier for Handlebars.
            tally[0]['top'] = True
        return tally

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

        context.update({
            'choice': self.choice,
            # Offset so choices will always be True.
            'answers': self.answers,
            'question': self.question,
            'js_template': js_template,
        })

        if self.choice:
            context.update({'tally': self.tally_detail()})

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
        result = {'success': True, 'errors': {'fields': {}, 'general': []}}
        if 'question' not in data or not data['question']:
            result['errors']['question'] = "This field is required."
            result['success'] = False

        # Aggressively clean/sanity check answers list.
        answers = OrderedDict(
            (key.replace('answer-', '', 1), value.strip()[:250])
            for key, value in data.items()
            if (key.startswith('answer-') and not key == 'answer-')
            and not value.isspace()
        )
        if not len(answers) > 1:
            result['errors']['general'].append(
                "You must include at least two answers.")
            result['success'] = False

        if not result['success']:
            return result

        self.answers = answers.items()
        self.question = data['question']

        tally = self.tally

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
        result = {'success': False}
        if self.choice is not None:
            result['message'] = 'You cannot vote twice.'
            return result
        try:
            choice = data['choice']
        except KeyError:
            result['message'] = 'Answer not included with request.'
            return result
        # Just to show data coming in...
        try:
            OrderedDict(self.answers)[choice]
        except KeyError:
            result['message'] = 'No key "{choice}" in answers table.'.format(choice=choice)
            return result

        self.choice = choice
        self.tally[choice] += 1
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