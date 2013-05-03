# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base


class Payments(Base):

    _payment_frame_locator = ('css selector', "iframe.screen[data-url*='mozpay']")
    _beginning_payment_locator = ('id', 'begin')
    _enter_pin_locator = ('id', 'enter-pin')
    _current_pin_box_locator = ('css selector', 'div.pinbox span.current')
    _continue_button_locator = ('css selector', '#pin > footer > button')

    _reverify_locator = ('css selector', "body[data-verify-url*='reverify']")

    _mobile_number_locator = ('id', 'msisdn')
    _mobile_network_select_locator = ('id', 'contentHolder_uxContent_uxDdlNetworks')

    def switch_to_payments_frame(self):
        self.wait_for_element_present(*self._payment_frame_locator)
        payment_iframe = self.marionette.find_element(*self._payment_frame_locator)
        self.marionette.switch_to_frame(payment_iframe)

    def wait_for_payments_to_begin_not_displayed(self):
        self.wait_for_element_not_displayed(*self._beginning_payment_locator)

    def wait_for_enter_pin_displayed(self):
        self.wait_for_element_displayed(*self._enter_pin_locator)

    def wait_for_reverify_pin_displayed(self):
        self.wait_for_element_displayed(*self._reverify_locator)

    def wait_for_mobile_number_displayed(self):
        self.wait_for_element_displayed(*self._mobile_number_locator)

    def tap_first_pin_number(self):
        self.marionette.find_element('css selector', 'div.pinbox span.current').click()

    def tap_continue(self):
        self.marionette.find_element('css selector', '#pin>footer>button').click()

    def select_country(self, value):
        pass
        # country_select = self.marionette.find_element(*)
        # country_select.click()
        # self.select(value)

    def type_mobile_number(self, value):
        mobile_number = self.marionette.find_element(*self._mobile_number_locator)
        mobile_number.send_keys(value)

    def select_mobile_network(self, value):
        mobile_network = self.marionette.find_element(*self._mobile_network_select_locator)
        mobile_network.click()
        self.select(value)
