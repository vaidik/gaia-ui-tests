# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import SkipTest

from gaiatest.tests.email.test_setup_active_sync_email import (
    BaseTestSetupActiveSync)


class TestSetupHostedActiveSync(BaseTestSetupActiveSync):

    def setUp(self):
        try:
            self.testvars['email']['ActiveSync']
        except KeyError:
            raise SkipTest('account details not present in test variables')

        BaseTestSetupActiveSync.setUp(self,
                                      self.testvars['email']['ActiveSync'])

    def test_setup_hosted_active_sync_email(self):
        BaseTestSetupActiveSync._test_setup_active_sync_email(self)
