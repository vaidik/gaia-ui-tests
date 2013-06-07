# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest import GaiaTestCase
from gaiatest.apps.marketplace.app import Marketplace
from gaiatest.apps.marketplace.regions.app_details import App
from gaiatest.mocks.persona_test_user import PersonaTestUser


class TestMarketplaceStartAppPurchase(GaiaTestCase):

    _APP_NAME = 'Private Yacht'

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

    # TODO: according to the issue do we need to test if user is not registered
    # at the time of purchasing the app and persona is first taking the user
    # through account creation stuff or not?

    def test_marketplace_start_app_purchase(self):
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

        # search for a paid app and tap on the price
        search = marketplace.search(self._APP_NAME)

        # go to the details page
        search.search_results[0].root_element.tap()
        app_details = App(self.marionette)

        # click on the purchase button to initiate the process
        bango = app_details.tap_purchase_button()

        # switch to bango frame and that's it
        bango.switch_to_bango_frame()
