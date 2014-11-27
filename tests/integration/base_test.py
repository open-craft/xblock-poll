from xblockutils.base_test import SeleniumBaseTest


class PollBaseTest(SeleniumBaseTest):
    default_css_selector = 'div.poll-block'
    module_name = __name__

    def get_submit(self):
        return self.browser.find_element_by_css_selector('input[name="poll-submit"]')