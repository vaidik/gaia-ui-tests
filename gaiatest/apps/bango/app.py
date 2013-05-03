# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from gaiatest.apps.persona.regions.payments import Payments


class Bango(Base):


    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.marionette.switch_to_frame()
        payments.switch_to_payments_frame()

    def payments(self, pin, phone_number, country, network):
        from gaiatest.apps.keyboard.app import Keyboard
        keyboard = Keyboard(self.marionette)
        payments = Payments(self.marionette)

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
        payments.wait_for_mobile_number_displayed()

        # add the phone number and network information
        payments.mobile_number(phone_number)

        # Select the country first otherwise it clears the other fields

        # Choose the mobile network
        payments.select_mobile_network(network)

        # TO BE CONTINUED
