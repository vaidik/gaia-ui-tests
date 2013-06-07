# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion


class App(Base):

    _search_results_area_locator = ('id', 'search-results')

    _name_locator = ('css selector', '.info > h3')
    _author_locator = ('css selector', '.info .author')
    _install_button_locator = ('css selector', '.button.product.install')
    _price_locator = ('css selector', '.info div.price')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_element_not_present(*self._search_results_area_locator)

    @property
    def name(self):
        return self.find_element(*self._name_locator).text

    @property
    def author(self):
        return self.find_element(*self._author_locator).text

    @property
    def price(self):
        return self.find_element(*self._price_locator).text

    @property
    def install_button_text(self):
        return self.find_element(*self._install_button_locator).text

    def tap_install_button(self):
        self.find_element(*self._install_button_locator).tap()
        # Switch back to system app and expect the 'Install' dialog
        self.marionette.switch_to_frame()

    def tap_purchase_button(self):
        self.marionette.find_element(*self._install_button_locator).tap()

        # Return Bango payment object
        from gaiatest.apps.bango.app import Bango
        return Bango(self.marionette)
