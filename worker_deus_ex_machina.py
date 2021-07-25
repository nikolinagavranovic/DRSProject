import random
import time

from PyQt5.QtCore import pyqtSignal

from worker import Worker


class WorkerDeusExMachina(Worker):

    show_on_grid = pyqtSignal(int)
    apply_force = pyqtSignal(list)

    def __init__(self, player, player_num, grid):
        super().__init__()

        self.player = player
        self.grid = grid
        self.is_done = False
        self.player_num = player_num
        self.time_until_showing_on_grid = random.randint(7, 14)
        self.place_on_grid = random.randint(1, 2)

        self.deus_ex_coords1 = [190, 315]
        self.deus_ex_coords2 = [550, 315]

        self.deus_ex_coords3 = [220, 445]
        self.deus_ex_coords4 = [550, 445]

        self.retList = []
        self.retList.append(self.player_num)

    def die(self):
        """
        End notifications.
        """
        self.is_done = True
        self.thread.quit()

    def work(self):
        if self.player_num == 1:
            while not self.is_done:
                time.sleep(self.time_until_showing_on_grid)
                self.show_on_grid.emit(self.place_on_grid)
                time.sleep(2)
                self.check_if_player_is_in_deus_ex_box_and_apply_force()

                self.time_until_showing_on_grid = random.randint(7, 14)
                self.place_on_grid = random.randint(1, 2)
        elif self.player_num == 2:
            while not self.is_done:
                time.sleep(self.time_until_showing_on_grid)
                self.show_on_grid.emit(self.place_on_grid)
                time.sleep(2)
                self.check_if_player_is_in_deus_ex_box_and_apply_force()

                self.time_until_showing_on_grid = random.randint(7, 14)
                self.place_on_grid = random.randint(3, 4)

    def check_if_player_is_in_deus_ex_box_and_apply_force(self):

        if self.place_on_grid == 1:
            coords = self.deus_ex_coords1
        elif self.place_on_grid == 2:
            coords = self.deus_ex_coords2
        elif self.place_on_grid == 3:
            coords = self.deus_ex_coords3
        else:
            coords = self.deus_ex_coords4

        is_player_in_deus_ex_box = False

        if (self.player.x() >= coords[0] and self.player.x() <= (coords[0] + 32)) and (self.player.y() >= coords[1] and (self.player.y() <= coords[1] + 32)):
            is_player_in_deus_ex_box = True
        elif (self.player.x() + 32 >= coords[0] and self.player.x() + 32 <= (coords[0] + 32)) and (self.player.y() >= coords[1] and (self.player.y() <= coords[1] + 32)):
            is_player_in_deus_ex_box = True
        elif (self.player.x() >= coords[0] and self.player.x() <= (coords[0] + 32)) and (self.player.y() + 32 >= coords[1] and (self.player.y() + 32 <= coords[1] + 32)):
            is_player_in_deus_ex_box = True
        elif (self.player.x() + 32 >= coords[0] and self.player.x() + 32 <= (coords[0] + 32)) and (self.player.y() + 32 >= coords[1] and (self.player.y() + 32 <= coords[1] + 32)):
            is_player_in_deus_ex_box = True


        print(is_player_in_deus_ex_box)
        print(self.player.x())
        print(self.player.y())
        print('asdf')

        # u retList, prvi element je redni broj playera, drugi element je flag da li je player u deus_ex boxu (0 nije, 1 jeste)
        # i treci element flag da li se dodaje zivot playeru ili se brise zivot (1 dodaje 0 brise)
        # prvi element sam dodao odmah na pocetku klase, jer znam koji je redni broj playera
        # a druga dva dodajem u ovoj funkciji pri svakom pozivu
        if is_player_in_deus_ex_box:
            self.retList.append(1)
            self.retList.append(random.randint(0, 1))
            self.apply_force.emit(self.retList)
            self.retList.pop()
            self.retList.pop()
        else:
            self.retList.append(0)
            self.apply_force.emit(self.retList)
            self.retList.pop()

