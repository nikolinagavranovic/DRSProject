from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDesktopWidget, QWidget, QGridLayout, QMainWindow, QLabel

from bullet import Bullet
from dead_enemy import DeadEnemy
from enemy import Enemy
from player import Player
from worker_dead_enemy import WorkerDeadEnemy
from worker_deus_ex_machina import WorkerDeusExMachina

from worker_enemy_movement import WorkerEnemyMovement
from worker_key_notifier import WorkerKeyNotifier
from worker_player_collision import WorkerPlayerCollision

from worker_shoot_bubble import WorkerShootBubble


class GameWindow(QMainWindow):
    def __init__(self, broj_playera, first_win, enemy_speed):
        super().__init__()

        self.num_of_players = broj_playera
        self.first_win = first_win
        self.bullet1_positioned = False
        self.bullet2_positioned = False

        self.player1_lives = 3
        self.player2_lives = 3

        self.num_of_dead_enemies = 0

        self.enemy_speed = enemy_speed

        self.initUI()

    def initUI(self):

        self.win = QWidget()
        self.setCentralWidget(self.win)
        grid = QGridLayout()

        self.initGrid(grid)

        # setuj grid u okviru layout-a prozora i kreiraj sam prozor
        self.win.setLayout(grid)
        self.setWindowTitle("Bubble Bobble")
        self.setGeometry(100, 100, 850, 650)
        self.setFixedSize(850, 650)
        # da nema ovoga videla bi se mreza
        self.setStyleSheet("background-color: black;")

        self.enemies = []
        self.enemies.append(Enemy(self, grid, 400, 50))
        self.enemies.append(Enemy(self, grid, 500, 50))

        self.enemies[0].setAccessibleName("enemy1")
        self.enemies[1].setAccessibleName("enemy2")

        self.dead_enemies = []
        self.dead_enemies.append(DeadEnemy(self, grid, -100, -100))
        self.dead_enemies.append(DeadEnemy(self, grid, -100, -100))

        self.dead_enemies[0].setAccessibleName("dead_enemy1")
        self.dead_enemies[1].setAccessibleName("dead_enemy2")

        self.bullet1 = Bullet(self, grid)
        #self.bullet.raise_()
        # sakrij bullet widget na iza nekog drugog widget-a na njegovoj poziciji
        self.bullet1.lower()

        self.bullet2 = Bullet(self, grid)
        # self.bullet.raise_()
        # sakrij bullet widget na iza nekog drugog widget-a na njegovoj poziciji
        self.bullet2.lower()


        # kreiraj player-a i prosledi mu grid zbog funkcija koje koristi i u kojima ce koristiti grid polja
        self.player1 = Player(self, grid, self.bullet1, 51, 570, 1)
        self.deus_ex_machina1 = WorkerDeusExMachina(self.player1, 1, grid)
        self.deus_ex_machina1.show_on_grid.connect(self.__show_deus_ex1__)
        self.deus_ex_machina1.apply_force.connect(self.__apply_deus_ex1__)

        self.deus_ex1 = QLabel(self)
        self.deus_ex1.setGeometry(-100, -100, 32, 32)
        self.deus_ex1.setPixmap(QtGui.QPixmap('Images/deus_ex.jpg'))
        self.deus_ex1.lower()

        if self.num_of_players == 2:
            self.player2 = Player(self, grid, self.bullet2, 735, 570, 2)
            self.deus_ex_machina2 = WorkerDeusExMachina(self.player2, 2, grid)
            self.deus_ex_machina2.show_on_grid.connect(self.__show_deus_ex2__)
            self.deus_ex_machina2.apply_force.connect(self.__apply_deus_ex2__)

            self.deus_ex2 = QLabel(self)
            self.deus_ex2.setGeometry(-100, -100, 32, 32)
            self.deus_ex2.setPixmap(QtGui.QPixmap('Images/deus_ex2.jpg'))
            self.deus_ex2.lower()

        #self.player1.setFocus()
        #self.player2.setFocus()

        self.shoot_bubble = WorkerShootBubble(self.player1, 1, self.enemies, grid)
        self.shoot_bubble.move_bullet.connect(self.__shoot_bubble__)
        self.shoot_bubble.kill_enemy.connect(self.__kill_enemy__)
        self.shoot_bubble.create_dead_enemy1.connect(self.__create_dead_enemy1__)
        self.shoot_bubble.create_dead_enemy2.connect(self.__create_dead_enemy2__)
        self.shoot_bubble.start()

        if self.num_of_players == 2:
            self.shoot_bubble2 = WorkerShootBubble(self.player2, 2, self.enemies, grid)
            self.shoot_bubble2.move_bullet.connect(self.__shoot_bubble__)
            self.shoot_bubble2.kill_enemy.connect(self.__kill_enemy__)
            self.shoot_bubble2.create_dead_enemy1.connect(self.__create_dead_enemy1__)
            self.shoot_bubble2.create_dead_enemy2.connect(self.__create_dead_enemy2__)
            self.shoot_bubble2.start()

        self.enemy_movement = []
        self.en_num = 0

        for en in self.enemies:
            self.en_num = self.en_num + 1
            self.enemy_movement.append(WorkerEnemyMovement(en, self.en_num,  grid, self.enemies, self.enemy_speed))
            # self.enemy_movement.move_enemy.connect(self.__enemy_movement__)
            # self.enemy_movement.start()

        self.enemy_movement[0].move_enemy1.connect(self.__enemy1_movement__)
        self.enemy_movement[0].fall_enemy1.connect(self.__enemy1_fall__)
        self.enemy_movement[0].jump_enemy1.connect(self.__enemy1_jump__)
        self.enemy_movement[0].start()

        self.enemy_movement[1].move_enemy2.connect(self.__enemy2_movement__)
        self.enemy_movement[1].fall_enemy2.connect(self.__enemy2_fall__)
        self.enemy_movement[1].jump_enemy2.connect(self.__enemy2_jump__)
        self.enemy_movement[1].start()

        self.dead_enemy_movement = []
        self.d_en_num = 0

        for d_en in self.dead_enemies:
            self.d_en_num = self.d_en_num + 1
            self.dead_enemy_movement.append(WorkerDeadEnemy(d_en, self.d_en_num, grid, self.num_of_dead_enemies))

        self.dead_enemy_movement[0].move_dead_enemy1.connect(self.__dead_enemy1_movement__)
        self.dead_enemy_movement[0].next_level.connect(self.__next_level__)

        self.dead_enemy_movement[1].move_dead_enemy2.connect(self.__dead_enemy2_movement__)
        self.dead_enemy_movement[1].next_level.connect(self.__next_level__)

        self.player1_collision = WorkerPlayerCollision(self.player1, 1, grid, self.enemies, self.dead_enemies)
        self.player1_collision.killed_by_enemy.connect(self.__player1_killed_by_enemy__)
        self.player1_collision.increment_lives.connect(self.__player1_increment_lives__)
        self.player1_collision.start()

        if self.num_of_players == 2:
            self.player2_collision = WorkerPlayerCollision(self.player2, 2, grid, self.enemies, self.dead_enemies)
            self.player2_collision.killed_by_enemy.connect(self.__player2_killed_by_enemy__)
            self.player2_collision.increment_lives.connect(self.__player2_increment_lives__)
            self.player2_collision.start()

        self.bubble_life1 = QLabel(self)
        self.bubble_life1.setGeometry(11, 11, 32, 32)
        self.bubble_life1.setPixmap(QtGui.QPixmap('Images/bubble_life.jpg'))
        self.bubble_life1.setAccessibleName("player1_life1")
        self.bubble_life1.raise_()

        self.bubble_life2 = QLabel(self)
        self.bubble_life2.setGeometry(53, 11, 32, 32)
        self.bubble_life2.setPixmap(QtGui.QPixmap('Images/bubble_life.jpg'))
        self.bubble_life2.setAccessibleName("player1_life2")
        self.bubble_life2.raise_()

        self.bubble_life3 = QLabel(self)
        self.bubble_life3.setGeometry(95, 11, 32, 32)
        self.bubble_life3.setPixmap(QtGui.QPixmap('Images/bubble_life.jpg'))
        self.bubble_life3.setAccessibleName("player1_life3")
        self.bubble_life3.raise_()

        if self.num_of_players == 2:
            self.bobble_life1 = QLabel(self)
            self.bobble_life1.setGeometry(723, 11, 32, 32)
            self.bobble_life1.setPixmap(QtGui.QPixmap('Images/bobble_life.jpg'))
            self.bobble_life1.setAccessibleName("player2_life1")
            self.bobble_life1.raise_()

            self.bobble_life2 = QLabel(self)
            self.bobble_life2.setGeometry(765, 11, 32, 32)
            self.bobble_life2.setPixmap(QtGui.QPixmap('Images/bobble_life.jpg'))
            self.bobble_life2.setAccessibleName("player2_life2")
            self.bobble_life2.raise_()

            self.bobble_life3 = QLabel(self)
            self.bobble_life3.setGeometry(807, 11, 32, 32)
            self.bobble_life3.setPixmap(QtGui.QPixmap('Images/bobble_life.jpg'))
            self.bobble_life3.setAccessibleName("player2_life3")
            self.bobble_life3.raise_()

        # centriraj window i prikazi ga
        self.center()
        self.show()


        self.key_notifier = WorkerKeyNotifier(self.player1, 1, grid)
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

        if self.num_of_players == 2:
            self.key_notifier2 = WorkerKeyNotifier(self.player2, 2, grid)
            self.key_notifier2.key_signal.connect(self.__update_position__)
            self.key_notifier2.start()

        self.deus_ex_machina1.start()
        if self.num_of_players == 2:
            self.deus_ex_machina2.start()

    # kad ugasim aplikaciju rucno obrisi sve pokrenute procese(threadove) od enemyja
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.key_notifier.die()
        self.shoot_bubble.die()
        self.player1_collision.die()
        self.deus_ex_machina1.die()
        for em in self.enemy_movement:
            em.die()
        if self.num_of_players == 2:
            self.key_notifier2.die()
            self.shoot_bubble2.die()
            self.player2_collision.die()
            self.deus_ex_machina2.die()

    # centriranje windowa
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.shoot_bubble.shoot()
        elif event.key() == QtCore.Qt.Key_Control:
            self.shoot_bubble2.shoot()
        elif event.key() != QtCore.Qt.Key_Down and event.key() != QtCore.Qt.Key_S:
            self.key_notifier.add_key(event.key())
            if self.num_of_players == 2:
                self.key_notifier2.add_key(event.key())

    def keyReleaseEvent(self, event):
        if event.key() != QtCore.Qt.Key_Down and event.key() != QtCore.Qt.Key_S and event.key() != QtCore.Qt.Key_Space and event.key() != QtCore.Qt.Key_Control:
            self.key_notifier.rem_key(event.key())
            if self.num_of_players == 2:
                self.key_notifier2.rem_key(event.key())

    @pyqtSlot()
    def __next_level__(self):
        self.close()
        if self.num_of_players == 2:
            generate_next_level = GameWindow(2, self.first_win, self.enemy_speed + 0.5)
        else:
            generate_next_level = GameWindow(1, self.first_win, self.enemy_speed + 0.5)

    @pyqtSlot(int)
    def __show_deus_ex1__(self, place_on_grid):
        if place_on_grid == 1:
            self.deus_ex1.move(190, 315)
            self.deus_ex1.raise_()
        elif place_on_grid == 2:
            self.deus_ex1.move(550, 315)
            self.deus_ex1.raise_()

    @pyqtSlot(list)
    def __apply_deus_ex1__(self, apply_force_list):
        if apply_force_list[0] == 1:
            self.deus_ex1.lower()
            self.deus_ex1.move(-100, -100)
            if apply_force_list[1] == 1:
                if apply_force_list[2] == 1 and self.player1_lives < 3:
                    if self.player1_lives == 2:
                        self.bubble_life3.raise_()
                        self.player1_lives = self.player1_lives + 1
                    else:
                        self.bubble_life2.raise_()
                        self.player1_lives = self.player1_lives + 1
                else:
                    if self.player1_lives == 3:
                        self.bubble_life3.lower()
                        self.player1_lives = self.player1_lives - 1
                    elif self.player1_lives == 2:
                        self.bubble_life2.lower()
                        self.player1_lives = self.player1_lives - 1
                    else:
                        if self.num_of_players == 1:
                            self.bubble_life1.lower()
                            self.player1_lives = self.player1_lives - 1
                            # kraj igre vrati na start game window
                            self.close()
                            self.first_win.show()
                        else:
                            if self.player2_lives < 1:
                                self.bubble_life1.lower()
                                self.player1_lives = self.player1_lives - 1
                                # kraj igre vrati na start game window
                                self.close()
                                self.first_win.show()
                        self.bubble_life1.lower()
                        self.player1_lives = self.player1_lives - 1
                        self.deus_ex_machina1.die()

    @pyqtSlot(int)
    def __show_deus_ex2__(self, place_on_grid):
        if place_on_grid == 3:
            self.deus_ex2.move(220, 445)
            self.deus_ex2.raise_()
        elif place_on_grid == 4:
            self.deus_ex2.move(550, 445)
            self.deus_ex2.raise_()

    @pyqtSlot(list)
    def __apply_deus_ex2__(self, apply_force_list):
        if apply_force_list[0] == 2:
            self.deus_ex2.lower()
            self.deus_ex2.move(-100, -100)
            if apply_force_list[1] == 1:
                if apply_force_list[2] == 1 and self.player2_lives < 3:
                    if self.player2_lives == 2:
                        self.bobble_life1.raise_()
                        self.player2_lives = self.player2_lives + 1
                    else:
                        self.bobble_life2.raise_()
                        self.player2_lives = self.player2_lives + 1
                else:
                    if self.player2_lives == 3:
                        self.bobble_life1.lower()
                        self.player2_lives = self.player2_lives - 1
                    elif self.player2_lives == 2:
                        self.bobble_life2.lower()
                        self.player2_lives = self.player2_lives - 1
                    else:
                        if self.player1_lives < 1:
                            self.bobble_life3.lower()
                            self.player2_lives = self.player2_lives - 1
                            # kraj igre vrati na start game window
                            self.close()
                            self.first_win.show()
                        self.bobble_life3.lower()
                        self.player2_lives = self.player2_lives - 1
                        self.deus_ex_machina2.die()

    @pyqtSlot(int)
    def __kill_enemy__(self, en_num):
        print(len(self.enemies))
        if en_num == 1:
            for en in self.enemies:
                if en.accessibleName() == "enemy1":
                    en.lower()
                    self.enemy_movement[0].die()
                    self.enemies.remove(en)
                    self.shoot_bubble.enemies = self.enemies
                    if self.num_of_players == 2:
                        self.shoot_bubble2.enemies = self.enemies
        else:
            for en in self.enemies:
                if en.accessibleName() == "enemy2":
                    en.lower()
                    self.enemy_movement[1].die()
                    self.enemies.remove(en)
                    self.shoot_bubble.enemies = self.enemies
                    if self.num_of_players == 2:
                        self.shoot_bubble2.enemies = self.enemies
        print(len(self.enemies))

    @pyqtSlot(int)
    def __player1_increment_lives__(self, num_of_dead_enemy):
        if num_of_dead_enemy == 1:
            for d_en in self.dead_enemies:
                if d_en.accessibleName() == "dead_enemy1":
                    d_en.lower()
                    d_en.move(-100, -100)
                    break
        else:
            for d_en in self.dead_enemies:
                if d_en.accessibleName() == "dead_enemy2":
                    d_en.lower()
                    d_en.move(-100, -100)
                    break
        if self.player1_lives < 3:
            self.player1_lives = self.player1_lives + 1
            if self.player1_lives == 2:
                self.bubble_life2.raise_()
            elif self.player1_lives == 3:
                self.bubble_life3.raise_()

    @pyqtSlot(int)
    def __player2_increment_lives__(self, num_of_dead_enemy):
        if num_of_dead_enemy == 1:
            for d_en in self.dead_enemies:
                if d_en.accessibleName() == "dead_enemy1":
                    d_en.lower()
                    d_en.move(-100, -100)
                    break
        else:
            for d_en in self.dead_enemies:
                if d_en.accessibleName() == "dead_enemy2":
                    d_en.lower()
                    d_en.move(-100, -100)
                    break
        if self.player2_lives < 3:
            self.player2_lives = self.player2_lives + 1
            if self.player2_lives == 2:
                self.bobble_life2.raise_()
            elif self.player2_lives == 3:
                self.bobble_life1.raise_()

    @pyqtSlot()
    def __player1_killed_by_enemy__(self):
        self.player1_lives = self.player1_lives - 1
        if self.player1_lives == 2:
            self.bubble_life3.lower()
            self.player1.setPixmap(QtGui.QPixmap('Images/bubble_right.png'))
            self.player1.setAccessibleName("player_right")
            self.player1.move(51, 570)
            self.key_notifier.jump = False
        elif self.player1_lives == 1:
            self.bubble_life2.lower()
            self.player1.setPixmap(QtGui.QPixmap('Images/bubble_right.png'))
            self.player1.setAccessibleName("player_right")
            self.player1.move(51, 570)
            self.key_notifier.jump = False
        elif self.num_of_players == 1:
            self.bubble_life1.lower()
            # kraj igre vrati na start game window
            self.close()
            self.first_win.show()
        elif self.player2_lives > 0:
            self.bubble_life1.lower()
            self.player1.move(-100, -100)
            self.player1.lower()
            self.deus_ex_machina1.die()
        else:
            self.bubble_life1.lower()
            # kraj igre vrati na start game window
            self.close()
            self.first_win.show()

    @pyqtSlot()
    def __player2_killed_by_enemy__(self):
        self.player2_lives = self.player2_lives - 1
        if self.player2_lives == 2:
            self.bobble_life1.lower()
            self.player2.setPixmap(QtGui.QPixmap('Images/bobble_left.png'))
            self.player2.setAccessibleName("player_right")
            self.player2.move(735, 570)
            self.key_notifier2.jump = False
        elif self.player2_lives == 1:
            self.bobble_life2.lower()
            self.player2.setPixmap(QtGui.QPixmap('Images/bobble_left.png'))
            self.player2.setAccessibleName("player_right")
            self.player2.move(735, 570)
            self.key_notifier2.jump = False
        elif self.player1_lives > 0:
            self.bobble_life3.lower()
            self.player2.move(-100, -100)
            self.player2.lower()
            self.deus_ex_machina2.die()
        else:
            self.bobble_life1.lower()
            # kraj igre vrati na start game window
            self.close()
            self.first_win.show()

    @pyqtSlot(int)
    def __enemy1_movement__(self, move_signal):
        for en in self.enemies:
            if en.accessibleName() == "enemy1":
                rec = en.geometry()
                if move_signal == 1:
                    en.setPixmap(QtGui.QPixmap('Images/enemy_right.png'))
                    en.move(rec.x() + 5, rec.y())
                elif move_signal == 2:
                    en.setPixmap(QtGui.QPixmap('Images/enemy_left.png'))
                    en.move(rec.x() - 5, rec.y())

    @pyqtSlot(int)
    def __enemy2_movement__(self, move_signal):
        for en in self.enemies:
            if en.accessibleName() == "enemy2":
                rec = en.geometry()
                if move_signal == 1:
                    en.setPixmap(QtGui.QPixmap('Images/enemy_right.png'))
                    en.move(rec.x() + 5, rec.y())
                elif move_signal == 2:
                    en.setPixmap(QtGui.QPixmap('Images/enemy_left.png'))
                    en.move(rec.x() - 5, rec.y())

    @pyqtSlot()
    def __enemy1_fall__(self):
        for en in self.enemies:
            if en.accessibleName() == "enemy1":
                en.move(en.x(), en.y() + 5)

    @pyqtSlot()
    def __enemy2_fall__(self):
        for en in self.enemies:
            if en.accessibleName() == "enemy2":
                en.move(en.x(), en.y() + 5)

    @pyqtSlot()
    def __enemy1_jump__(self):
        for en in self.enemies:
            if en.accessibleName() == "enemy1":
                en.move(en.x(), en.y() - 5)

    @pyqtSlot()
    def __enemy2_jump__(self):
        for en in self.enemies:
            if en.accessibleName() == "enemy2":
                en.move(en.x(), en.y() - 5)

    @pyqtSlot(list)
    def __create_dead_enemy1__(self, enemy_coord):
        self.num_of_dead_enemies = self.num_of_dead_enemies + 1
        for d_en in self.dead_enemies:
            if d_en.accessibleName() == "dead_enemy1":
                d_en.move(enemy_coord[0], enemy_coord[1])
                self.dead_enemy_movement[0].dead_enemy = d_en
                self.dead_enemy_movement[0].num_of_dead_enemies = self.num_of_dead_enemies
                self.dead_enemy_movement[0].start()
                # d_en.kreni_ka_gore(False)
                break

    @pyqtSlot(list)
    def __create_dead_enemy2__(self, enemy_coord):
        self.num_of_dead_enemies = self.num_of_dead_enemies + 1
        for d_en in self.dead_enemies:
            if d_en.accessibleName() == "dead_enemy2":
                d_en.move(enemy_coord[0], enemy_coord[1])
                self.dead_enemy_movement[1].dead_enemy = d_en
                self.dead_enemy_movement[1].num_of_dead_enemies = self.num_of_dead_enemies
                self.dead_enemy_movement[1].start()
                # d_en.kreni_ka_gore(False)
                break

    @pyqtSlot()
    def __dead_enemy1_movement__(self):
        for d_en in self.dead_enemies:
            if d_en.accessibleName() == "dead_enemy1":
                rec = d_en.geometry()
                d_en.move(rec.x(), rec.y() - 5)

    @pyqtSlot()
    def __dead_enemy2_movement__(self):
        for d_en in self.dead_enemies:
            if d_en.accessibleName() == "dead_enemy2":
                rec = d_en.geometry()
                d_en.move(rec.x(), rec.y() - 5)

    @pyqtSlot(list)
    def __shoot_bubble__(self, direction):
        if direction[0] == 1:
            if direction[1] == 2 and not self.bullet1_positioned:
                self.bullet1_positioned = True
                self.player1.bullet.setGeometry(self.player1.x(), self.player1.y(), 32, 32)
                self.player1.bullet.raise_()
                self.player1.raise_()
                self.player1.bullet.move(self.player1.bullet.x() + 5, self.player1.bullet.y())
            elif direction[1] == 2:
                self.player1.bullet.raise_()
                self.player1.raise_()
                self.player1.bullet.move(self.player1.bullet.x() + 5, self.player1.bullet.y())
            elif direction[1] == 1 and not self.bullet1_positioned:
                self.bullet1_positioned = True
                self.player1.bullet.setGeometry(self.player1.x(), self.player1.y(), 32, 32)
                self.player1.bullet.raise_()
                self.player1.raise_()
                self.player1.bullet.move(self.player1.bullet.x() - 5, self.player1.bullet.y())
            elif direction[1] == 1:
                self.player1.bullet.raise_()
                self.player1.raise_()
                self.player1.bullet.move(self.player1.bullet.x() - 5, self.player1.bullet.y())
            else:
                self.player1.bullet.setGeometry(self.player1.x(), self.player1.y(), 32, 32)
                self.player1.bullet.lower()
                self.bullet1_positioned = False
        else:
            if direction[1] == 2 and not self.bullet2_positioned:
                self.bullet2_positioned = True
                self.player2.bullet.setGeometry(self.player2.x(), self.player2.y(), 32, 32)
                self.player2.bullet.raise_()
                self.player2.raise_()
                self.player2.bullet.move(self.player2.bullet.x() + 5, self.player2.bullet.y())
            elif direction[1] == 2:
                self.player2.bullet.raise_()
                self.player2.raise_()
                self.player2.bullet.move(self.player2.bullet.x() + 5, self.player2.bullet.y())
            elif direction[1] == 1 and not self.bullet2_positioned:
                self.bullet2_positioned = True
                self.player2.bullet.setGeometry(self.player2.x(), self.player2.y(), 32, 32)
                self.player2.bullet.raise_()
                self.player2.raise_()
                self.player2.bullet.move(self.player2.bullet.x() - 5, self.player2.bullet.y())
            elif direction[1] == 1:
                self.player2.bullet.raise_()
                self.player2.raise_()
                self.player2.bullet.move(self.player2.bullet.x() - 5, self.player2.bullet.y())
            else:
                self.player2.bullet.setGeometry(self.player2.x(), self.player2.y(), 32, 32)
                self.player2.bullet.lower()
                self.bullet2_positioned = False

    @pyqtSlot(int)
    def __update_position__(self, key):
        rec1 = self.player1.geometry()
        if key == QtCore.Qt.Key_Right and rec1.x() <= 765 and rec1.x() > -60:
            self.player1.setPixmap(QtGui.QPixmap('Images/bubble_right.png'))
            self.player1.setAccessibleName("player_right")
            self.player1.setGeometry(rec1.x() + 5, rec1.y(), rec1.width(), rec1.height())
        elif key == QtCore.Qt.Key_Up and rec1.y() >= 60:
            self.player1.setGeometry(rec1.x(), rec1.y() - 5, rec1.width(), rec1.height())
        elif key == QtCore.Qt.Key_Down and rec1.y() < 570:
            self.player1.setGeometry(rec1.x(), rec1.y() + 5, rec1.width(), rec1.height())
        elif key == QtCore.Qt.Key_Left and rec1.x() >= 56:
            self.player1.setPixmap(QtGui.QPixmap('Images/bubble_left.png'))
            self.player1.setAccessibleName("player_left")
            self.player1.setGeometry(rec1.x() - 5, rec1.y(), rec1.width(), rec1.height())

        if self.num_of_players == 2:
            rec2 = self.player2.geometry()

            if key == QtCore.Qt.Key_D and rec2.x() <= 765 and rec2.x() > -60:
                self.player2.setPixmap(QtGui.QPixmap('Images/bobble_right.png'))
                self.player2.setAccessibleName("player_right")
                self.player2.setGeometry(rec2.x() + 5, rec2.y(), rec2.width(), rec2.height())
            elif key == QtCore.Qt.Key_W and rec2.y() >= 60:
                self.player2.setGeometry(rec2.x(), rec2.y() - 5, rec2.width(), rec2.height())
            elif key == QtCore.Qt.Key_S and rec2.y() < 570:
                self.player2.setGeometry(rec2.x(), rec2.y() + 5, rec2.width(), rec2.height())
            elif key == QtCore.Qt.Key_A and rec2.x() >= 56:
                self.player2.setPixmap(QtGui.QPixmap('Images/bobble_left.png'))
                self.player2.setAccessibleName("player_left")
                self.player2.setGeometry(rec2.x() - 5, rec2.y(), rec2.width(), rec2.height())

    def initGrid(self, grid):
        # inicijalno napravi grid 15*20 i svakom polju grida dodaj labelu koja ima black background
        for i in range(0, 15):
            for j in range(0, 20):
                label = QLabel(self)
                label.setStyleSheet("background-color: black;")
                grid.addWidget(label, i, j)
        # border left
        for i in range(0, 15):
            label = QLabel(self)
            pixmap = QPixmap('Images/brick.png')
            label.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())
            label.setScaledContents(True)
            label.setAccessibleName("brick")
            grid.addWidget(label, i, 0)
        # border top
        for i in range(0, 20):
            label = QLabel(self)
            pixmap = QPixmap('Images/brick.png')
            label.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())
            label.setScaledContents(True)
            label.setAccessibleName("brick")
            grid.addWidget(label, 0, i)
        # border bottom
        for i in range(0, 20):
            label = QLabel(self)
            pixmap = QPixmap('Images/brick.png')
            label.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())
            label.setScaledContents(True)
            label.setAccessibleName("brick")
            grid.addWidget(label, 14, i)
        # border right
        for i in range(0, 15):
            label = QLabel(self)
            pixmap = QPixmap('Images/brick.png')
            label.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())
            label.setScaledContents(True)
            label.setAccessibleName("brick")
            grid.addWidget(label, i, 19)
        # platform
        for i in range(10):
            label = QLabel(self)
            pixmap = QPixmap('Images/brick.png')
            label.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())
            label.setScaledContents(True)
            label.setAccessibleName("brick")
            grid.addWidget(label, 2, i + 5)
        # platform
        for i in range(8):
            label = QLabel(self)
            pixmap = QPixmap('Images/brick.png')
            label.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())
            label.setScaledContents(True)
            label.setAccessibleName("brick")
            grid.addWidget(label, 5, i + 11)

        # platform
        for i in range(7):
            label = QLabel(self)
            pixmap = QPixmap('Images/brick.png')
            label.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())
            label.setScaledContents(True)
            label.setAccessibleName("brick")
            grid.addWidget(label, 5, i + 1)

        # platform
        for i in range(5):
            label = QLabel(self)
            pixmap = QPixmap('Images/brick.png')
            label.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())
            label.setScaledContents(True)
            label.setAccessibleName("brick")
            grid.addWidget(label, 11, i + 4)

        # platform
        for i in range(9):
            label = QLabel(self)
            pixmap = QPixmap('Images/brick.png')
            label.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())
            label.setScaledContents(True)
            label.setAccessibleName("brick")
            grid.addWidget(label, 11, i + 10)
        # platform
        for i in range(6):
            label = QLabel(self)
            pixmap = QPixmap('Images/brick.png')
            label.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())
            label.setScaledContents(True)
            label.setAccessibleName("brick")
            grid.addWidget(label, 8, i + 3)

            # platform
            for i in range(6):
                label = QLabel(self)
                pixmap = QPixmap('Images/brick.png')
                label.setPixmap(pixmap)
                self.resize(pixmap.width(), pixmap.height())
                label.setScaledContents(True)
                label.setAccessibleName("brick")
                grid.addWidget(label, 8, i + 11)