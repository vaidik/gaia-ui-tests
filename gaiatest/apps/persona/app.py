# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base


class Persona(Base):
    # Trusty UI on home screen
    _tui_container_locator = ('id', 'trustedui-frame-container')

    # iframes
    _persona_frame_locator = ('css selector', "iframe.screen[data-url*='persona.org']")

    # persona login
    _waiting_locator = ('css selector', 'body.waiting')
    _email_input_locator = ('id', 'authentication_email')
    _password_input_locator = ('id', 'authentication_password')
    _next_button_locator = ('css selector', 'button.start')
    _returning_button_locator = ('css selector', 'button.returning')
    _sign_in_button_locator = ('id', 'signInButton')
    _this_session_only_button_locator = ('id', 'this_is_not_my_computer')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.marionette.switch_to_frame()
        self.wait_for_element_present(*self._tui_container_locator)

    def login(self, email, password):
        self._switch_to_persona_frame()

        # this is necessary because we can't have a clean profile every time we log in
        if self.is_element_displayed(*self._email_input_locator):
            # self.wait_for_element_displayed(*self._email_input_locator)
            self._email(email)
            self._tap_next()
            self.wait_for_element_displayed(*self._password_input_locator)
            self._password(password)
            self._tap_returning()
        else:
            self.wait_for_element_displayed(*self._sign_in_button_locator)
            self._tap_sign_in()
            # Sometimes it prompts for "Remember Me?"
            # If it does, tell it to remember you for this session only
            # TODO: Find out actual logic behind when it prompts or not
            try:
                self.wait_for_element_displayed(*self._this_session_only_button_locator)
                self._tap_this_session_only()
            except:
                pass

    def _switch_to_persona_frame(self):
        self.wait_for_element_present(*self._persona_frame_locator)
        persona_iframe = self.marionette.find_element(*self._persona_frame_locator)
        self.marionette.switch_to_frame(persona_iframe)

        self.wait_for_element_not_present(*self._waiting_locator)

    def _email(self, value):
        email_field = self.marionette.find_element(*self._email_input_locator)
        email_field.send_keys(value)

    def _password(self, value):
        password_field = self.marionette.find_element(*self._password_input_locator)
        password_field.send_keys(value)

    def _tap_next(self):
        next_button = self.marionette.find_element(*self._next_button_locator)
        # TODO:  Remove workaround after bug 845849
        self.marionette.execute_script("arguments[0].scrollIntoView(false);", [next_button])
        self.marionette.tap(next_button)

    def _tap_sign_in(self):
        self.marionette.tap(self.marionette.find_element(*self._sign_in_button_locator))

    def _tap_returning(self):
        self.marionette.tap(self.marionette.find_element(*self._returning_button_locator))

    def _tap_this_session_only(self):
        self.marionette.tap(self.marionette.find_element(*self._this_session_only_button_locator))
