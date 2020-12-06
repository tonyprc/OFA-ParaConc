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

import sys
from PyQt5.QtWidgets import QApplication

from para_conc.core.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
