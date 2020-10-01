"""
    main(terminal).py

    Author: Fabio Condomitti
"""
from solver import print_grid, solve

def main():
    sudoku_grid = [ [0,8,0,  0,0,0,  2,0,0],
                    [0,0,0,  0,8,4,  0,9,0],
                    [0,0,6,  3,2,0,  0,1,0],
                    
                    [0,9,7,  0,0,0,  0,8,0],
                    [8,0,0,  9,0,3,  0,0,2],
                    [0,1,0,  0,0,0,  9,5,0],
                    
                    [0,7,0,  0,4,5,  8,0,0],
                    [0,3,0,  7,1,0,  0,0,0],
                    [0,0,8,  0,0,0,  0,4,0]
                ]

    print_grid(sudoku_grid)
    print('....................................')
    copy = sudoku_grid
    solve(copy)
    print_grid(copy)

if __name__ == "__main__":
    main()