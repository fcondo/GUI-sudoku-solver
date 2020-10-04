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

LINE_COLOR = (0, 0, 0)            # black
BORDER_COLOR = (200, 0, 0)
BLUE_BUTTON_OFF = (110, 214, 255)
BLUE_BUTTON_ON = (102, 204, 255)
GREEN_BUTTON_OFF = (163, 255, 231)
GREEN_BUTTON_ON = (153, 255, 221)
RED_BUTTON_OFF = (235, 0, 0)
RED_BUTTON_ON = (255, 0, 0)

pygame.font.init()


class Cube:
    """
    This class handles the basic cell needed to compose the whole grid
    """
    def __init__(self, row, col, val, width, height):
        """
        Cube constructor
        :param row: int
        :param col: int
        :param val: int
        :param width: int
        :param height: int
        :return: None
        """
        self.row = row
        self.col = col
        self.val = val
        self.temp = 0                       # temporary value
        self.is_grid = False                # immutable or can be changed during game
        self.width = width                  # single cube width
        self.height = height                # single cube height
        self.selected = False               
        self.help_cells_highlight = False   # to highlight horizontal, vertical and 3x3 around cells
        self.same_number_highlight = False  # to highlight errors
        self.same_number_exists = False     # to highlight other number with a given value
        self.correct = 0                    # green in sudoku correctly solved, red otherwise

    def draw(self, win):
        """
        Cube constructor
        :param win: pygame window
        :return: None
        """
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
        elif(self.temp != 0):
            size = 35
            s = self.temp
            pos_x = x + 5
            pos_y = y + 5
            
        # color the cell based on the game state during game
        if(self.selected):
            pygame.draw.rect(win, (204, 255, 255), (x, y, self.width, self.height))
        elif(self.same_number_exists):
            pygame.draw.rect(win, (225, 168, 168), (x, y, self.width + 2, self.height + 2))
        elif(self.help_cells_highlight):
            pygame.draw.rect(win, (235, 235, 235), (x, y, self.width, self.height))
        elif(self.same_number_highlight):
            pygame.draw.rect(win, (225, 225, 250), (x, y, self.width, self.height))
        
        # color the cell text at the end of the game
        if(self.correct == 1):
            color = (0, 200, 0)
        elif(self.correct == 2):
            color = (200, 0, 0)

        font = pygame.font.SysFont('Comic Sans MS', size)
        string = font.render(str(s), 1, color)
        win.blit(string, (pos_x, pos_y))


class Grid:
    """
    This class handles the the whole grid
    """
    def __init__(self, win, width, height, row, col):
        """
        Grid constructor
        :param win: pygame window
        :param width: int
        :param height: int
        :param row: int
        :param col: int
        :return: None
        """
        self.win = win
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = None

        single_width = self.width / self.row        # dimension of each 1x1 cell
        single_height  = self.height / self.col
        self.cubes = [[Cube(i, j, 0, single_width, single_height) for j in range(self.col)] for i in range(self.row)]

    def reset(self):
        """
        This function reset the temporary and the final values of every cell to play a game with the same grid
        :return: None
        """
        for i in range(0, self.row):
            for j in range(0, self.col):
                if(not self.cubes[i][j].is_grid):
                    self.cubes[i][j].temp = 0
                    self.cubes[i][j].val = 0
                self.cubes[j][i].correct = 0
    
    def new_game(self):
        """
        This function clear the status to play another game with a new grid
        :return: None
        """
        for i in range(0, self.row):
            for j in range(0, self.col):
                    self.cubes[i][j].temp = 0
                    self.cubes[i][j].val = 0
                    self.cubes[i][j].is_grid = False
                    self.cubes[i][j].selected = False
                    self.cubes[j][i].correct = False
        self.selected = None
    
    def fix_grid(self):
        """
        This function fix the grid allowing the user to create a personal sudoku with an immutable grid
        :return: None
        """
        gr = []
        for i in range(0, self.row):
            temp = []
            for j in range(0, self.col):
                if(self.cubes[i][j].val != 0):
                    self.cubes[i][j].is_grid = True
                    self.cubes[i][j].color = (100, 100, 100)
                temp.append(self.cubes[i][j].val)
            gr.append(temp)

    def de_highlight(self):
        """
        This function removes the cells highlight that helps the user
        :return: None
        """
        for i in range(0, self.row):
            for j in range(0, self.col):
                self.cubes[i][j].same_number_highlight = False
                self.cubes[i][j].same_number_exists = False
    
    def highlight(self):
        """
        This function based on the currently selected value highlight cells to help the user
        :return: None
        """
        row, col = self.selected
        val = self.cubes[row][col].val

        # highlights other cell with the same value of the selected one and clears the state of the cells
        for i in range(0, self.row):
            for j in range(0, self.col):
                if(self.cubes[i][j].val == val and val != 0):
                    self.cubes[i][j].same_number_highlight = True
                else:
                    self.cubes[i][j].same_number_highlight = False
                self.cubes[i][j].help_cells_highlight = False
                self.cubes[i][j].same_number_exists = False

        for j in range(0, self.row):
            # highlights cells in the same row
            if(j != col):
                if(self.cubes[row][j].val == val and val != 0):
                    self.cubes[row][j].same_number_exists = True
                self.cubes[row][j].help_cells_highlight = True
            # highlights cells in the same col
            if(j != row):
                if(self.cubes[j][col].val == val and val != 0):
                    self.cubes[j][col].same_number_exists = True
                self.cubes[j][col].help_cells_highlight = True

        # highlights cell in the 3x3 square around the selected cell
        small_row = floor(row / 3) * 3
        small_col = floor(col / 3) * 3
        
        for i in range(small_row, small_row + 3):
            for j in range(small_col, small_col + 3):
                self.cubes[i][j].help_cells_highlight = True
                if(self.cubes[i][j].val == val and val != 0):
                    self.cubes[i][j].same_number_exists = True
                else:
                    self.cubes[i][j].same_number_exists = False

    def set_temp(self, k):
        """
        This function modifies the temporary value of modifiable cells
        :param k: int
        :return: None
        """
        if(self.selected):
            i = self.selected[0]
            j = self.selected[1]
            if(not self.cubes[i][j].is_grid):
                self.cubes[i][j].temp = k
                self.cubes[i][j].val = 0
    
    def set_val(self, k):
        """
        This function modifies the value of modifiable cells or makes the temporary become actual
        :param k: int
        :return: int
        """
        if(self.selected):
            i, j = self.selected
            if(k == 0):
                k = self.cubes[i][j].temp
            self.cubes[i][j].val = k
            self.highlight()
        return k
    
    def select(self, ii, jj):
        """
        This function sets the clicked cell as selected and updates the status
        :param ii: int
        :param jj: int
        :return: None
        """
        # clear the status
        for i in range(0, self.row):
            for j in range(0, self.col):
                self.cubes[i][j].selected = False

        self.cubes[ii][jj].selected = True
        self.selected = (ii, jj)
        self.highlight()                    # to help the user with the highlight
    
    def random(self):
        """
        This function uses a json file to load a random sudoku game
        :return: None
        """
        with open('grids.json', 'r') as f:
            data = json.load(f)
        i = str(randint(0, len(data.keys()) - 1))
        sudoku_grid = data[i]
        for i in range(len(sudoku_grid)):
            for j in range(len(sudoku_grid[0])):
                self.cubes[i][j].val = sudoku_grid[j][i]
        self.fix_grid()

    def check_solution(self):
        """
        This function checks if the user solution is the correct one
        :return: bool
        """
        start_grid = []
        grid = []
        # creates a list for the full user grid and a list of the fixed grid
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

        # compare the correct solution with the user one
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

        # sets the bool to color the final stage
        for i in range(0, self.row):
            for j in range(0, self.col):
                self.cubes[j][i].correct = result
        return correct

    def count_free_cubes(self):
        """
        This function counts how many cells have a value: if all do, then the grid is full and we can check the result
        :return: int
        """
        count = DIM * DIM
        for i in range(0, self.row):
            for j in range(0, self.col):
                if(self.cubes[i][j].val != 0):
                    count -= 1
        return count

    def get_clicked_cube(self, mouse_pos):
        """
        This function finds and returns the cell based on the mouse point where the user has clicked
        :param mouse_pos: (i, j)
        :return: (i, j)
        """
        space_x = self.width / self.row
        space_y = self.height / self.col

        i = floor(mouse_pos[0] / space_x)
        j = floor(mouse_pos[1] / space_y)

        return (i, j)

    def draw(self):
        """
        This function draws both the grid and the dividing lines to compose the sudoku
        :return: None
        """
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
        # draw final border to separate grid from user panel
        pygame.draw.line(self.win, BORDER_COLOR, (0, 9 * space), (self.width, 9 * space), 5)

def get_formatted_time(s):
    """
    This function gets an amount of seconds started when the game began and converts it to minutes:second format
    :param s: float
    :return: string
    """
    seconds = int(s % 60)
    minutes = int(s / 60)
    # hours = int(minutes / 60)

    return ('{0}:{1}').format(minutes, seconds)

class Button:

    def __init__(self, c, cc, x, y, w, h, f=None, text=''):
        """
        Button constructor
        :param c: pygame color
        :param cc: pygame color
        :param x: int
        :param y: int
        :param w: int
        :param h: int
        :param f: function
        :param text: string
        :return: None
        """
        self.text = text
        self.color = c
        self.color_list = [c, cc]
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.fun = f

    def draw(self, win, outline=None):
        """
        This function draws the button and the text inside it
        :param win: pygame window
        :param outlin: bool
        :return: None
        """
        if(outline):
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if(self.text != ''):
            button_font = pygame.font.SysFont('Comic Sans MS', 45)
            text = button_font.render(str(self.text), 1, (100, 100, 100))
            pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height), 0)
            
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        """
        This function checks if the mouse click or mouse position are over the button and returns a bool and the
        text of the controlled button
        :param pos: (i, j)
        :return: (bool, string)
        """
        self.color = self.color_list[0]
        if(pos[0] > self.x and pos[0] < self.x + self.width):
            if pos[1] > self.y and pos[1] < self.y + self.height:
                self.color = self.color_list[1]
                return (True, self.text)

        return (False, self.text)


class Sudoku_GUI:
    """
    This class handles the whole sudoku game and the user interactions
    """
    def __init__(self, width, height):
        """
        Sudoku GUI constructor
        :param width: int
        :param height: int
        :return: None
        """
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Sudoku Solver')
        self.grid = Grid(self.win, self.width, self.width, DIM, DIM)
        self.started = False
        self.finished = False
        self.moves_list = []
        self.moves_index = 0

        # buttons creation
        new_btn = Button(BLUE_BUTTON_OFF, BLUE_BUTTON_ON, 20, self.height - 105, 170, 70, f=self.grid.new_game, text='New game')
        random_btn = Button(GREEN_BUTTON_OFF, GREEN_BUTTON_ON, 220, self.height - 105, 190, 70, f=self.grid.random, text='Random')
        reset_btn = Button(GREEN_BUTTON_OFF, GREEN_BUTTON_ON, 220, self.height - 105, 190, 70, f=self.grid.reset, text='Restart')
        start_btn = Button(BLUE_BUTTON_OFF, BLUE_BUTTON_ON, 20, self.height - 105, 170, 70, f=self.grid.fix_grid, text='Start game')
        self.b = [new_btn, reset_btn, random_btn, start_btn]

        # start the game loop
        self.execute()

    def handle_key_press(self, event):
        """
        This function handles the key press and return the number pressed by the user
        :param event: pygame event
        :return: int
        """
        key = 0
        # int to insert numbers
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

        # checks if the user wants to delete the cell value if it is mutable
        if((event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE) and not self.finished):
            i, j = self.grid.selected
            if(not self.grid.cubes[i][j].is_grid):
                self.grid.set_val(0)
            self.grid.set_temp(0)
            self.grid.de_highlight()
            self.grid.highlight()

        # checks if the user presses Ctrl+Z to undo the insertions
        if(self.started and not self.finished):
            if(event.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL)):
                self.move_backward()

        return key
    
    def move_backward(self):
        """
        This function performs the sudoku-state undo when the user presses Ctrl+Z
        :return: None
        """
        if(not self.moves_list):        # no states available. State = [(i, j), val] -> val inserted in cell (i, j)
            return
        
        self.moves_index -= 1           # index to move inside the states-list
        
        if(self.moves_index < 0):
            self.moves_index = 0
            return
        (i, j), val = self.moves_list[self.moves_index]
        
        self.grid.cubes[i][j].val = 0
        if(not self.grid.cubes[i][j].is_grid):
            self.grid.cubes[i][j].temp = 0
        
        # remove the last element
        self.moves_list.pop()
        # de-highlights and the highlights based on the current user selection
        self.grid.de_highlight()
        self.grid.highlight()

    def move_cursor(self, key, event):
        """
        This function moves the selected cell according to the arrow keys pressed by the user and returns the value
        of the new position to set it again if the game is not started yed
        :param key: int
        :param event: pygame window
        :return: int
        """
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
        """
        This function is the main loop of the game
        :return: None
        """
        self.run = True
        start = time.time()
        self.playing_time = 0

        while(self.run):
            clock = pygame.time.Clock()
            clock.tick(60)

            # starts the timer and shows different button combinations depending on the game is started or not yet
            if(self.started):
                if(not self.finished):
                    self.playing_time = time.time() - start
                self.buttons = self.b[:-2]
            else:
                self.playing_time = 0
                self.buttons = self.b[-2:]

            pos = pygame.mouse.get_pos()

            if(self.grid.selected):
                i, j = self.grid.selected
                key = self.grid.cubes[i][j].val
            else:
                key = 0
            
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    self.run = False

                if(event.type == pygame.KEYDOWN):
                    key = self.handle_key_press(event)    # handle numbers
                    
                    if(self.grid.selected):                 # handle moving selection with arrow keys if a cell was selected
                        key = self.move_cursor(key, event)
                    
                    if(not self.started):                   # user can setup custom grid witoput temporary values
                        self.grid.set_val(key)
                    else:
                        if(key != 0):
                            self.grid.set_temp(key)         # user sets the temporary value first
                            
                        if(event.key == pygame.K_RETURN):   # temp val becomes fixed after RETURN only
                            if(self.grid.cubes[i][j].val != 0):
                                key = self.grid.cubes[i][j].val

                            v = self.grid.set_val(key)
                            self.moves_list.append([(i, j), v]) # to save the state changes and perform the undo
                            self.moves_index += 1               # index for the undo operation

                            if(self.grid.count_free_cubes() == 0):  # the last RETURN completed the whole grid -> check the result
                                if(self.grid.check_solution()):
                                    self.finished = True
                    
                if(event.type == pygame.MOUSEMOTION):               # changes the button color when the mouse is over it
                    for b in self.buttons:
                        if(b.is_over(pos)[0]):
                            b.color = b.color_list[1]
                        else:
                            b.color = b.color_list[0]

                if(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):     # user left click
                    if(pos[1] > WIDTH):     # check button click
                        for b in self.buttons:
                            if(b.is_over(pos)[0]):
                                b.fun()
                                # reset the state and the timer depending on the clicked button 
                                if(b.is_over(pos)[1] == 'New game'):
                                    self.started = False
                                    self.finished = False
                                    self.moves_index = 0
                                    self.moves_list = []
                                elif(b.is_over(pos)[1] == 'Start game' or b.is_over(pos)[1] == 'Random'):
                                    self.started = True
                                    self.finished = False
                                    start = time.time()
                                    self.moves_index = 0
                                    self.moves_list = []
                                elif(b.is_over(pos)[1] == 'Restart' or b.is_over(pos)[1] == 'Solve'):
                                    start = time.time()
                                    self.finished = False
                                    self.moves_index = 0
                                    self.moves_list = []
                                    
                    else:                   # check grid click
                        i, j = self.grid.get_clicked_cube(pos)
                        self.grid.select(i, j)

            self.draw()
            pygame.display.update()

        pygame.quit()

    def draw(self):
        """
        This function calls the draw() of each object involved in the game
        :return: None
        """
        self.win.fill((255,255,255))
        # draw the sudoku grid
        self.grid.draw()
        space = self.width / DIM

        # draw the timer value
        font = pygame.font.SysFont('Comic Sans MS', 45)
        string = font.render('Elapsed time:  ' + get_formatted_time(self.playing_time), 1, (51, 153, 255))
        self.win.blit(string, (self.width / 2 + 80, 9 * space + 55))

        # draw the buttons
        for b in self.buttons:
            b.draw(self.win, 1)

        
g = Sudoku_GUI(WIDTH, HEIGHT)
