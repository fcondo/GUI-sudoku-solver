"""
    sudoku_GUI.py

    Author: Fabio Condomitti
"""
import time
import pygame
import json

from copy import deepcopy
from solver import solve
from math import floor
from random import randint

WIDTH = 800
HEIGHT = 940
DIM = 9
LINE_COLOR = (0, 0, 0)    # black
BORDER_COLOR = (200, 0, 0)    # red
GREEN_BUTTON_OFF = (0, 180, 0)
GREEN_BUTTON_ON = (0, 220, 0)
YELLOW_BUTTON_OFF = (200, 200, 0)
YELLOW_BUTTON_ON = (225, 225, 0)
RED_BUTTON_OFF = (235, 0, 0)
RED_BUTTON_ON = (255, 0, 0)

pygame.font.init()


class Cube:

    def __init__(self, row, col, val, width, height):
        self.row = row
        self.col = col
        self.val = val
        self.temp = 0
        self.is_grid = False
        self.width = width
        self.height = height
        self.selected = False
        self.correct = 0

    def draw(self, win):
        size = 60
        x = self.row * self.width
        y = self.col * self.height
        s = ''
        color = (0, 15, 185)
        pos_x = x + self.width/2 - 12
        pos_y = y + self.height/2 - 15

        if(self.is_grid):
            color = (125, 125, 125)
            s = self.val
        elif(self.val != 0):
            color = (0, 0, 0)
            s = self.val
            
        # elif(not self.is_grid and self.temp != 0):
        elif(self.temp != 0):
            size = 35
            s = self.temp
            pos_x = x + 5
            pos_y = y + 5
            
        if(self.selected):
            pygame.draw.rect(win, (255,0,0), (x, y, self.width, self.height), 4)
        
        if(self.correct == 1):
            color = (0, 200, 0)
        elif(self.correct == 2):
            color = (200, 0, 0)

        font = pygame.font.SysFont('Comic Sans MS', size)
        string = font.render(str(s), 1, color)
        win.blit(string, (pos_x, pos_y))


class Grid:
    
    def __init__(self, win, width, height, row, col):
        self.win = win
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = None

        single_width = self.width / self.row
        single_height  = self.height / self.col
        self.cubes = [[Cube(i, j, 0, single_width, single_height) for j in range(self.col)] for i in range(self.row)]

    def reset(self):
        for i in range(0, self.row):
            for j in range(0, self.col):
                if(not self.cubes[i][j].is_grid):
                    self.cubes[i][j].temp = 0
                    self.cubes[i][j].val = 0
                self.cubes[j][i].correct = 0
    
    def new_game(self):
        for i in range(0, self.row):
            for j in range(0, self.col):
                    self.cubes[i][j].temp = 0
                    self.cubes[i][j].val = 0
                    self.cubes[i][j].is_grid = False
                    self.cubes[i][j].selected = False
                    self.cubes[j][i].correct = False
        self.selected = None
    
    def fix_grid(self):
        gr = []
        for i in range(0, self.row):
            temp = []
            for j in range(0, self.col):
                if(self.cubes[i][j].val != 0):
                    self.cubes[i][j].is_grid = True
                    self.cubes[i][j].color = (100, 100, 100)
                temp.append(self.cubes[i][j].val)
            gr.append(temp)

    def set_temp(self, k):
        if(self.selected):
            i = self.selected[0]
            j = self.selected[1]
            if(not self.cubes[i][j].is_grid):
                self.cubes[i][j].temp = k
                self.cubes[i][j].val = 0
    
    def set_val(self, k):
        if(self.selected):
            i = self.selected[0]
            j = self.selected[1]
            if(k == 0):
                k = self.cubes[i][j].temp
            self.cubes[i][j].val = k

    def select(self, ii, jj):
        for i in range(0, self.row):
            for j in range(0, self.col):
                self.cubes[i][j].selected = False

        self.cubes[ii][jj].selected = True
        self.selected = (ii, jj)
    
    def random(self):
        with open('grids.json', 'r') as f:
            data = json.load(f)
        i = str(randint(0, len(data.keys()) - 1))
        sudoku_grid = data[i]
        for i in range(len(sudoku_grid)):
            for j in range(len(sudoku_grid[0])):
                self.cubes[i][j].val = sudoku_grid[j][i]
        self.fix_grid()

    def check_solution(self):
        start_grid = []
        grid = []
        for i in range(0, self.row):
            start_temp = []
            temp = []
            for j in range(0, self.col):
                temp.append(self.cubes[j][i].val)
                if(self.cubes[j][i].is_grid):
                    start_temp.append(self.cubes[j][i].val)
                else:
                    start_temp.append(0)
            grid.append(temp)
            start_grid.append(start_temp)
        
        corrected_grid = deepcopy(start_grid)
        solve(corrected_grid, DIM)

        correct = True
        for i in range(0, self.row):
            for j in range(0, self.col):
                if(corrected_grid[i][j] != grid[i][j]):
                    correct = False
        
        if(correct):
            result = 1
            print("Sudoku solved!")
        else:
            result = 2
            print('Sudoku not solved. Restart it')

        for i in range(0, self.row):
            for j in range(0, self.col):
                self.cubes[j][i].correct = result
        return correct

    def count_free_cubes(self):
        count = DIM * DIM
        for i in range(0, self.row):
            for j in range(0, self.col):
                if(self.cubes[i][j].val != 0):
                    count -= 1
        return count

    def get_clicked_cube(self, mouse_pos):
            space_x = self.width / self.row
            space_y = self.height / self.col

            i = floor(mouse_pos[0] / space_x)
            j = floor(mouse_pos[1] / space_y)

            return (i, j)

    def draw(self):
        # draw grid
        for i in range(0, self.row):
            for j in range(0, self.col):
                self.cubes[i][j].draw(self.win)        

        # draw lines
        space = self.width / self.row
        
        for i in range(0, self.row):
            for j in range(0, self.col):
                if(i % 3 == 0):
                    thickness = 4
                else:
                    thickness = 1
                pygame.draw.line(self.win, LINE_COLOR, (0, i * space), (self.width, i * space), thickness)
                pygame.draw.line(self.win, LINE_COLOR, (i * space, 0), (i * space, self.height), thickness)
        
        pygame.draw.line(self.win, BORDER_COLOR, (0, 9 * space), (self.width, 9 * space), 5)

def get_formatted_time(s):
    seconds = int(s % 60)
    minutes = int(s / 60)
    # hours = int(minutes / 60)

    return ('{0}:{1}').format(minutes, seconds)

class Button:

    def __init__(self, c, cc, x, y, w, h, f=None, text=''):
        self.text = text
        self.color = c
        self.color_list = [c, cc]
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.fun = f

    def draw(self, win, outline=None):
        if(outline):
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if(self.text != ''):
            button_font = pygame.font.SysFont('Comic Sans MS', 45)
            text = button_font.render(str(self.text), 1, (255, 255, 255))
            pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height), 0)
            
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        self.color = self.color_list[0]
        if(pos[0] > self.x and pos[0] < self.x + self.width):
            if pos[1] > self.y and pos[1] < self.y + self.height:
                self.color = self.color_list[1]
                return (True, self.text)

        return (False, self.text)


class Sudoku_GUI:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Sudoku Solver')
        self.grid = Grid(self.win, self.width, self.width, DIM, DIM)
        self.started = False
        self.finished = False

        new_btn = Button(GREEN_BUTTON_OFF, GREEN_BUTTON_ON, 20, self.height - 105, 170, 70, f=self.grid.new_game, text='New game')
        random_btn = Button(YELLOW_BUTTON_OFF, YELLOW_BUTTON_ON, 220, self.height - 105, 190, 70, f=self.grid.random, text='Random')
        reset_btn = Button(YELLOW_BUTTON_OFF, YELLOW_BUTTON_ON, 220, self.height - 105, 190, 70, f=self.grid.reset, text='Restart')
        # solve_btn = Button(RED_BUTTON_OFF, RED_BUTTON_ON, 520, self.height - 85, 185, 70, f=self.grid.check_solution, text='Solve game')
        start_btn = Button(GREEN_BUTTON_OFF, GREEN_BUTTON_ON, 20, self.height - 105, 170, 70, f=self.grid.fix_grid, text='Start game')
        self.b = [new_btn, reset_btn, random_btn, start_btn]

        self.execute()

    def get_pressed_number(self, event):
        key = 0
        if(event.key == pygame.K_1 or event.key == pygame.K_KP1):
            key = 1
        if(event.key == pygame.K_2 or event.key == pygame.K_KP2):
            key = 2
        if(event.key == pygame.K_3 or event.key == pygame.K_KP3):
            key = 3
        if(event.key == pygame.K_4 or event.key == pygame.K_KP4):
            key = 4
        if(event.key == pygame.K_5 or event.key == pygame.K_KP5):
            key = 5
        if(event.key == pygame.K_6 or event.key == pygame.K_KP6):
            key = 6
        if(event.key == pygame.K_7 or event.key == pygame.K_KP7):
            key = 7
        if(event.key == pygame.K_8 or event.key == pygame.K_KP8):
            key = 8
        if(event.key == pygame.K_9 or event.key == pygame.K_KP9):
            key = 9
        if((event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE) and not self.finished):
            self.grid.set_val(0)
            self.grid.set_temp(0)

        return key
        
    def move_cursor(self, key, event):
        i, j = self.grid.selected
        if(event.key == pygame.K_LEFT):
            i = i - 1
            if i < 0:
                i = 0
            key = 0
            self.grid.select(i, j)
        if(event.key == pygame.K_RIGHT):
            i = i + 1
            if i + 1 > self.grid.row:
                i = self.grid.row - 1
            key = 0
            self.grid.select(i, j)
        if(event.key == pygame.K_UP):
            j = j - 1
            if j < 0:
                j = 0
            key = 0
            self.grid.select(i, j)
        if(event.key == pygame.K_DOWN):
            j = j + 1
            if j + 1 > self.grid.col:
                j = self.grid.col - 1
            key = 0
            self.grid.select(i, j)
        
        if(not self.started):
            i = self.grid.selected[0]
            j = self.grid.selected[1]
            if(self.grid.cubes[i][j].val != 0):
                key = self.grid.cubes[i][j].val
        return key

    def execute(self):
        self.run = True
        start = time.time()
        self.playing_time = 0

        while(self.run):
            clock = pygame.time.Clock()
            clock.tick(60)

            if(self.started):
                if(not self.finished):
                    self.playing_time = time.time() - start
                self.buttons = self.b[:-2]
            else:
                self.playing_time = 0
                self.buttons = self.b[-2:]

            pos = pygame.mouse.get_pos()

            if(self.grid.selected):
                i = self.grid.selected[0]
                j = self.grid.selected[1]
                key = self.grid.cubes[i][j].val
            else:
                key = 0
            
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    self.run = False

                if(event.type == pygame.KEYDOWN):
                    key = self.get_pressed_number(event)    # handle numbers
                    
                    if(self.grid.selected):                 # handle moving cursor with arrow keys
                        key = self.move_cursor(key, event)
                    
                    if(not self.started):                   # setup custom grid
                        self.grid.set_val(key)
                    else:
                        if(key != 0):
                            self.grid.set_temp(key)         # temporary value
                        if(event.key == pygame.K_RETURN):   # new val becomes fixed after RETURN only
                            if(self.grid.cubes[i][j].val != 0):
                                key = self.grid.cubes[i][j].val
                            self.grid.set_val(key)
                            if(self.grid.count_free_cubes() == 0):
                                if(self.grid.check_solution()):
                                    # self.started = False
                                    self.finished = True

                    
                if(event.type == pygame.MOUSEMOTION):
                    for b in self.buttons:
                        if(b.is_over(pos)[0]):
                            b.color = b.color_list[1]
                        else:
                            b.color = b.color_list[0]

                if(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    if(pos[1] > WIDTH):     # check button click
                        for b in self.buttons:
                            if(b.is_over(pos)[0]):
                                b.fun()
                                if(b.is_over(pos)[1] == 'New game'):
                                    self.started = False
                                    self.finished = False
                                elif(b.is_over(pos)[1] == 'Start game' or b.is_over(pos)[1] == 'Random'):
                                    self.started = True
                                    self.finished = False
                                    start = time.time()
                                elif(b.is_over(pos)[1] == 'Restart' or b.is_over(pos)[1] == 'Solve'):
                                    start = time.time()
                                    self.finished = False
                                    
                    else:                   # check grid click
                        i, j = self.grid.get_clicked_cube(pos)
                        self.grid.select(i, j)

            self.draw()
            pygame.display.update()

        pygame.quit()

    def draw(self):
        self.win.fill((255,255,255))
        self.grid.draw()
        space = self.width / DIM

        font = pygame.font.SysFont('Comic Sans MS', 45)
        string = font.render('Elapsed time:  ' + get_formatted_time(self.playing_time), 1, (255, 0, 0))
        self.win.blit(string, (self.width / 2 + 40, 9 * space + 55))

        for b in self.buttons:
            b.draw(self.win, 1)

        
g = Sudoku_GUI(WIDTH, HEIGHT)
