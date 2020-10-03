"""
    sudoku_GUI.py

    Author: Fabio Condomitti
"""
import time
import pygame
from math import floor


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
        self.fixed = False
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        font = pygame.font.SysFont('Comic Sans MS', 30)
        
        x = self.row * self.width
        y = self.col * self.height

        if(self.fixed):
            s = self.val
            pos_x = self.width/2 - 30
            pos_y = self.height/2 - 30

            if(self.val != 0):
                s = self.val
            elif(self.temp != 0):
                s = self.temp
                pos_x = x + 5
                pos_y = y + 5
            else:
                s = ''
                pos_x = x + 5
                pos_y = y + 5
        else:
            s = ''#self.val
            pos_x = self.width/2 - 30
            pos_y = self.height/2 - 30
            
        if(self.selected):
            pygame.draw.rect(win, (255,0,0), (x, y, self.width, self.height), 4)
        
        string = font.render(str(s), 1, (125, 125, 125))
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
                self.cubes[i][j].temp = 0
                self.cubes[i][j].val = 0

        print('RESET')
    
    def fix_cubes(self):
        for i in range(0, self.row):
            for j in range(0, self.col):
                if(self.cubes[i][j].val == 0):
                    self.cubes[i][j].fixed = True

    def set_temp(self, k):
        if(self.selected):
            i = self.selected[0]
            j = self.selected[1]
            self.cubes[i][j].temp = k
            print(i, j, k)
    
    def set_val(self, k):
        if(self.selected):
            i = self.selected[0]
            j = self.selected[1]
            self.cubes[i][j].val = k

    def select(self, ii, jj):
        for i in range(0, self.row):
            for j in range(0, self.col):
                self.cubes[i][j].selected = False

        self.cubes[ii][jj].selected = True
        self.selected = (ii, jj)


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

def get_time_format(t):
    return '00:20'


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
                return True

        return False


class Sudoku_GUI:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Sudoku Solver')
        self.grid = Grid(self.win, self.width, self.width, DIM, DIM)
        self.time = 0
        self.started = False

        # new_btn = Button(GREEN_BUTTON_OFF, GREEN_BUTTON_ON, 20, self.height - 105, 170, 70, f=self.grid.reset, text='New game')
        # reset_btn = Button(YELLOW_BUTTON_OFF, YELLOW_BUTTON_ON, 220, self.height - 105, 190, 70, f=self.grid.reset, text='Restart')
        # solve_btn = Button(RED_BUTTON_OFF, RED_BUTTON_ON, 520, self.height - 85, 185, 70, f=self.grid.reset, text='Solve game')
        
        new_btn = Button(GREEN_BUTTON_OFF, GREEN_BUTTON_ON, 20, self.height - 105, 170, 70, f=self.grid.reset, text='New game')
        reset_btn = Button(YELLOW_BUTTON_OFF, YELLOW_BUTTON_ON, 220, self.height - 105, 190, 70, f=self.grid.reset, text='Restart')
        solve_btn = Button(RED_BUTTON_OFF, RED_BUTTON_ON, 520, self.height - 85, 185, 70, f=self.grid.reset, text='Solve game')
        start_btn = Button(GREEN_BUTTON_OFF, GREEN_BUTTON_ON, 20, self.height - 105, 170, 70, f=self.grid.fix_cubes, text='Start game')
        
        self.buttons = [new_btn, reset_btn, solve_btn, start_btn]

        self.execute()
        
    def execute(self):
        self.run = True
        key = None
        while(self.run):
            clock = pygame.time.Clock()
            clock.tick(60)
            pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    self.run = False

                if(event.type == pygame.KEYDOWN):
                    # if(event.key == pygame.K_0 or event.key == pygame.K_KP0):
                    #     key = 0
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
                    # if(event.key == pygame.K_0 or event.key == pygame.K_KP0):
                    #     key = 0
                    # if(event.key == pygame.K_1 or event.key == pygame.K_KP1):
                    #     key = 1
                    # if(event.key == pygame.K_0 or event.key == pygame.K_KP0):
                    #     key = 0
                    if(not self.started):
                        self.grid.set_val(key)

                    if(event.key == pygame.K_RETURN):
                        key = 0
                    if(event.key == pygame.K_RETURN):
                        self.grid.set_val(key)


                if(event.type == pygame.MOUSEMOTION):
                    for b in self.buttons:
                        if(b.is_over(pos)):
                            b.color = b.color_list[1]
                        else:
                            b.color = b.color_list[0]

                if(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    
                    if(pos[1] > WIDTH):     # check button click
                        for b in self.buttons:
                            if(b.is_over(pos)):
                                b.fun()
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

        font = pygame.font.SysFont('Comic Sans MS', 50)
        string = font.render('Elapsed time:  ' + get_time_format(time), 1, (255, 0, 0))
        self.win.blit(string, (self.width / 2 + 42, 9 * space + 10))

        for b in self.buttons:
            b.draw(self.win, 1)

        
g = Sudoku_GUI(WIDTH, HEIGHT)
