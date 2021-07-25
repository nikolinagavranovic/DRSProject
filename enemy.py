import threading
from time import sleep

from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel


class Enemy(QLabel):
    def __init__(self, nebitno, grid, x, y):
        #print(nebitno)
        super().__init__(nebitno)
        # kreiraj enemy-ja
        self.setGeometry(x, y, 32, 32)
        self.setPixmap(QtGui.QPixmap('Images/enemy_left.png'))
        self.grid = grid
        self.setAccessibleName("enemy_left")
        self.padanje = True
        # inicijalno odmah po kreiranju enemija nek krene da se krece levo
        # self.enemy_kretnja_levo(False)
