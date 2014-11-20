from xblockutils.base_test import SeleniumBaseTest


class PollBaseTest(SeleniumBaseTest):
    default_css_selector = 'div.poll-block'
    module_name = __name__