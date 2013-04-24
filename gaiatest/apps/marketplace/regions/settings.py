# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion


class Settings(Base):

    _email_account_field_locator = ('id', 'email')
    _save_locator = ('css selector', '.form-footer.c > button')
    _sign_in_button_locator = ('css selector', 'a.button.browserid')
    _sign_out_button_locator = ('css selector', 'a.button.logout')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_element_displayed(*self._save_locator)

    def wait_for_sign_in_displayed(self):
        self.wait_for_element_displayed(*self._sign_in_button_locator)

    def tap_sign_in(self):
        # TODO: click works but not tap
        self.marionette.find_element(*self._sign_in_button_locator).click()
        from gaiatest.apps.persona.app import Persona
        return Persona(self.marionette)

    def wait_for_sign_out_button(self):
        self.wait_for_element_displayed(*self._sign_out_button_locator)

    def tap_sign_out(self):
        sign_out_button = self.marionette.find_element(*self._sign_out_button_locator)
        # TODO: click works but not tap
        sign_out_button.click()

    @property
    def email(self):
        return self.marionette.find_element(*self._email_account_field_locator).get_attribute('value')
