# -*- coding: utf-8 -*-
# compiled by Tony96163

import sys
from PyQt5.QtWidgets import QApplication

from para_conc.core.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
