"""
Test to make sure the layout for results is sane when taking images into
account.
"""
from tests.integration.base_test import PollBaseTest
import time


class TestLayout(PollBaseTest):
    """
    Do tests to verify that the layout of elements makes sense depeneding on
    the number of images.
    """

    def test_all_images(self):
        """
        Verify img tags are created for answers when they're all set.
        """
        self.go_to_page('All Pictures')
        pics = self.browser.find_elements_by_css_selector('.poll-image')
        self.assertEqual(len(pics), 4)

        # Pics should be within labels.
        pics[0].find_element_by_css_selector('img').click()
        self.get_submit().click()

        self.wait_until_exists('.poll-image')

        self.assertEqual(len(self.browser.find_elements_by_css_selector('.poll-image')), 4)

    def test_one_image(self):
        """
        Verify layout is sane when only one answer has an image.
        """
        self.go_to_page('One Picture')
        pics = self.browser.find_elements_by_css_selector('.poll-image')
        # On the polling page, there should only be one pics div.
        self.assertEqual(len(pics), 1)

        pics[0].find_element_by_css_selector('img').click()

        self.get_submit().click()

        self.wait_until_exists('.poll-image.result-image')
        # ...But on the results page, we need four, for table layout.
        self.assertEqual(len(self.browser.find_elements_by_css_selector('.poll-image')), 4)