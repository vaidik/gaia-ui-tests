# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
import time
import re


class Bango(Base):

    _payment_frame_locator = ('css selector', "div#trustedui-frame-container > iframe")


    _beginning_payment_locator = ('id', 'begin')
    # 4-digit password pin number
    _enter_pin_locator = ('id', 'enter-pin')

    # Enter/confirm PIN
    _enter_pin_section_locator = ('css selector', 'form[action="/mozpay/pin/create"]')
    _confirm_pin_section_locator = ('css selector', 'form[action="/mozpay/pin/confirm"]')

    _current_pin_box_locator = ('css selector', 'div.pinbox span.current')
    _confirm_pin_continue_button_locator = ('css selector', '#pin > footer > button')

    # Enter mobile network/number/country locators
    _number_section_locator = ('id', 'numberSection')
    _mobile_number_locator = ('id', 'msisdn')
    _mobile_network_select_locator = ('id', 'contentHolder_uxContent_uxDdlNetworks')
    _change_country_link_locator = ('id', 'contentHolder_uxContent_uxRegionSelection_uxRegionChangeLnk')
    _country_select_list_locator = ('id', 'contentHolder_uxContent_uxRegionSelection_uxUlCountries')
    _mobile_section_continue_button_locator = ('id', 'contentHolder_uxContent_uxLnkContinue')

    # Pin received from SMS message
    _pin_section_locator = ('id', 'pinSection')
    _pin_input_locator = ('id', 'pin')
    _confirm_sms_pin_button_locator = ('id', 'contentHolder_uxContent_uxLnkConfirm')


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

        # create pin workflow
        self.wait_for_enter_pin_section_displayed()

        # tap and enter the pin for the first time
        self.tap_first_pin_number()
        keyboard.send(pin)

        # switch back to app
        self.switch_to_bango_frame()
        self.tap_confirm_pin_continue()
        self.wait_for_confirm_pin_section_displayed()

        # enter the pin code for the second time
        self.tap_first_pin_number()
        keyboard.send(pin)

        # switch back to app
        self.switch_to_bango_frame()
        self.tap_confirm_pin_continue()

        # wait for the phone number and network form
        self.wait_for_confirm_number_section_displayed()

        # Select the country first otherwise it clears the other fields
        self.tap_change_country()
        self.select_country(country)

        # Enter the phone number
        self.type_mobile_number("07449159596")

        # Choose the mobile network
        self.select_mobile_network(network)

        self.tap_mobile_section_continue_button()

        # Switch to System frame and wait for the SMS to arrive.
        self.marionette.switch_to_frame()
        _notification_toaster_locator = ('id', 'notification-toaster')
        notification_toaster = self.marionette.find_element(*_notification_toaster_locator)

        # TODO Re-enable this when Bug 861874
        # self.wait_for_element_displayed(*self._notification_toaster_locator)
        self.wait_for_condition(lambda m: notification_toaster.location['y'] == 0, timeout=180)

        m = re.search("PIN: ([0-9]+).", notification_toaster.text)
        pin_number = m.group(1)

        self.switch_to_bango_frame()

        self.wait_for_sms_pin_section_displayed()

        self.enter_sms_pin(pin_number)
        self.tap_confirm_sms_pin_button()

        time.sleep(2)

        # Hack to get scrollbar back into view
        self.marionette.switch_to_frame()
        self.marionette.execute_script("document.getElementById('statusbar').scrollIntoView();")
        self.switch_to_bango_frame()

        # Not sure what I'm waiting for here just yet.



    def wait_for_enter_pin_section_displayed(self):
        self.wait_for_element_displayed(*self._enter_pin_section_locator)

    def wait_for_confirm_pin_section_displayed(self):
        self.wait_for_element_displayed(*self._confirm_pin_section_locator)

    def wait_for_confirm_number_section_displayed(self):
        self.wait_for_element_displayed(*self._number_section_locator)

    def wait_for_sms_pin_section_displayed(self):
        self.wait_for_element_displayed(*self._pin_section_locator)

    def tap_first_pin_number(self):
        self.marionette.find_element(*self._current_pin_box_locator).click()

    def tap_confirm_pin_continue(self):
        self.marionette.find_element(*self._confirm_pin_continue_button_locator).click()

    def tap_change_country(self):
        self.marionette.tap(self.marionette.find_element(*self._change_country_link_locator))
        self.wait_for_element_displayed(*self._country_select_list_locator)

    def select_country(self, value):
        country_select = self.marionette.find_element('link text', value)
        country_select.click()
        self.wait_for_element_not_displayed(*self._country_select_list_locator)

    def type_mobile_number(self, value):
        mobile_number_input = self.marionette.find_element(*self._mobile_number_locator)
        mobile_number_input.send_keys(value)

        # Hit a dummy element to break focus from the input
        self.marionette.find_element(*self._number_section_locator).click()

    def select_mobile_network(self, network):
        mobile_network = self.marionette.find_element(*self._mobile_network_select_locator)
        mobile_network.click()
        self.marionette.switch_to_frame()

        select_locator = ("xpath", "//section[@id='value-selector-container']//li[label[span[text()='%s']]]" % network)

        self.wait_for_element_present(*select_locator)
        element = self.marionette.find_element(*select_locator)
        element.click()

        close_button = self.marionette.find_element('css selector', 'button.value-option-confirm')
        self.marionette.tap(close_button)

        self.switch_to_bango_frame()

    def tap_mobile_section_continue_button(self):
        self.marionette.find_element(*self._mobile_section_continue_button_locator).click()

    def enter_sms_pin(self, sms_pin_number):
        pin_input = self.marionette.find_element(*self._pin_input_locator)
        pin_input.click()
        pin_input.send_keys(sms_pin_number)

        # Hit a dummy element to break focus from the input
        self.marionette.find_element(*self._pin_section_locator).click()

    def tap_confirm_sms_pin_button(self):
        self.marionette.find_element(*self._confirm_sms_pin_button_locator).click()
