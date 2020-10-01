"""
    sudoku_GUI.py

    Author: Fabio Condomitti
"""
import time
import pygame

DIM = 9
LINE_COLOR = (0, 0, 0)    # black
BORDER_COLOR = (200, 0, 0)    # red

pygame.init()


class Cube:

    def __init__(self, row, col, val, width, height):
        self.row = row
        self.col = col
        self.val = val
        self.temp = 0
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        x = self.row * width
        y = self.col * height

        # win.blit()


class Grid:
    
    def __init__(self, win, width, height, row, col):
        self.win = win
        self.row = row
        self.col = col
        self.width = width
        self.height = height

        single_width = self.width / self.row
        single_height  = self.height / self.col
        self.cubes = [[Cube(i, j, 0, single_width, single_height) for j in range(self.col)] for i in range(self.row)]

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

def draw_window(window, grid, time):
    window.fill((255,255,255))
    grid.draw()

def main():

    win = pygame.display.set_mode((800, 880))
    pygame.display.set_caption('Sudoku Solver')
    win.fill((255,255,255))
    
    grid = Grid(win, 800, 800, DIM, DIM)
    
    t = 0

    run = True
    while(run):
        pygame.time.delay(100)

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
        
        
        draw_window(win, grid, t)
        pygame.display.update()

main()
pygame.quit()