# -*- coding: utf-8 -*-
# Copyright (c) 2020 Tony96163 (42716403@qq.com)

# Disclaimer:

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PyQt5.QtWidgets import QMainWindow, QTextEdit


class SubWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SubWindow, self).__init__(parent)
        self.setWindowTitle('全文')
        self.setGeometry(100, 100, 400, 400)
        self._browser = QTextEdit(self)
        self.setCentralWidget(self._browser)

    def set_title(self, title):
        self.setWindowTitle(title)

    def set_text(self, text):
        self._browser.setText(text)
