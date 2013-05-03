# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.marketplace.app import Marketplace
from gaiatest.mocks.persona_test_user import PersonaTestUser


class TestMarketplacePurchaseApp(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()
        self.install_marketplace()

        # generate unverified PersonaTestUser account
        self.user = PersonaTestUser().create_user()

    def test_marketplace_purchase_app(self):

        marketplace = Marketplace(self.marionette, 'Marketplace dev')
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
        import time
        time.sleep(2)

        # return to Marketplace homepage
        marketplace = settings.tap_back()

        # search for a paid app and tap on the price
        search = marketplace.search('Private Yacht')
        bango = search.search_results[0].tap_price()

        # pay app
        bango.make_payment(pin='1234', phone_number=self.testvars['this_phone_number'], country="United Kingdom", network='Three')
