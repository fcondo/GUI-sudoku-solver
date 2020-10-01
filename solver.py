"""
    solver.py

    Author: Fabio Condomitti
"""

from math import floor

DIM = 9

def print_grid(gr):
    """
    Prints a sudoku grid
    :param gr: 2D list
    :return: None
    """
    for i in range(0,9):
        if((i % 3) == 0):
            print('- - - - - - - - - - - - - - - -')
        for j in range(0,9):
            if((j % 3) == 0):
                print('|', end='')
            
            val = str(gr[i][j])
            if(val == '0'):
                val = ' '
            
            print(' ' + val + ' ', end = '')
        print('|')
    print('- - - - - - - - - - - - - - - -')

def find_empty_cells(gr):
    """
    Collects all the (i,j) free couples of the grid 
    :param gr: 2D list
    :return: list
    """
    l = list()
    for i in range(0,9):
        for j in range(0,9):
            if(gr[i][j] == 0):
                l.append([i, j])
    return l

def check_dim(gr):
    """
    Checks if it is a 9x9 grid 
    :param gr: 2D list
    :return: None
    """
    l = len(gr)
    if(l != DIM):
        return False

    for i in range(0, DIM):
        if(len(gr[i]) != l):
            return False 
    return True

def solve(gr):
    """
    Solves the sudoku
    :param gr: 2D list
    :return: None
    """
    
    # dimension check
    if(not check_dim(gr)):
        print('ERROR in the grid dimension')
        return

    available_cells = find_empty_cells(gr)
    pos = 0
    
    while(pos < len(available_cells)):
        i, j = available_cells[pos]
        valid_num = False

        if(gr[i][j] == 0):
            start = 1
        else:
            start = gr[i][j]

        for num in range(start, len(gr) + 1):
            if(is_valid(gr, available_cells[pos], num)):
                gr[i][j] = num
                pos += 1
                valid_num = True
                break

        if(not valid_num):    
            gr[i][j] = 0
            pos -= 1
            i = available_cells[pos][0]
            j = available_cells[pos][1]
            gr[i][j] += 1
        
def is_valid(gr, pos, num):
    """
    Checks if a given number can be put in the pos (i, j) position of the grid 
    :param gr: 2D list
    :param pos: (row, col)
    :param num: int
    :return: bool
    """
    
    row = pos[0]
    col = pos[1]
    
    for i in range(0, 9):
        # test row
        if(i != col and gr[row][i] == num):
            return False
        # test col
        if(i != row and gr[i][col] == num):
            return False

    # test 3x3 square
    small_row = floor(row / 3) * 3
    small_col = floor(col / 3) * 3

    for i in range(small_row, small_row + 3):
        for j in range(small_col, small_col + 3):
            if((i != row and j != col) and gr[i][j] == num):
                return False
    
    return True

