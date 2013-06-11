# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest import GaiaTestCase
from gaiatest.apps.marketplace.app import Marketplace
from gaiatest.apps.marketplace.regions.app_details import App
from gaiatest.mocks.persona_test_user import PersonaTestUser


class TestMarketplaceEnterValidPin(GaiaTestCase):

    _APP_NAME = 'Private Yacht'

    _cancel_sms_pin_button_locator = ('id', 'contentHolder_uxContent_uxLnkCancel')
    _incorrect_pin_error_holder = ('css selector', 'p.error-msg')

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

        # purchase the app
        bango = search.search_results[0].tap_purchase_button()

        # create pin workflow
        bango.wait_for_enter_id_pin_section_displayed()

        # tap and enter the pin for the first time
        bango.type_id_pin_number('1234')
        bango.tap_confirm_id_pin_continue()
        bango.wait_for_confirm_id_pin_section_displayed()

        # enter the pin code for the second time
        bango.type_id_pin_number('1234')
        bango.tap_confirm_id_pin_continue()

        # wait for the phone number and network form
        bango.wait_for_confirm_number_section_displayed()

        # now cancel PIN confirmation because we don't need it right now
        self.marionette.find_element(*self._cancel_sms_pin_button_locator).tap()
        time.sleep(1)
        self.apps.kill_all()

    def test_marketplace_enter_valid_pin(self):
        marketplace = Marketplace(self.marionette, 'Marketplace Dev')
        marketplace.launch()

        # search for a paid app and tap on the price
        search = marketplace.search(self._APP_NAME)

        # click on the purchase button to initiate the process
        bango = search.search_results[0].tap_purchase_button()

        # wait for enter pin screen
        bango.wait_for_verify_id_pin_section_displayed()

        # enter valid pin
        bango.type_id_pin_number('1234')

        # continue for PIN verification
        bango.tap_confirm_id_pin_continue()

        # wait for bango's confirm screen
        bango.wait_for_confirm_number_section_displayed()

        # confirm if the next screen is the mobile number confirmation screen.
        self.assertEqual(self.marionette.title, 'Confirm Your Mobile Number',
                         'Mobile confirmation screen from Bango did not load.')

    def test_marketplace_enter_invalid_pin(self):
        marketplace = Marketplace(self.marionette, 'Marketplace Dev')
        marketplace.launch()

        # search for a paid app and tap on the price
        search = marketplace.search(self._APP_NAME)

        # click on the purchase button to initiate the process
        bango = search.search_results[0].tap_purchase_button()
        
        # wait for enter pin screen
        bango.wait_for_verify_id_pin_section_displayed()

        # enter invalid pin
        bango.type_id_pin_number('1111')

        # continue for PIN verification
        bango.tap_confirm_id_pin_continue()

        # i don't know what to wait for here. :(
        time.sleep(4)

        # error message element
        error = self.marionette.find_element(*self._incorrect_pin_error_holder)

        # confirms that the PIN is incorrect
        self.assertEqual(error.text, 'Wrong pin')
