#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2020 Tony Chang (42716403@qq.com)

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
import os,json
from PyQt5.QtWidgets import QMainWindow, QTextEdit


class SubWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SubWindow, self).__init__(parent)
        currentDir = os.getcwd()
        dataDir = os.path.join(currentDir, "app_data")
        workFileDir = os.path.join(dataDir, "workfiles")
        self._interface_lang_file = os.path.join(workFileDir,'interface_language_setting.txt')
        self._interface_lang_dict = os.path.join(workFileDir,'interface_language_dict.json')
        self.fc_lg, self.fc_dict = self.set_lang()
        
        self.setWindowTitle(self.fc_dict['sub_full_text'][self.fc_lg])
        self.setGeometry(100, 100, 400, 400)
        self._browser = QTextEdit(self)
        self.setCentralWidget(self._browser)
        
    def set_lang(self):
        with open (self._interface_lang_file, mode = 'r', encoding = 'utf-8-sig') as f:
            default_lg = f.read().strip()
        with open (self._interface_lang_dict, mode = 'r', encoding = 'utf-8-sig') as f:
            lg_dict = json.loads(f.read())
        return default_lg, lg_dict
    
    def set_title(self, title):
        self.setWindowTitle(title)

    def set_text(self, text):
        self._browser.setText(text)
