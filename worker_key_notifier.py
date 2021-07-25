import time

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtGui, QtCore

from worker import Worker


class WorkerKeyNotifier(Worker):

    key_signal = pyqtSignal(int)

    def __init__(self, player, num_of_player, grid):
        super().__init__()

        self.player = player
        self.grid = grid
        self.keys = []
        self.is_done = False
        self.jump = False
        self.counter = 0
        self.num_of_player = num_of_player
        self.bullet_counter = 0

        self.padanje = False

    def add_key(self, key):
        self.keys.append(key)

    def rem_key(self, key):
        self.keys.remove(key)

    def die(self):
        """
        End notifications.
        """
        self.is_done = True
        self.thread.quit()

    def work(self):
        if self.num_of_player == 1:
            while not self.is_done:
                if self.jump and self.counter < 35:
                    self.key_signal.emit(QtCore.Qt.Key_Up)
                    self.counter = self.counter + 1
                elif self.jump:
                    self.jump = False
                    self.counter = 0

                if self.check_if_fall(self.player, self.grid) and not self.padanje and not self.jump:
                    self.padanje = True
                    self.add_key(QtCore.Qt.Key_Down)
                elif not self.check_if_fall(self.player, self.grid) and self.padanje:
                    self.padanje = False
                    self.rem_key(QtCore.Qt.Key_Down)

                for k in self.keys:
                    if k == QtCore.Qt.Key_Up and not self.jump and not self.padanje:
                        self.jump = True
                        self.key_signal.emit(k)
                        self.counter = self.counter + 1
                    elif k != QtCore.Qt.Key_Up and k != QtCore.Qt.Key_W and k != QtCore.Qt.Key_A and k != QtCore.Qt.Key_D:
                        self.key_signal.emit(k)
                time.sleep(0.01)
        else:
            while not self.is_done:
                if self.jump and self.counter < 35:
                    self.key_signal.emit(QtCore.Qt.Key_W)
                    self.counter = self.counter + 1
                elif self.jump:
                    self.jump = False
                    self.counter = 0

                if self.check_if_fall(self.player, self.grid) and not self.padanje and not self.jump:
                    self.padanje = True
                    self.add_key(QtCore.Qt.Key_S)
                elif not self.check_if_fall(self.player, self.grid) and self.padanje:
                    self.padanje = False
                    self.rem_key(QtCore.Qt.Key_S)

                for k in self.keys:
                    if k == QtCore.Qt.Key_W and not self.jump and not self.padanje:
                        self.jump = True
                        self.key_signal.emit(k)
                        self.counter = self.counter + 1
                    elif k != QtCore.Qt.Key_W and k != QtCore.Qt.Key_Up and k != QtCore.Qt.Key_Left and k != QtCore.Qt.Key_Right:
                        self.key_signal.emit(k)
                time.sleep(0.01)

    # provera da li je ispod playera platforma, tj da li ce player padati
    # prvo uzimamo donju ivicu playera, zatim uzimam sva polja iz grida
    # zatim filtriram samo polja platforme, pa filtriram samo polja platforme koja su u x osi tacno ispod playera (+-5px)
    # i na kraju od tih polja platforme tacno ispod playera, filtriram samo ona koja su bar delom u ravni playera (y osi)
    # ako ima takvih polja, onda player nece padati i funkcija vraca false
    def check_if_fall(self, player, grid):
        donja_ivica_playera = self.player.y() + self.player.height()

        items = (self.grid.itemAt(i) for i in range(self.grid.count()))
        bricks = []

        for w in items:
            if w.widget().accessibleName() == "brick":
                bricks.append(w.widget())

        bricks_2 = []
        for brick in bricks:
            if brick.y() >= donja_ivica_playera and brick.y() <= donja_ivica_playera + 5:
                bricks_2.append(brick)

        leva_ivica_playera = self.player.x()
        desna_ivica_playera = self.player.x() + self.player.width()

        brick_konacno = []

        for brick2 in bricks_2:
            if (brick2.x() <= leva_ivica_playera and ((brick2.x() + brick2.width()) > leva_ivica_playera)) or (
                    desna_ivica_playera <= (brick2.x() + brick2.width()) and desna_ivica_playera >= brick2.x()):
                brick_konacno.append(brick2)

        if len(brick_konacno) == 0:
            return True
        else:
            return False
