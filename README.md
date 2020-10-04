# GUI-sudoku-solver
This application allows to solve a sudoku both with a GUI and a terminal version. Throught the GUI the user can insert its own sudoku grid, solve it and the application compares its result with the correct one, or try a random game.  
Run sudoku_GUI.py for the GUI version, or the main(terminal).py for the textual version after editing the python file to insert your own sudoku grid.
# Instruction
*Before starting* to play:  
Button **Start game** --> after the user has entered the initial values of the sudoku to be solved, press this button to freeze the grid and start playing  
Button **Random** --> generates a random sudoku and starts the game  
When inserting your own grid there is no need to hit ENTER, just press the number on your keyboard.  

When the game is *running*:  
Button **New game** --> creates a new empty grid and allows the withdrawal  
Button **Reset** --> restarts the grid from the initial one, thus removing only the user tries  

Click a cell to select it, or reach it by moving the selection with the arrow keys, hit the number on your keyboard to make it temporary. Hit ENTER to make it final.  
Press **DELETE** or **BACKSPACE** to delete both a temporary or stable value.  
Press **Ctrl+Z** to undo the last moves.

# Utilities
The application highlights the row, column and 3x3 grid surrounding the selected cell to help the user. It also highlights in blue cells with the same number throughout the grid for graphical help and shows them in red in case of an error.  

# Examples
![Correct grid](https://github.com/fcondo/GUI-sudoku-solver/blob/master/Examples/1.png " Example 1") 
![Error in grid](https://github.com/fcondo/GUI-sudoku-solver/blob/master/Examples/2.png " Example 2")
