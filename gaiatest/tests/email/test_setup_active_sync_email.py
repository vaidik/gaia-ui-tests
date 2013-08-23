# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import SkipTest

from gaiatest import GaiaTestCase
from gaiatest.apps.email.app import Email


class BaseTestSetupActiveSync(GaiaTestCase):

    def setUp(self, credential):
        self.credentials = credential
        GaiaTestCase.setUp(self)
        self.connect_to_network()

    def _test_setup_active_sync_email(self):
        # setup ActiveSync account

        self.email = Email(self.marionette)
        self.email.launch()

        self.email.setup_active_sync_email(self.credentials)

        # check header area
        self.assertTrue(self.email.header.is_compose_visible)
        self.assertTrue(self.email.header.is_menu_visible)
        self.assertEqual(self.email.header.label, 'Inbox')

        # check toolbar area
        self.assertTrue(self.email.toolbar.is_edit_visible)
        self.assertTrue(self.email.toolbar.is_refresh_visible)

        # wait for sync to complete
        self.email.wait_for_emails_to_sync()
