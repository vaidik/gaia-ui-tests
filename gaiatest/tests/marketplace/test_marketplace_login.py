# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.marketplace.app import Marketplace


class TestMarketplaceLogin(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()

        self.marketplace = Marketplace(self.marionette)
        self.marketplace.launch()

        # Switch to marketplace iframe
        self.marketplace.switch_to_marketplace_frame()

    def test_login_marketplace(self):
        # https://moztrap.mozilla.org/manage/case/4134/

        self.marketplace.wait_for_setting_displayed()
        settings = self.marketplace.tap_settings()
        persona = settings.tap_sign_in()

        persona.login(self.testvars['marketplace']['username'], self.testvars['marketplace']['password'])

        # switch back to Marketplace
        self.marionette.switch_to_frame()
        self.marketplace.launch()
        self.marketplace.switch_to_marketplace_frame()

        # self.marketplace.wait_for_signed_in_notification()
        # self.marketplace.tap_signed_in_notification()

        settings.wait_for_sign_out_button()

        # Verify that user is logged in
        self.assertEqual(self.testvars['marketplace']['username'], settings.email)

        # Sign out, which should return to the Marketplace home screen
        settings.tap_sign_out()

        # Verify that user is signed out
        self.marketplace.wait_for_setting_displayed()
        settings = self.marketplace.tap_settings()
        settings.wait_for_sign_in_displayed()
