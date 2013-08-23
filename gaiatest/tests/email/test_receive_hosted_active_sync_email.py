# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import SkipTest

from gaiatest.apps.email.app import Email
from gaiatest.mocks.mock_email import MockEmail
from gaiatest.tests.email.test_receive_active_sync_email import (
    BaseTestReceiveActiveSyncEmail)
from gaiatest.utils.email.email_util import EmailUtil


class TestReceiveHostedActiveSyncEmail(BaseTestReceiveActiveSyncEmail):

    def setUp(self):
        try:
            self.testvars['email']['ActiveSync']
        except KeyError:
            raise SkipTest('ActiveSync account details not present in test '
                           'variables')

        BaseTestReceiveActiveSyncEmail.setUp(
            self, self.testvars['email']['ActiveSync'])

    def test_receive_hosted_active_sync_email(self):
        BaseTestReceiveActiveSyncEmail._test_receive_active_sync_email(self)
