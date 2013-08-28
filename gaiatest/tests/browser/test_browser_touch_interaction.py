# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By

from gaiatest import GaiaTestCase
from gaiatest.apps.browser.app import Browser


class TestBrowserTouchInteraction(GaiaTestCase):

    URL = 'http://mozqa.com/data/firefox/form_manager/form.html'

    _form_locator = (By.CSS_SELECTOR, 'form')

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()

    def test_browser_touch_interaction(self):
        browser = Browser(self.marionette)
        browser.launch()

        browser.go_to_url(self.URL)
