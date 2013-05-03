# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
import time


class Bango(Base):

    _payment_frame_locator = ('css selector', "div#trustedui-frame-container > iframe")

    _beginning_payment_locator = ('id', 'begin')
    _enter_pin_locator = ('id', 'enter-pin')
    _current_pin_box_locator = ('css selector', 'div.pinbox span.current')
    _continue_button_locator = ('css selector', '#pin > footer > button')

    _reverify_locator = ('css selector', "body[data-verify-url*='reverify']")

    _mobile_number_locator = ('id', 'msisdn')
    _mobile_network_select_locator = ('id', 'contentHolder_uxContent_uxDdlNetworks')

    _change_country_link_locator = ('id', 'contentHolder_uxContent_uxRegionSelection_uxRegionChangeLnk')
    _country_select_list_locator = ('id', 'contentHolder_uxContent_uxRegionSelection_uxUlCountries')


    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.switch_to_bango_frame()

    def switch_to_bango_frame(self):
        self.marionette.switch_to_frame()
        self.wait_for_element_present(*self._payment_frame_locator)
        payment_iframe = self.marionette.find_element(*self._payment_frame_locator)
        self.marionette.switch_to_frame(payment_iframe)


    def make_payment(self, pin, phone_number, country, network):
        '''
        A helper method to complete all of the payment steps
        '''
        from gaiatest.apps.keyboard.app import Keyboard
        keyboard = Keyboard(self.marionette)

        # wait for the pin code form
        self.wait_for_payments_to_begin_not_displayed()

        time.sleep(2)
        self.wait_for_enter_pin_displayed()

        # create pin workflow
        # tap and enter the pin for the first time
        self.tap_first_pin_number()
        keyboard.send(pin)

        # switch back to app
        self.switch_to_bango_frame()
        self.tap_continue()

        # enter the pin code for the second time
        self.wait_for_reverify_pin_displayed()
        self.tap_first_pin_number()
        keyboard.send(pin)

        # switch back to app
        self.switch_to_bango_frame()
        self.tap_continue()

        # wait for the phone number and network form
        self.wait_for_mobile_number_displayed()

        # print self.marionette.page_source

        # Select the country first otherwise it clears the other fields
        self.tap_change_country()
        self.select_country(country)

        time.sleep(2)

        # Enter the phone number
        self.type_mobile_number(phone_number)

        time.sleep(2)

        # Choose the mobile network
        self.select_mobile_network(network)
        time.sleep(2)

        self.marionette.find_element('id', 'contentHolder_uxContent_uxLnkContinue').click()

        time.sleep(5)
        print self.marionette.page_source



    ####################

    def wait_for_payments_to_begin_not_displayed(self):
        self.wait_for_element_not_displayed(*self._beginning_payment_locator)

    def wait_for_enter_pin_displayed(self):
        self.wait_for_element_displayed(*self._enter_pin_locator)

    def wait_for_reverify_pin_displayed(self):
        self.wait_for_element_displayed(*self._reverify_locator)

    def wait_for_mobile_number_displayed(self):
        self.wait_for_element_displayed(*self._mobile_number_locator)

    def tap_first_pin_number(self):
        self.marionette.find_element(*self._current_pin_box_locator).click()

    def tap_continue(self):
        self.marionette.find_element(*self._continue_button_locator).click()

    def tap_change_country(self):
        self.marionette.tap(self.marionette.find_element(*self._change_country_link_locator))
        self.wait_for_element_displayed(*self._country_select_list_locator)

    def select_country(self, value):
        country_select = self.marionette.find_element('link text', value)
        country_select.click()

    def type_mobile_number(self, value):
        mobile_number = self.marionette.find_element(*self._mobile_number_locator)
        mobile_number.send_keys(value)

    def select_mobile_network(self, network):
        mobile_network = self.marionette.find_element(*self._mobile_network_select_locator)
        mobile_network.click()
        self.marionette.switch_to_frame()

        element = self.marionette.find_element(
            "xpath", "//section[@id='value-selector-container']//li[label[span[text()='%s']]]" % network)
        close_button = self.marionette.find_element('css selector', 'button.value-option-confirm')

        element.click()
        self.marionette.tap(close_button)

        self.switch_to_bango_frame()
