from ddt import ddt, unpack, data
from selenium.common.exceptions import NoSuchElementException
from base_test import PollBaseTest


scenarios = ('Survey Private', ['enjoy', 'recommend', 'learn']), ('Poll Private', ['choice'])

@ddt
class TestPrivateResults(PollBaseTest):
    """
    Check the functionality of private results.
    """

    def make_selections(self, names):
        """
        Selects the first option for each named input.
        """
        for name in names:
            self.browser.find_element_by_css_selector('input[name="%s"]' % name).click()

    def do_submit(self, names):
        """
        Do selection and submit.
        """
        self.make_selections(names)
        submit = self.get_submit()
        submit.click()
        self.wait_until_clickable(self.browser.find_element_by_css_selector('.poll-voting-thanks'))

    @unpack
    @data(*scenarios)
    def test_form_remains(self, page_name, names):
        """
        User should still have a form presented after submitting so they can resubmit.
        """
        self.go_to_page(page_name)
        # Form should be there to begin with, of course.
        self.browser.find_element_by_css_selector('div.poll-block form')
        self.do_submit(names)

    @unpack
    @data(*scenarios)
    def test_no_results(self, page_name, names):
        """
        The handlebars template for results should never be called, and the form should persist.
        """
        self.go_to_page(page_name)
        self.do_submit(names)

        # No results should be showing.
        self.assertNotIn(self.browser.find_element_by_css_selector('div.poll-block').get_attribute('innerHTML'), 'poll-top-choice')
        self.assertRaises(NoSuchElementException, self.browser.find_element_by_css_selector, '.poll-footnote')

    @unpack
    @data(*scenarios)
    def test_submit_button(self, page_name, names):
        self.go_to_page(page_name)
        submit = self.get_submit()
        self.assertIn('Submit', submit.get_attribute('outerHTML'))

        self.make_selections(names)
        submit.click()
        self.wait_until_clickable(self.browser.find_element_by_css_selector('.poll-voting-thanks'))

        self.assertIn('Resubmit', submit.get_attribute('outerHTML'), 'Resubmit')

        # This should persist on page reload.
        self.go_to_page(page_name)
        submit = self.get_submit()
        self.assertIn('Resubmit', submit.get_attribute('outerHTML'), 'Resubmit')

    @unpack
    @data(*scenarios)
    def test_feedback_display(self, page_name, names):
        self.go_to_page(page_name)
        self.assertFalse(self.browser.find_element_by_css_selector('.poll-feedback').is_displayed())
        self.do_submit(names)
        self.assertTrue(self.browser.find_element_by_css_selector('.poll-feedback').is_displayed())
