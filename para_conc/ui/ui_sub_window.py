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
