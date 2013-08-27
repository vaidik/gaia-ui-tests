# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import SkipTest

from gaiatest.mocks.mock_email import MockEmail
from gaiatest.tests.email.test_receive_active_sync_email import (
    BaseTestReceiveActiveSyncEmail)
from gaiatest.utils.email.email_util import EmailUtil


class TestReceiveOutlookActiveSyncEmail(BaseTestReceiveActiveSyncEmail):

    def setUp(self):
        try:
            self.testvars['email']['Outlook']
        except KeyError:
            raise SkipTest('Outlook account details not present in test '
                           'variables')

        BaseTestReceiveActiveSyncEmail.setUp(
            self, self.testvars['email']['Outlook'])

    def test_receive_outlook_active_sync_email(self):
        BaseTestReceiveActiveSyncEmail._test_receive_active_sync_email(
            self, wait_timeout=300)
