# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest import GaiaTestCase
from gaiatest.apps.marketplace.app import Marketplace
from gaiatest.apps.system.app import System
from gaiatest.mocks.persona_test_user import PersonaTestUser


class TestMarketplacePurchaseAppCreditCard(GaiaTestCase):

    _APP_NAME = 'Private Yacht'
    _app_icon_locator = ('xpath', "//li[@class='icon']//span[text()='%s']" % _APP_NAME)

    _homescreen_iframe_locator = ('css selector', 'div.homescreen iframe')

    def setUp(self):
        GaiaTestCase.setUp(self)

        if self.apps.is_app_installed(self._APP_NAME):
            self.apps.uninstall(self._APP_NAME)

        self.data_layer.connect_to_wifi()
        self.install_marketplace()

        # generate unverified PersonaTestUser account
        self.user = PersonaTestUser().create_user(verified=True, env={
            "browserid": "firefoxos.persona.org",
            "verifier": "marketplace-dev.allizom.org"})

    def test_marketplace_purchase_app_credit_card(self):

        marketplace = Marketplace(self.marionette, 'Marketplace Dev')
        marketplace.launch()

        # Tap settings and sign in in Marketplace
        settings = marketplace.tap_settings()
        persona = settings.tap_sign_in()

        # login with PersonaTestUser account
        persona.login(self.user.email, self.user.password)

        # switch back to Marketplace
        self.marionette.switch_to_frame()
        marketplace.launch()

        # wait for the page to refresh and the sign out button to be visible
        settings.wait_for_sign_out_button()

        # Well I dunno, it just needs this
        time.sleep(3)

        settings.select_region("Spain")

        time.sleep(3)

        settings.tap_save_changes()

        # search for a paid app and tap on the price
        search = marketplace.search(self._APP_NAME)
        bango = search.search_results[0].tap_purchase_button()

        # pay app
        bango.create_pin('1234')

        # enter credit card details
        bango.pay_using_credit_card(self.testvars['credit_card']['number'],
                                    self.testvars['credit_card']['expiry'],
                                    self.testvars['credit_card']['cvv'])
        self.marionette.switch_to_frame()

        # At gaia System level, complete the installation prompt
        System(self.marionette).confirm_app_installation()

        # Switch into homescreen frame
        homescreen_frame = self.marionette.find_element(*self._homescreen_iframe_locator)
        self.marionette.switch_to_frame(homescreen_frame)

        # Not overly concerned about it being visible, only present
        self.assertTrue(self.is_element_present(*self._app_icon_locator))
