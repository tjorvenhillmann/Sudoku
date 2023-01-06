from random import randint, shuffle
from time import time

class Generator:
    '''
    Generator Class is the logic of a Sudoku Game. The Class contains the main funkctions of the Sudoku.
    The Generator is build with the fillGrid and the reduceGrid function.
    The Solver function will solve a Sudoku Puzzle and find a possible Solution using a Brute-Force (Backtracking) Algorithm.

    To use the Generator more efficiently our GUI we have the Sudoku function.
    '''
    def __init__(self) -> None:
        # Counter variable for reduce Grid
        self.counter = 1

        # Initialise empty 9x9 grid
        self.grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0]]


    def checkGrid(self, grid:list) -> bool:
        '''
        This function checks every cell for a value other than zero -> validation
        '''
        # iter trough grid
        for row in range(0,9):
            for col in range(0,9):
                # Grid is not solved completely
                if grid[row][col] == 0:
                    return False
        # The grid is complete
        return True
    
    def checkSquare(self, grid:list, row:int, col:int) -> list:
        '''
        This Function will return a list of the numbers from the 3x3 sqaure in that the cell is located
        '''

        # Check in 3x3 Square
        c0 = (col//3)*3
        r0 = (row//3)*3
        square = []
        for r in range(3):
            for c in range(3):
                square.append(self.grid[r0+r][c0+c]) 
        return square

    def solveGrid(self, grid:list) -> bool:
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
                            # Empty square is an a 2D-list
                            square = self.checkSquare(grid, row, col)
                            
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
                            square = self.checkSquare(self.grid, row, col)
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

    def print_board(self) -> None:
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

    def reduceGrid(self, remaining:int) -> None:
        '''
        remaining: int, control difficultness

        This Function will remove numbers from the grid by setting them to 0.
        The difficult level is controlled by the remaining numbers in the puzzle.
        17 is the minimum, because it´s the limit for a Puzzle with only one solution, will take a lot of time to generate, Python is not high performing enough.
        '''
        # start value of numbers in puzzle, because grid is filled complete
        clues = 81
        while clues >= remaining:
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
            # copyGrid = dc(self.grid)
            copyGrid = []
            for r in range(0,9):
                copyGrid.append([])
                for c in range(0,9):
                    copyGrid[r].append(self.grid[r][c])
            
            # Count the number of solutions that this grid has
            self.counter = 0      
            self.solveGrid(copyGrid)   
            # If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
            if self.counter != 1:
                self.grid[row][col] = backup
            
            # one number less in the puzzle
            else:
                clues -= 1
    
    def sudoku(self, remaining:int)->tuple:
        '''
        remaining: int, control difficultness
        This Function is a helper so you can create a new Puzzle in different Difficult-Levels by one call.
        '''
        # Return Method for Sudoku game, the solved and the game board are returned in a tuple, to do so we need a complete copy
        # Generatetd Full Board == Solved Board
        self.fillGrid()
        solved_board = []
        for r in range(0,9):
                solved_board.append([])
                for c in range(0,9):
                    solved_board[r].append(self.grid[r][c])
        # Reduce the numbers of the Board, depends on level
        self.reduceGrid(remaining)
        game_board = []
        for r in range(0,9):
                game_board.append([])
                for c in range(0,9):
                    game_board[r].append(self.grid[r][c])
        
        return solved_board, game_board

def testing():
    # From empty grid to a solvable puzzle
    g = Generator()
    time_start = time()
    g.fillGrid()
    time_end = time()
    print(f"Time to generate grid: {time_end - time_start} secs")
    g.print_board()
    print()
    time_start = time()
    g.reduceGrid(36)
    time_end = time()
    print(f"Time to reduce grid: {time_end - time_start} secs")
    g.print_board()
    count = 0
    for row in g.grid:
        for element in row:
            if element != 0:
                count += 1
    
    print("\nRemaining Numbers:", count)

if __name__ == "__main__":
    testing()