# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By

from gaiatest import GaiaTestCase
from gaiatest.apps.browser.app import Browser


class TestBrowserTouchInteraction(GaiaTestCase):

    URL = 'http://mozqa.com/data/firefox/form_manager/form.html'

    _textbox_locator = (By.ID, 'ship_fname')
    _submit_button_locator = (By.ID, 'SubmitButton')

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()

    def test_browser_touch_interaction(self):
        browser = Browser(self.marionette)
        browser.launch()

        # Have to do it this way because of bug 829514
        self.marionette.execute_script(
            "return window.wrappedJSObject.Browser.navigate('%s');" % self.URL)
        browser.switch_to_content()

        self.marionette.find_element(*self._textbox_locator).send_keys('xyz')

        self.marionette.find_element(*self._submit_button_locator).tap()

        self.wait_for_condition(
            lambda m: m.find_element(*self._textbox_locator).is_displayed)

        self.assertEqual(
            self.marionette.find_element(
                *self._textbox_locator).get_attribute('value'), '')
