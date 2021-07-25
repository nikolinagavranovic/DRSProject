import time

from PyQt5.QtCore import pyqtSignal

from worker import Worker


class WorkerShootBubble(Worker):

    move_bullet = pyqtSignal(list)
    kill_enemy = pyqtSignal(int)
    create_dead_enemy1 = pyqtSignal(list)
    create_dead_enemy2 = pyqtSignal(list)

    def __init__(self, player, player_num, enemies, grid):
        super().__init__()

        self.enemies = enemies
        self.player = player
        self.player_num = player_num
        self.grid = grid
        self.is_done = False
        self.metak_u_letu = False
        self.bullet_count = 0
        self.shoot_direction = 0  # levo (1) , desno (2)
        self.enemy1_coord = []
        self.enemy2_coord = []

        self.retList = []
        self.retList.append(self.player_num)

    def shoot(self):
        if not self.metak_u_letu:
            self.metak_u_letu = True
            if self.player.accessibleName() == "player_right":
                self.shoot_direction = 2
            else:
                self.shoot_direction = 1.

    def die(self):
        """
        End notifications.
        """
        self.is_done = True
        self.thread.quit()

    def work(self):
        while not self.is_done:
            if self.metak_u_letu and (not self.proveri_desno() or not self.proveri_levo()):
                self.metak_u_letu = False
                self.bullet_count = 0
                self.retList.append(3)
                self.move_bullet.emit(self.retList)
                self.retList.pop()
            if self.metak_u_letu and self.shoot_direction == 2 and self.bullet_count < 45:
                self.retList.append(2)
                self.move_bullet.emit(self.retList)
                self.retList.pop()
                self.bullet_count = self.bullet_count + 1
            elif self.metak_u_letu and self.shoot_direction == 1 and self.bullet_count < 45:
                self.retList.append(1)
                self.move_bullet.emit(self.retList)
                self.retList.pop()
                self.bullet_count = self.bullet_count + 1
            elif self.metak_u_letu:
                self.metak_u_letu = False
                self.bullet_count = 0
                self.retList.append(3)
                self.move_bullet.emit(self.retList)
                self.retList.pop()
            time.sleep(0.01)

    # uzimam sva polja grida, filtriram samo cigle, zatim filtriram sve cigle koje su u x osi odmah desno uz bullet(+- 5px)
    # i na kraju filtriram samo ciglu koja je u ravni sa bullet-om po y osi
    def proveri_desno(self):
        items = (self.grid.itemAt(i) for i in range(self.grid.count()))

        bricks = []

        for w in items:
            if w.widget().accessibleName() == "brick":
                bricks.append(w.widget())

        enemies_2 = []
        bricks_2 = []

        for brick in bricks:
            if brick.x() >= (self.player.bullet.x() + self.player.bullet.width()) and brick.x() <= (self.player.bullet.x() + self.player.bullet.width()) + 5:
                bricks_2.append(brick)

        for enemy in self.enemies:
            if enemy.x() >= (self.player.bullet.x() + self.player.bullet.width()) and enemy.x() <= (self.player.bullet.x() + self.player.bullet.width()) + 10:
                enemies_2.append(enemy)

        gornja_ivica_bulleta = self.player.bullet.y()
        donja_ivica_bulleta = self.player.bullet.y() + self.player.bullet.height()
        brick_konacno = []

        for brick2 in bricks_2:
            if (brick2.y() <= gornja_ivica_bulleta and ((brick2.y() + brick2.height()) > gornja_ivica_bulleta)) or (
                    donja_ivica_bulleta <= (brick2.y() + brick2.height()) and donja_ivica_bulleta >= brick2.y()):
                brick_konacno.append(brick2)
                # print(brick2.pos())

        enemy_konacno = []

        for enemy in enemies_2:
            if (enemy.y() <= gornja_ivica_bulleta and ((enemy.y() + enemy.height()) > gornja_ivica_bulleta)) or (
                    donja_ivica_bulleta <= (enemy.y() + enemy.height()) and donja_ivica_bulleta >= enemy.y()):
                enemy_konacno.append(enemy)
                # stvori jaje i unisti enemija

                if enemy.accessibleName() == "enemy1":
                    self.enemy1_coord.append(enemy.x())
                    self.enemy1_coord.append(enemy.y())
                    self.kill_enemy.emit(1)
                    self.create_dead_enemy1.emit(self.enemy1_coord)
                else:
                    self.enemy2_coord.append(enemy.x())
                    self.enemy2_coord.append(enemy.y())
                    self.kill_enemy.emit(2)
                    self.create_dead_enemy2.emit(self.enemy2_coord)

                # enemy.lower()
                # for d_en in self.dead_enemies:
                #     if d_en.x() == -100:
                #         d_en.move(enemy.x(), enemy.y())
                #         d_en.kreni_ka_gore(False)
                #         break

                # self.enemies.remove(enemy)

        return len(brick_konacno) == 0 and len(enemy_konacno) == 0

    # uzimam sva polja grida, filtriram samo cigle, zatim filtriram sve cigle koje su u x osi odmah levo uz bullet(+- 5px)
    # i na kraju filtriram samo ciglu koja je u ravni sa bullet-om po y osi
    def proveri_levo(self):
        items = (self.grid.itemAt(i) for i in range(self.grid.count()))

        bricks = []

        for w in items:
            if w.widget().accessibleName() == "brick":
                bricks.append(w.widget())

        bricks_2 = []
        enemies_2 = []

        for brick in bricks:
            if brick.x() + brick.width() <= self.player.bullet.x() and (brick.x() + brick.width()) >= (self.player.bullet.x() - 5):
                bricks_2.append(brick)

        for enemy in self.enemies:
            if enemy.x() + enemy.width() <= self.player.bullet.x() and (enemy.x() + enemy.width()) >= (self.player.bullet.x() - 10):
                enemies_2.append(enemy)

        gornja_ivica_bulleta = self.player.bullet.y()
        donja_ivica_bulleta = self.player.bullet.y() + self.player.bullet.height()
        brick_konacno = []

        for brick2 in bricks_2:
            if (brick2.y() <= gornja_ivica_bulleta and ((brick2.y() + brick2.height()) > gornja_ivica_bulleta)) or (
                    donja_ivica_bulleta <= (brick2.y() + brick2.height()) and donja_ivica_bulleta >= brick2.y()):
                brick_konacno.append(brick2)
                # print(brick2.pos())

        enemy_konacno = []

        for enemy in enemies_2:
            if (enemy.y() <= gornja_ivica_bulleta and ((enemy.y() + enemy.height()) > gornja_ivica_bulleta)) or (
                    donja_ivica_bulleta <= (enemy.y() + enemy.height()) and donja_ivica_bulleta >= enemy.y()):
                enemy_konacno.append(enemy)
                # stvori jaje i unisti enemija
                if enemy.accessibleName() == "enemy1":
                    self.enemy1_coord.append(enemy.x())
                    self.enemy1_coord.append(enemy.y())
                    self.kill_enemy.emit(1)
                    self.create_dead_enemy1.emit(self.enemy1_coord)
                else:
                    self.enemy2_coord.append(enemy.x())
                    self.enemy2_coord.append(enemy.y())
                    self.kill_enemy.emit(2)
                    self.create_dead_enemy2.emit(self.enemy2_coord)
                # for d_en in self.dead_enemies:
                #     if d_en.x() == -100:
                #         d_en.move(enemy.x(), enemy.y())
                #         d_en.kreni_ka_gore(False)
                #         break

                # self.enemies.remove(enemy)

        return len(brick_konacno) == 0 and len(enemy_konacno) == 0
