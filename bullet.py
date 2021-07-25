import threading
from time import sleep

from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel


class Bullet(QLabel):
    def __init__(self, nebitno, grid):
        super().__init__(nebitno)
        # kreiraj bullet
        self.setGeometry(51, 570, 32, 32)
        self.setPixmap(QtGui.QPixmap('Images/bubble_ball.png'))
        self.enemies = nebitno.enemies
        self.nebitno = nebitno
        self.game_win = nebitno
        self.dead_enemies = nebitno.dead_enemies
        self.grid = grid
        self.setAccessibleName("bullet")
        self.metak_u_letu = False
