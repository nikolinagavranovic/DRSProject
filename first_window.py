from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QMainWindow, QHBoxLayout, \
    QDesktopWidget, QVBoxLayout, QLabel

from game_window import GameWindow


class FirstWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Bubble Bobble")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        lay = QVBoxLayout(self.central_widget)

        label = QLabel(self)
        pixmap = QPixmap('Images/first_window_img.jpg')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.setFixedSize(980, 650)

        label.setScaledContents(True)

        lay.addWidget(label)

        self.start_1p_btn = QPushButton("start 1P game", self)
        self.start_1p_btn.setGeometry(400, 280, 200, 50)
        self.start_1p_btn.setFont(QFont('Times', 15))
        self.start_1p_btn.setStyleSheet("background-color : yellow")
        self.start_1p_btn.clicked.connect(self.show_game_window_1p)

        self.start_2p_btn = QPushButton("start 2P game", self)
        self.start_2p_btn.setGeometry(400, 380, 200, 50)
        self.start_2p_btn.setFont(QFont('Times', 15))
        self.start_2p_btn.setStyleSheet("background-color : yellow")
        self.start_2p_btn.clicked.connect(self.show_game_window_2p)

        self.quit_btn = QPushButton("quit", self)
        self.quit_btn.setGeometry(400, 480, 200, 50)
        self.quit_btn.setFont(QFont('Times', 15))
        self.quit_btn.setStyleSheet("background-color : pink")
        self.quit_btn.clicked.connect(self.quit_game)

        self.center()
        self.show()

    def show_game_window_1p(self):
        self.close()
        self.next_window = GameWindow(1, self, 1)


    def show_game_window_2p(self):
        self.close()
        self.next_window = GameWindow(2, self, 1)

    def quit_game(self):
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())