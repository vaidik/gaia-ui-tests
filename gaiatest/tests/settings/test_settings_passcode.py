# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestSettingsPasscode(GaiaTestCase):

    # Input data
    _input_passcode = ['7', '9', '3', '1']

    # Passcode Settings locators
    _phonelock_menu_item_locator = ('id', 'menuItem-phoneLock')
    _phonelock_section_locator = ('id', 'phoneLock')
    _passcode_enable_locator = ('css selector', 'li.lockscreen-enabled label')
    _phonelock_passcode_section_locator = ('id', 'phoneLock-passcode')
    _passcode_create_locator = ('id', 'passcode-create')

    def setUp(self):

        GaiaTestCase.setUp(self)

        # Enable lock screen
        self.data_layer.set_setting('lockscreen.enabled', True)
        # launch the Settings app
        self.app = self.apps.launch('Settings')

    def test_set_passcode_by_settings(self):
        """ Set a passcode using Settings app

        https://github.com/mozilla/gaia-ui-tests/issues/477

        """
        # navigate to phone lock settings
        self.wait_for_element_displayed(*self._phonelock_menu_item_locator)
        phonelock_menu_item = self.marionette.find_element(*self._phonelock_menu_item_locator)
        # TODO bug 878017 - remove the explicit scroll once bug is fixed
        self.marionette.execute_script("arguments[0].scrollIntoView(false);", [phonelock_menu_item])
        phonelock_menu_item.tap()

        # enable passcode
        self.wait_for_element_displayed(*self._phonelock_section_locator)
        passcode_enable_item = self.marionette.find_element(*self._passcode_enable_locator)
        # TODO Tap one pixel above bottom edge to dodge the System update notification banner bug 879192
        passcode_enable_item.tap(y=(passcode_enable_item.size['height'] - 1))

        # switch to keyboard, input passcode
        self.wait_for_element_displayed(*self._phonelock_passcode_section_locator)
        self.keyboard.switch_to_keyboard()
        for times in range(2):
            self.keyboard.send("".join(self._input_passcode))

        # switch to settings frame
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.app.frame)

        # create passcode
        self.wait_for_element_displayed(*self._phonelock_passcode_section_locator)
        passcode_create = self.marionette.find_element(*self._passcode_create_locator)

        passcode_create.tap()
        self.wait_for_element_displayed(*self._phonelock_section_locator)

        # assert
        passcode_code = self.data_layer.get_setting('lockscreen.passcode-lock.code')
        passcode_enabled = self.data_layer.get_setting('lockscreen.passcode-lock.enabled')
        self.assertEqual(passcode_code, "".join(self._input_passcode), 'Passcode is "%s", not "%s"' % (passcode_code, "".join(self._input_passcode)))
        self.assertEqual(passcode_enabled, True, 'Passcode is not enabled.')

    def tearDown(self):
        # switch to settings frame
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.app.frame)

        # disable passcode
        self.data_layer.set_setting('lockscreen.passcode-lock.code', '1111')
        self.data_layer.set_setting('lockscreen.passcode-lock.enabled', False)
