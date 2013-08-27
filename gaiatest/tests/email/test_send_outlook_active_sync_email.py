# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import SkipTest

from gaiatest.tests.email.test_send_active_sync_email import (
    BaseTestSendActiveSyncEmail)


class TestSendOutlookActiveSyncEmail(BaseTestSendActiveSyncEmail):

    def setUp(self):
        try:
            account = self.testvars['email']['Outlook']
        except KeyError:
            raise SkipTest('account details not present in test variables')

        BaseTestSendActiveSyncEmail.setUp(self,
                                          self.testvars['email']['Outlook'])

    def test_send_outlook_active_sync_email(self):
        BaseTestSendActiveSyncEmail._test_send_active_sync_email(
            self, wait_timeout=300)
