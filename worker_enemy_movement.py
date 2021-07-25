import random
import time

from PyQt5.QtCore import pyqtSignal

from worker import Worker


class WorkerEnemyMovement(Worker):

    move_enemy1 = pyqtSignal(int)
    move_enemy2 = pyqtSignal(int)

    fall_enemy1 = pyqtSignal()
    fall_enemy2 = pyqtSignal()

    jump_enemy1 = pyqtSignal()
    jump_enemy2 = pyqtSignal()

    def __init__(self, enemy, en_num, grid, enemies, enemy_speed):
        super().__init__()

        self.enemy_speed = enemy_speed
        self.enemies = enemies
        self.enemy = enemy
        self.grid = grid
        self.is_done = False
        self.jump = False
        self.counter = 0
        self.padanje = False
        self.krecem_se_levo = False
        self.krecem_se_desno = False
        self.en_num = en_num
        self.skok_brojac = 0
        self.time_until_jump = random.randint(20, 200)

        # kretanje enemija levo (2), kretanje enemija desno (1)

    def die(self):
        """
        End notifications.
        """
        self.is_done = True
        self.thread.quit()

    def work(self):
        if self.en_num == 1:
            # time.sleep(0.01)
            self.move_enemy1.emit(2)  # kretanje enemija levo (2), kretanje enemija desno (1)
            self.krecem_se_levo = True
            time.sleep(0.01 / self.enemy_speed)
            while not self.is_done:
                if self.check_if_fall(self.grid) and not self.jump:
                    self.padanje = True
                    self.fall_enemy1.emit()
                    time.sleep(0.01 / self.enemy_speed)
                else:
                    self.padanje = False

                if not self.padanje and not self.jump and self.skok_brojac > self.time_until_jump and self.enemy.y() >= 100:
                    self.jump = True
                    self.skok_brojac = 0
                    self.counter = self.counter + 1
                    self.jump_enemy1.emit()
                    time.sleep(0.01 / self.enemy_speed)
                elif self.jump and self.counter < 35:
                    self.skok_brojac = 0
                    self.counter = self.counter + 1
                    self.jump_enemy1.emit()
                    time.sleep(0.01 / self.enemy_speed)
                elif self.jump:
                    self.jump = False
                    self.skok_brojac = 0
                    self.counter = 0
                    self.time_until_jump = random.randint(50, 300)

                if self.krecem_se_levo and self.proveri_zid_levo():
                    self.move_enemy1.emit(2)
                    self.skok_brojac = self.skok_brojac + 1
                    time.sleep(0.01 / self.enemy_speed)
                elif not self.krecem_se_desno:
                    self.move_enemy1.emit(1)
                    self.krecem_se_levo = False
                    self.krecem_se_desno = True
                    self.skok_brojac = self.skok_brojac + 1
                    time.sleep(0.01 / self.enemy_speed)
                elif self.krecem_se_desno and self.proveri_zid_desno():
                    self.move_enemy1.emit(1)
                    self.skok_brojac = self.skok_brojac + 1
                    time.sleep(0.01 / self.enemy_speed)
                elif not self.krecem_se_levo:
                    self.move_enemy1.emit(2)
                    self.krecem_se_levo = True
                    self.krecem_se_desno = False
                    self.skok_brojac = self.skok_brojac + 1
                    time.sleep(0.01 / self.enemy_speed)
        elif self.en_num == 2:
            # time.sleep(0.01)
            self.move_enemy2.emit(2)
            self.krecem_se_levo = True
            time.sleep(0.01 / self.enemy_speed)
            while not self.is_done:
                if self.check_if_fall(self.grid) and not self.jump:
                    self.padanje = True
                    self.fall_enemy2.emit()
                    time.sleep(0.01 / self.enemy_speed)
                else:
                    self.padanje = False

                if not self.padanje and not self.jump and self.skok_brojac > self.time_until_jump and self.enemy.y() >= 100:
                    self.jump = True
                    self.skok_brojac = 0
                    self.counter = self.counter + 1
                    self.jump_enemy2.emit()
                    time.sleep(0.01 / self.enemy_speed)
                elif self.jump and self.counter < 35:
                    self.skok_brojac = 0
                    self.counter = self.counter + 1
                    self.jump_enemy2.emit()
                    time.sleep(0.01 / self.enemy_speed)
                elif self.jump:
                    self.jump = False
                    self.skok_brojac = 0
                    self.counter = 0
                    self.time_until_jump = random.randint(50, 300)
                if self.krecem_se_levo and self.proveri_zid_levo():
                    self.move_enemy2.emit(2)
                    self.skok_brojac = self.skok_brojac + 1
                    time.sleep(0.01 / self.enemy_speed)
                elif not self.krecem_se_desno:
                    self.move_enemy2.emit(1)
                    self.krecem_se_levo = False
                    self.krecem_se_desno = True
                    self.skok_brojac = self.skok_brojac + 1
                    time.sleep(0.01 / self.enemy_speed)
                elif self.krecem_se_desno and self.proveri_zid_desno():
                    self.move_enemy2.emit(1)
                    self.skok_brojac = self.skok_brojac + 1
                    time.sleep(0.01 / self.enemy_speed)
                elif not self.krecem_se_levo:
                    self.move_enemy2.emit(2)
                    self.krecem_se_levo = True
                    self.krecem_se_desno = False
                    self.skok_brojac = self.skok_brojac + 1
                    time.sleep(0.01 / self.enemy_speed)

    # provera dal se odmah levo od enemija nalazi zid
    # prvo uzimam sve zidove, zatim filtriram sve one levo od njega (od njegove leve ivice)
    # i na kraju filtriram samo onaj zid koji se nalazi odmah levo od njega
    def proveri_zid_levo(self):
        items = (self.grid.itemAt(i) for i in range(self.grid.count()))
        bricks = []

        for w in items:
            if w.widget().accessibleName() == "brick":
                bricks.append(w.widget())

        bricks_2 = []
        enemies_2 = []

        for brick in bricks:
            if brick.x() + brick.width() <= self.enemy.x() and (brick.x() + brick.width()) >= (self.enemy.x() - 5):
                bricks_2.append(brick)

        for enemy in self.enemies:
            if enemy.x() + enemy.width() <= self.enemy.x() and (enemy.x() + enemy.width()) >= (self.enemy.x() - 10):
                enemies_2.append(enemy)

        gornja_ivica_bulleta = self.enemy.y()
        donja_ivica_bulleta = self.enemy.y() + self.enemy.height()
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

        return len(brick_konacno) == 0 and len(enemy_konacno) == 0

    # provera dal se odmah desno od enemija nalazi zid
    # prvo uzimam sve zidove, zatim filtriram sve one desno od njega (od njegove desne ivice)
    # i na kraju filtriram samo onaj zid koji se nalazi odmah desno od njega
    def proveri_zid_desno(self):
        items = (self.grid.itemAt(i) for i in range(self.grid.count()))
        bricks = []

        for w in items:
            if w.widget().accessibleName() == "brick":
                bricks.append(w.widget())

        bricks_2 = []
        enemies_2 = []

        for brick in bricks:
            if brick.x() >= (self.enemy.x() + self.enemy.width()) and brick.x() <= (self.enemy.x() + self.enemy.width()) + 5:
                bricks_2.append(brick)
        # print(len(bricks_2))

        for enemy in self.enemies:
            if enemy.x() >= (self.enemy.x() + self.enemy.width()) and enemy.x() <= (self.enemy.x() + self.enemy.width()) + 10:
                enemies_2.append(enemy)

        gornja_ivica_bulleta = self.enemy.y()
        donja_ivica_bulleta = self.enemy.y() + self.enemy.height()
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

        return len(brick_konacno) == 0 and len(enemy_konacno) == 0

    # provera da li je ispod enemija platforma, tj da li ce enemy padati
    # prvo uzimamo donju ivicu enemija, zatim uzimam sva polja iz grida
    # zatim filtriram samo polja platforme, pa filtriram samo polja platforme koja su u x osi tacno ispod enemija (+-5px)
    # i na kraju od tih polja platforme tacno ispod enemija, filtriram samo ona koja su bar delom u ravni enemija (y osi)
    # ako ima takvih polja, onda enemy nece padati i funkcija vraca false
    def check_if_fall(self, grid):
        donja_ivica_enemy = self.enemy.y() + self.enemy.height()

        items = (grid.itemAt(i) for i in range(grid.count()))
        bricks = []

        for w in items:
            if w.widget().accessibleName() == "brick":
                bricks.append(w.widget())

        bricks_2 = []
        for brick in bricks:
            if brick.y() >= donja_ivica_enemy and brick.y() <= donja_ivica_enemy + 5:
                bricks_2.append(brick)

        leva_ivica_enemy = self.enemy.x()
        desna_ivica_enemy = self.enemy.x() + self.enemy.width()

        brick_konacno = []

        for brick2 in bricks_2:
            if (brick2.x() <= leva_ivica_enemy and ((brick2.x() + brick2.width()) > leva_ivica_enemy)) or (
                    desna_ivica_enemy <= (brick2.x() + brick2.width()) and desna_ivica_enemy >= brick2.x()):
                brick_konacno.append(brick2)
        return len(brick_konacno) == 0