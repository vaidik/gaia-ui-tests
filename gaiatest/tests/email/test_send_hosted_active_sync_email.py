# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from marionette import SkipTest

from gaiatest.apps.email.app import Email
from gaiatest.tests.email.test_send_active_sync_email import (
    BaseTestSendActiveSyncEmail)


class TestSendHostedActiveSyncEmail(BaseTestSendActiveSyncEmail):

    def setUp(self):
        try:
            account = self.testvars['email']['ActiveSync']
        except KeyError:
            raise SkipTest('account details not present in test variables')

        BaseTestSendActiveSyncEmail.setUp(self,
                                          self.testvars['email']['ActiveSync'])

    def test_send_hosted_active_sync_email(self):
        BaseTestSendActiveSyncEmail._test_send_active_sync_email(self)
