import time

from PyQt5.QtCore import pyqtSignal

from worker import Worker


class WorkerDeadEnemy(Worker):

    move_dead_enemy1 = pyqtSignal()
    move_dead_enemy2 = pyqtSignal()
    next_level = pyqtSignal()

    def __init__(self, dead_enemy, d_en_num, grid, num_of_dead_enemies):
        super().__init__()

        self.dead_enemy = dead_enemy
        self.num_of_dead_enemies = num_of_dead_enemies
        self.grid = grid
        self.is_done = False
        self.d_en_num = d_en_num

    def die(self):
        """
        End notifications.
        """
        self.is_done = True
        self.thread.quit()

    def work(self):
        if self.d_en_num == 1:
            while not self.is_done:
                if self.dead_enemy.y() >= 52:
                    self.move_dead_enemy1.emit()
                    time.sleep(0.01)
                else:
                    time.sleep(3)
                    if self.num_of_dead_enemies == 2:
                        self.next_level.emit()
                    self.die()
                    break
        elif self.d_en_num == 2:
            while not self.is_done:
                if self.dead_enemy.y() >= 52:
                    self.move_dead_enemy2.emit()
                    time.sleep(0.01)
                else:
                    time.sleep(3)
                    if self.num_of_dead_enemies == 2:
                        self.next_level.emit()
                    self.die()
                    break
