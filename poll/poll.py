"""TO-DO: Write a description of what this XBlock is."""
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
        default=['Red', 'Blue', 'Green', 'Other'],
        scope=Scope.settings, help="The questions on this poll."
    )
    tally = Dict(default={1: 0, 2: 0, 3: 0, 4: 0}, scope=Scope.user_state_summary,
                 help="Total tally of answers from students.")
    # No default. Hopefully this will yield 'None', or do something
    # distinctive when queried.
    # Choices are always one above their place in the index so that choice
    # is never false if it's provided.
    choice = Integer(scope=Scope.user_state, help="The student's answer")

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
        # TODO: Cache this.
        tally = [{'count': 0, 'answer': answer, 'top': False}
                 for answer in self.answers
        ]
        total = 0
        for key, value in self.tally.items():
            key, value = int(key), int(value)
            tally[key - 1]['count'] = value
            total += value

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
            context = Context()

        js_template = self.resource_string(
            '/static/handlebars/results.handlebars')

        context.update({
            'choice': self.choice,
            # Offset so choices will always be True.
            'answers': zip(range(1, len(self.answers) + 1), self.answers),
            'question': self.question,
            'js_template': js_template,
        })

        if self.choice:
            context.update({'tally': self.tally_detail()})

        html = self.resource_string("static/html/poll.html")
        html = Template(html).render(context)
        frag = Fragment(html)
        frag.add_css(self.resource_string("static/css/poll.css"))
        frag.add_javascript(self.resource_string("static/js/vendor/handlebars.js"))
        frag.add_javascript(self.resource_string("static/js/src/poll.js"))
        frag.initialize_js('PollBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def vote(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        result = {'result': 'error'}
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
            choice = int(choice)
            self.answers[choice]
        except (IndexError, ValueError):
            result['message'] = 'No index "{choice}" in answers list.'.format(choice=choice)
            return result

        self.choice = choice
        self.tally[choice - 1] += 1
        result['result'] = 'success'

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