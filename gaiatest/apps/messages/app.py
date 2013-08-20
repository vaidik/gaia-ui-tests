# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.base import Base


class Messages(Base):

    name = 'Messages'

    _summary_header_locator = (By.CSS_SELECTOR, "h1[data-l10n-id='messages']")
    _create_new_message_locator = (By.ID, 'icon-add')
    _messages_frame_locator = (By.CSS_SELECTOR, 'iframe[data-frame-origin*=sms]')
    _edit_button_locator = (By.ID, 'messages-edit-icon')
    _delete_selected_button_locator = (By.ID, 'messages-delete-button')
    _selected_messages_text_locator = (By.ID, 'messages-edit-mode')

    def launch(self):
        Base.launch(self)
        self.wait_for_element_displayed(*self._summary_header_locator)

    def tap_edit(self):
        self.marionette.find_element(*self._edit_button_locator).tap()

    def tap_delete_selected(self):
        self.marionette.find_element(*self._delete_selected_button_locator).tap()

    def tap_create_new_message(self):
        self.marionette.find_element(*self._create_new_message_locator).tap()
        from gaiatest.apps.messages.regions.new_message import NewMessage
        return NewMessage(self.marionette)

    def switch_to_messages_frame(self):
        self.marionette.switch_to_frame()
        self.wait_for_element_present(*self._messages_frame_locator)
        messages_frame = self.marionette.find_element(*self._messages_frame_locator)
        self.marionette.switch_to_frame(messages_frame)

    @property
    def selected_messages(self):
        return int(self.marionette.find_element(*self._selected_messages_text_locator).text.split(' ')[0])
