from random import randint, shuffle
from time import time
from copy import deepcopy

class Generator:
    '''
    Generator Class is the logic of a Sudoku Game. The Class contains the main funkctions of a Sudoku.
    This class contains the following functions:
    - checkGrid
    - getSquare
    - solveGrid
    - fillGrid
    - printBoard
    - reduceGrid
    - sudoku

    The Generator is build with the fillGrid and the reduceGrid function.
    The Solver function will solve a Sudoku Puzzle and find a possible Solution using a Brute-Force (back-tracking) algorithm.

    To use the Generator more efficiently in our GUI we have the sudoku function.
    '''

    def __init__(self) -> None:
        # Counter variable for possible Solutions
        self.counter = 0
        # Initialise empty 9x9 grid
        self.grid = [[0]*9 for x in range(9)]


    def checkGrid(self, grid:list) -> bool:
        '''
        grid: list, contains the sudoku puzzle
        This function checks every cell for a value other than zero
        This function will return a bool to valid the grid.
        '''
        # iter trough grid
        for row in range(0,9):
            for col in range(0,9):
                # Grid is not solved completely
                if grid[row][col] == 0:
                    return False
        return True
    
    def getSquare(self, grid:list, row:int, col:int) -> list:
        '''
        grid: list, contains the sudoku puzzle
        row: int, actual row of the cell
        col: int, actual column of the cell
        This Function will return a list of the numbers from the 3x3 sqaure in that the cell is located
        '''
        # Check in 3x3 Square
        c0 = (col//3)*3
        r0 = (row//3)*3
        square = []
        for r in range(3):
            for c in range(3):
                square.append(grid[r0+r][c0+c]) 
        return square

    def solveGrid(self, grid:list) -> bool:
        '''
        grid: list, contains sudoku puzzle to solve
        This Function will solve a sudoku by using a Brute-Force algorithm.
        The algorithm will iter trough the empty cells and try if the value does fit. If not, back-tracking takes place and we restart the process.
        This Function returns a bool, in this way we can use it recursive.
        '''
        # Find next empty cell to solve
        for i in range(0,81):
            # iter trough grid by integer division for rows and modulo for colums to avoid for-loops and tabs(increases readability)
            row = i//9
            col = i%9
            if grid[row][col] == 0:
                for value in range(1,10):
                    # Check that this number is not alreday used in this row
                    if value not in grid[row]:
                        # Check if this number is not already used in this column
                        if value not in (grid[r][col] for r in range(9)):
                            # Identify in which of the 9 squares were are working
                            square = self.getSquare(grid, row, col)
                            
                            # Check that this number is not already be used on this 3x3 square
                            if value not in (square):
                                grid[row][col] = value
                                if self.checkGrid(grid):
                                    self.counter += 1
                                    break
                                else:
                                    if self.solveGrid(grid):
                                        return True
                # all possibilities are done
                break
        # Setting back to Zero
        grid[row][col] = 0

    def fillGrid(self) -> bool:
        '''
        This Function will fill a blank grid. Therefore it will generate a random solution for the empty sudoku puzzle.
        The variation of the Puzzle comes trough the shuffeling of the numbers 1-9 for each cell.
        This function works with recursion, so it repeates itself. When there is no possible solution, the back-tracking will start and put the values back to zero (empty cell).
        This Function returns a bool, in this way we can use it recursive.
        '''
        # Number list needed for the shuffel function
        numberList = [1,2,3,4,5,6,7,8,9]
        # Find next empty cell to solve
        for i in range(0,81):
            # iter trough grid by integer division for rows and modulo for colums to avoid for-loops and tabs(increases readability)
            row = i//9
            col = i%9 
            if self.grid[row][col] == 0:
                # randomly "sort" 1-9
                shuffle(numberList)
                for value in numberList:
                    # Check that this number is not alreday used in this row
                    if value not in self.grid[row]:
                        # Check if this number is not already used in this column
                        if value not in (self.grid[r][col] for r in range(9)):
                            # Identify in which of the 9 squares were are working
                            square = self.getSquare(self.grid, row, col)

                            # Check that this number is not already be used on this 3x3 square
                            if value not in (square):
                                self.grid[row][col] = value
                                #all cells filled
                                if self.checkGrid(self.grid):
                                    return True
                                else:
                                    if self.fillGrid():
                                        return True 
                # all possibilities are done, back tracking
                break
        # Setting back to Zero
        self.grid[row][col] = 0

    def printBoard(self) -> None:
        # Function to print a Game Board not in the list output in the terminal
        for i in range(len(self.grid)):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - -  ")
            for j in range(len(self.grid[0])):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                if j == 8:
                    print(self.grid[i][j])
                else:
                    print(str(self.grid[i][j]) + " ", end="")

    def reduceGrid(self, remaining:int) -> float:
        '''
        remaining: int, control difficultness

        This Function will remove numbers from the grid by setting them to 0.
        The difficult level is controlled by the remaining numbers in the puzzle.
        17 is the minimum, because it`s the limit for a Puzzle with only one solution, will take a lot of time to generate, Python is not high performing enough.
        This function returns the time in ms, that the solver needs to solve the puzzle
        '''
        # start value of numbers in puzzle, because grid is filled complete
        clues = 81
        while clues > remaining:
            # Select a random cell that is not already empty
            row = randint(0,8)
            col = randint(0,8)
            while self.grid[row][col] == 0:
                row = randint(0,8)
                col = randint(0,8)

            # Remember its cell value in case we need to put it back, then remove it  
            backup = self.grid[row][col]
            self.grid[row][col] = 0
            
            # Take a full copy of the grid
            copyGrid = deepcopy(self.grid)
            
            # Count the number of solutions that this grid has
            self.counter = 0
            start_time = time()  
            self.solveGrid(copyGrid)
            end_time = time()   
            # If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
            if self.counter != 1:
                self.grid[row][col] = backup
            
            # one number less in the puzzle
            else:
                clues -= 1
        # Solver Time in ms
        solverTime = (end_time-start_time)*1000
        return solverTime
    
    def sudoku(self, remaining:int)->tuple:
        '''
        remaining: int, control difficultness
        This Function is a helper, so you can create a new Puzzle in different Difficult-Levels by one call.
        The Function returns a tuple, wich contains the solved grid, game grid and solver time.
        '''
        # Generatetd Full Board == Solved Board
        self.fillGrid()
        solved_board = deepcopy(self.grid)
        # Reduce the numbers of the Board, depends on level
        solver_time = self.reduceGrid(remaining)
        game_board = deepcopy(self.grid)
        
        return solved_board, game_board, solver_time

def testing():
    # From empty grid to a solvable puzzle
    g = Generator()
    time_start = time()
    g.fillGrid()
    time_end = time()
    print(f"Time to generate grid: {time_end - time_start} secs")
    g.printBoard()
    time_start = time()
    solver_time = g.reduceGrid(30)
    time_end = time()
    print(f"\nTime to reduce grid: {time_end - time_start} secs")
    g.printBoard()
    print(f"\nTime to solve reduced grid: {solver_time} msecs")
    count = 0
    for row in g.grid:
        for element in row:
            if element != 0:
                count += 1
    
    print(f"Remaining Numbers: {count}\n")

if __name__ == "__main__":
    testing()