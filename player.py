import threading
from time import sleep

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QLabel


class Player(QLabel):
    def __init__(self, nebitno, grid, bullet, x, y, num_of_player):
        super().__init__(nebitno)
        # kreiraj player-a
        self.setGeometry(x, y, 32, 32)
        if num_of_player == 1:
            self.setPixmap(QtGui.QPixmap('Images/bubble_right.png'))
        else:
            self.setPixmap(QtGui.QPixmap('Images/bobble_left.png'))
        self.grid = grid
        self.setAccessibleName("player_right")
        self.bullet = bullet
        self.num_of_player = num_of_player

        self.padanje = True
        self.skok = False
        self.kretanje_levo = False
        self.kretanje_desno = False
