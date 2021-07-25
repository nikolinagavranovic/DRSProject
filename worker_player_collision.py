import time

from PyQt5.QtCore import pyqtSignal

from worker import Worker


class WorkerPlayerCollision(Worker):

    killed_by_enemy = pyqtSignal()
    increment_lives = pyqtSignal(int)

    def __init__(self, player, player_num, grid, enemies, dead_enemies):
        super().__init__()

        self.player = player
        self.enemies = enemies
        self.dead_enemies = dead_enemies
        self.grid = grid
        self.is_done = False
        self.player_num = player_num

    def die(self):
        """
        End notifications.
        """
        self.is_done = True
        self.thread.quit()

    def work(self):
        if self.player_num == 1:
            while not self.is_done:
                if not self.proveri_enemies_levo_desno():
                    time.sleep(0.01)
                    self.killed_by_enemy.emit()
                    time.sleep(0.01)
                elif not self.proveri_dead_enemies_levo_desno():
                    time.sleep(0.01)
                else:
                    time.sleep(0.01)
        elif self.player_num == 2:
            while not self.is_done:
                if not self.proveri_enemies_levo_desno():
                    time.sleep(0.01)
                    self.killed_by_enemy.emit()
                    time.sleep(0.01)
                elif not self.proveri_dead_enemies_levo_desno():
                    time.sleep(0.01)
                else:
                    time.sleep(0.01)

    def proveri_enemies_levo_desno(self):

        enemies_2 = []

        for enemy in self.enemies:
            if enemy.x() + enemy.width() <= self.player.x() and (enemy.x() + enemy.width()) >= (self.player.x() - 10):
                enemies_2.append(enemy)

        gornja_ivica_bulleta = self.player.y()
        donja_ivica_bulleta = self.player.y() + self.player.height()

        enemy_konacno = []

        for enemy in enemies_2:
            if (enemy.y() <= gornja_ivica_bulleta and ((enemy.y() + enemy.height()) > gornja_ivica_bulleta)) or (
                    donja_ivica_bulleta <= (enemy.y() + enemy.height()) and donja_ivica_bulleta >= enemy.y()):
                enemy_konacno.append(enemy)

        enemies_3 = []

        for enemy in self.enemies:
            if enemy.x() >= (self.player.x() + self.player.width()) and enemy.x() <= (self.player.x() + self.player.width()) + 10:
                enemies_3.append(enemy)

        gornja_ivica_bulleta = self.player.y()
        donja_ivica_bulleta = self.player.y() + self.player.height()

        enemy2_konacno = []

        for enemy in enemies_3:
            if (enemy.y() <= gornja_ivica_bulleta and ((enemy.y() + enemy.height()) > gornja_ivica_bulleta)) or (
                    donja_ivica_bulleta <= (enemy.y() + enemy.height()) and donja_ivica_bulleta >= enemy.y()):
                enemy2_konacno.append(enemy)

        return len(enemy_konacno) == 0 and len(enemy2_konacno) == 0

    def proveri_dead_enemies_levo_desno(self):

        dead_enemies_2 = []

        for d_enemy in self.dead_enemies:
            if d_enemy.x() + d_enemy.width() <= self.player.x() and (d_enemy.x() + d_enemy.width()) >= (self.player.x() - 10):
                dead_enemies_2.append(d_enemy)

        gornja_ivica_bulleta = self.player.y()
        donja_ivica_bulleta = self.player.y() + self.player.height()

        dead_enemy_konacno = []

        for d_enemy in dead_enemies_2:
            if (d_enemy.y() <= gornja_ivica_bulleta and ((d_enemy.y() + d_enemy.height()) > gornja_ivica_bulleta)) or (
                    donja_ivica_bulleta <= (d_enemy.y() + d_enemy.height()) and donja_ivica_bulleta >= d_enemy.y()):
                dead_enemy_konacno.append(d_enemy)

        dead_enemies_3 = []

        for d_enemy in self.dead_enemies:
            if d_enemy.x() >= (self.player.x() + self.player.width()) and d_enemy.x() <= (self.player.x() + self.player.width()) + 10:
                dead_enemies_3.append(d_enemy)

        gornja_ivica_bulleta = self.player.y()
        donja_ivica_bulleta = self.player.y() + self.player.height()

        dead_enemy2_konacno = []

        for d_enemy in dead_enemies_3:
            if (d_enemy.y() <= gornja_ivica_bulleta and ((d_enemy.y() + d_enemy.height()) > gornja_ivica_bulleta)) or (
                    donja_ivica_bulleta <= (d_enemy.y() + d_enemy.height()) and donja_ivica_bulleta >= d_enemy.y()):
                dead_enemy2_konacno.append(d_enemy)

                if d_enemy.accessibleName() == "dead_enemy1":
                    self.increment_lives.emit(1)
                else:
                    self.increment_lives.emit(2)

        return len(dead_enemy_konacno) == 0 and len(dead_enemy2_konacno) == 0