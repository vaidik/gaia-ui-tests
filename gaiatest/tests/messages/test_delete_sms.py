# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time
from gaiatest.apps.messages.app import Messages


class TestDeleteSms(GaiaTestCase):
    _text_message_content = "Automated Test %s" % str(time.time())

    def test_delete_sms(self):

        # launch the app
        self.messages = Messages(self.marionette)
        self.messages.launch()

        # click new message
        new_message = self.messages.tap_create_new_message()
        new_message.type_phone_number(self.testvars['carrier']['phone_number'])

        new_message.type_message(self._text_message_content)

        # click send
        self.message_thread = new_message.tap_send()
        self.message_thread.wait_for_received_messages()

        # tap edit button
        self.messages.tap_edit()

        # get the most recent listed and most recent received text message
        last_received_message = self.message_thread.received_messages[-1]

        # select the message
        last_received_message.select_message()

        # check that the message was selected
        self.assertEqual(self.messages.selected_messages, 1)

        # delete selected messages
        self.messages.tap_delete_selected()

        # say yes in the alert but the step before this is blocking
        # tap the Delete button in the alert and the test will move to the next
        # statement.
        import pdb; pdb.set_trace()

        # verify that the message was deleted
        self.assertEqual(len(self.message_thread.received_messages), 0)
