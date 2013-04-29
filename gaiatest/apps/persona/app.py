# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from gaiatest.apps.persona.regions.payments import Payments
from gaiatest.apps.persona.regions.login import Login


class Persona(Base):

    # Trusty UI on home screen
    _tui_container_locator = ('id', 'trustedui-frame-container')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.marionette.switch_to_frame()
        self.wait_for_element_present(*self._tui_container_locator)

    def payments(self, pin, phone_number, network):
        from gaiatest.apps.keyboard.app import Keyboard
        keyboard = Keyboard(self.marionette)

        payments = Payments(self.marionette)
        payments.switch_to_payments_frame()

        # wait for the pin code form
        payments.wait_for_payments_to_begin_not_displayed()
        payments.wait_for_enter_pin_displayed()

        # create pin workflow
        # tap and enter the pin for the first time
        payments.tap_first_pin_number()
        keyboard.send(pin)

        # switch back to app
        payments.switch_to_payments_frame()
        payments.tap_continue()

        # enter the pin code for the second time
        payments.wait_for_reverify_pin_displayed()
        payments.tap_first_pin_number()
        keyboard.send(pin)

        # switch back to app
        payments.switch_to_payments_frame()
        payments.tap_continue()

        # wait for the phone number and network form
        payments.wait_for_mobile_number_displayed

        # add the phone number and network information
        payments.mobile_number(phone_number)
        payments.select_mobile_network(network)

        # TO BE CONTINUED

    def login(self, email, password):
        login = Login(self.marionette)

        login.switch_to_persona_frame()

        # This is a hack until we are able to run test with a clean profile
        # if a user was logged in tap this is not me
        if login.form_section_id == "selectEmail":
            login.wait_for_sign_in_button()
            login.tap_this_is_not_me()

        # this is necessary because we can't have a clean profile every time we log in
        if login.form_section_id == 'authentication_form':
            login.wait_for_email_input()
            login.type_email(email)
            login.tap_next()
            # if we login with an unverified user we have to confirm the password
            if login.form_section_id == "authentication_form":
                login.wait_for_password_input()
                login.type_password(password)
                login.tap_returning()
            elif login.form_section_id == "set_password":
                login.type_create_password(password)
                login.type_confirm_password(password)
                login.tap_verify_user()
