import sys

from PyQt5.QtWidgets import QApplication

from first_window import FirstWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fir_win = FirstWindow()
    sys.exit(app.exec_())
