import os
import random
import time
import threading
import sys
import Constants
from msvcrt import getch

class Desk():   # Вынести логику игры в класс Core

    def __init__(self):
        self.desk = self.make_desk()
        self.primary_arrangement()
        self.direction = '-'

    def make_desk(self):
        desk = [['#' for i in range(17)] for g in range(17)]
        field = ['·' for i in range(1, 16)]
        for i in desk[1: 16]:
            i[1: 16] = field
        return desk

    # Первичная остановка
    def primary_arrangement(self):
        self.player = Player()
        self.desk[7][6] = self.player.p
        self.obj_manager = Object_Manager()
        self.player_cords = [7, 6]
        self.player.render_body(self.desk)
        self.gen_obj()
        self.desk[0].append(f'|{self.player.score}|')

    # Отрисовка доски
    def render(self):
        while Constants.GAME_WORK:
            self.desk[0][-1] = f'|{self.player.score}|'
            for i in self.desk:
               for g in i:
                   print(g + '    ', end='')
               print('\n')
            time.sleep(0.0153)
            os.system("cls")

    # Отлов направления движения
    def define_direction(self):
        while Constants.GAME_WORK:
            self.direction = getch().decode()
            #if self.direction == 'e':
            #    self.game_end()

    # Генерация объектов
    def gen_obj(self):
        while True:
            new_obj_cord = self.obj_manager.obj_generator()
            if self.desk[new_obj_cord[0]][new_obj_cord[1]] == '○' or \
                    self.desk[new_obj_cord[0]][new_obj_cord[1]] == '□':
                continue
            else:
                break
        self.desk[new_obj_cord[0]][new_obj_cord[1]] = self.obj_manager.obj

    def change_cords(self, future_cord):
        horizontal_cord, vertical_cord = self.player_cords
        self.desk[horizontal_cord][vertical_cord] = '·'
        lost_obj_flag = self.check_object(future_cord)
        self.desk[future_cord[0]][future_cord[1]] = self.player.p
        self.player.move_body(self.desk, self.player_cords)
        if lost_obj_flag:
            self.gen_obj()
        self.player_cords = future_cord

    def new_obj_body(self):
        self.player.body.append(self.player.vre_cords)

    def check_object(self, future_cord):
        if self.desk[future_cord[0]][future_cord[1]] == '■':
            self.player.score += 100
            self.new_obj_body()
            return True
        if self.desk[future_cord[0]][future_cord[1]] == '#' or \
                self.desk[future_cord[0]][future_cord[1]] == '□':
            self.game_end()

    # Движение
    def move(self):
        while Constants.GAME_WORK:
            time.sleep(0.4)
            horizontal_cord, vertical_cord = self.player_cords
            if self.direction == 'w':
                self.change_cords([horizontal_cord - 1, vertical_cord])
            if self.direction == 'a':
                self.change_cords([horizontal_cord, vertical_cord - 1])
            if self.direction == 's':
                self.change_cords([horizontal_cord + 1, vertical_cord])
            if self.direction == 'd':
                self.change_cords([horizontal_cord, vertical_cord + 1])
            if self.direction == 'e':
                self.game_end()

    def game_end(self):
        Constants.GAME_WORK = False
        os.system("cls")
        print(f"Игра закончена, вы набрали - {self.player.score} очков")
        sys.exit()

    def start_page(self):
        print("Игра Змейка - цель набрать наибольшее количество очков за поедание объектов - ■, \n "
              "Вы будете увеличивать в размерах при поедании объекта, \n"
              "При столкновении с телом - □ или границей - # - игра заканчивается \n"
              "Управляющие кнопки - wasd, e - выход из игры \n"
              "Нажмите любую кнопку, чтобы начать")
        input()

    def main(self):
        self.start_page()
        threading.Thread(target=self.render).start()
        threading.Thread(target=self.define_direction).start()
        threading.Thread(target=self.move).start()


class Player:
    def __init__(self):
        self.p = '○'
        self.score = 0
        self.body = [[7, 5], [7, 4], [7, 3]]

    def render_body(self, desk):
        for i in self.body:
            desk[i[0]][i[1]] = '□'

    def move_body(self, desk, player_cords):
        self.vre_cords = self.body[-1]
        for i in reversed(range(len(self.body))):
            self.body[i] = self.body[i-1]
        self.body[0] = player_cords
        desk[self.vre_cords[0]][self.vre_cords[1]] = '·'
        self.render_body(desk)

class Object_Manager:

    def __init__(self):
        self.obj = '■'

    def obj_generator(self):
        a = random.randint(1, 15)
        b = random.randint(1, 15)
        return [a, b]

d = Desk()
d.main()



