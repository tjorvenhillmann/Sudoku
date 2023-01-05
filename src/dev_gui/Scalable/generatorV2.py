from random import randint, shuffle
from time import time

class Generator:
    def __init__(self) -> None:
        # Initialise empty 9 by 9 grid
        self.grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # Counter variable for the 
        self.counter = 1


    def checkGrid(self, grid):
        # This function checks every cell for a value other than zero
        for row in range(0,9):
            for col in range(0,9):
                if grid[row][col] == 0:
                    return False

        # The grid is complete 
        return True
    
    def checkSquare(self, grid:list, row:int, col:int) -> list:
        #Check in 3x3 Square
        c0 = (col//3)*3
        r0 = (row//3)*3
        square = []
        for r in range(3):
            for c in range(3):
                square.append(self.grid[r0+r][c0+c]) 
        return square

    def solveGrid(self, grid):
        # Find next empty cell to solve
        for i in range(0,81):
            row = i//9 # Needed to get on 9th cell row = 1 and thats the 2nd row of the grid 
            col = i%9  # No integer divison because columns are not affected by line break 
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
                break
        grid[row][col] = 0

    def fillGrid(self):
        # Number list needed for the shuffel function
        numberList = [1,2,3,4,5,6,7,8,9]
        # Find next empty cell to solve
        for i in range(0,81):
            row = i//9 # Needed to get on 9th cell row = 1 and thats the 2nd row of the grid 
            col = i%9  # No integer divison because columns are not affected by line break 
            if self.grid[row][col] == 0:
                shuffle(numberList)
                for value in numberList:
                    # Check that this number is not alreday used in this row
                    if value not in self.grid[row]:
                        # Check if this number is not already used in this column
                        if value not in (self.grid[r][col] for r in range(9)):

                            # Identify in which of the 9 squares were are working
                            # Empty square is an a 2D-list 
                            square = self.checkSquare(self.grid, row, col)
                            # Check that this number is not already be used on this 3x3 square
                            if value not in (square):
                                self.grid[row][col] = value
                                if self.checkGrid(self.grid):
                                    return True
                                else:
                                    if self.fillGrid():
                                        return True 
                break
        #Setting back to Zero
        self.grid[row][col] = 0

    def print_board(self):
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

    def reduceGrid(self, remaining):
        # Start by removing numbers from random cells
        # With increased number of attemps more numbers are getting removed
        # This increases the difficulty
        clues = 81
        while clues >= remaining:
            #Select a random cell that is not already empty
            row = randint(0,8)
            col = randint(0,8)
            while self.grid[row][col] == 0:
                row = randint(0,8)
                col = randint(0,8)
            # Remember its cell value in case we need to put it back  
            backup = self.grid[row][col]
            self.grid[row][col] = 0
            
            # Take a full copy of the grid
            #copyGrid = dc(self.grid)
            copyGrid = []
            for r in range(0,9):
                copyGrid.append([])
                for c in range(0,9):
                    copyGrid[r].append(self.grid[r][c])
            
            # Count the number of solutions that this grid has (using a backtracking approach implemented in the solveGrid() function)
            self.counter = 0      
            self.solveGrid(copyGrid)   
            # If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
            if self.counter != 1:
                self.grid[row][col] = backup
                #We could stop here, but we can also have another attempt with a different cell just to try to remove more numbers
                #attempts -= 1
            else:
                clues -= 1
    
    def sudoku(self, remaining:int)->tuple:
        #Return Method for Sudoku game, the solved and the game board are returned in a tuple, to do so we need a complete copy
        #Generatetd Full Board == Solved Board
        self.fillGrid()
        solved_board = []
        for r in range(0,9):
                solved_board.append([])
                for c in range(0,9):
                    solved_board[r].append(self.grid[r][c])
        #Reduce the numbers of the Board, depends on level
        self.reduceGrid(remaining)
        game_board = []
        for r in range(0,9):
                game_board.append([])
                for c in range(0,9):
                    game_board[r].append(self.grid[r][c])
        boards = (solved_board, game_board)

        return(boards)


def testing():
    # From empty grid to a solvable puzzle
    g = Generator()
    time_start = time()
    g.fillGrid()
    time_end = time()
    print(f"Time to fill grid: {time_end - time_start} secs")
    g.print_board()
    print()
    time_start = time()
    g.reduceGrid()
    time_end = time()
    print(f"Time to reduce grid: {time_end - time_start} secs")
    g.print_board()
    print("Sudoku Grid Ready")

def boardGenerator(clues):
    g = Generator()
    boards = g.sudoku(clues)
    solved, game = boards

    return game, solved

if __name__ == "__main__":
    game, solved = boardGenerator(35)
    count = 0
    for i in game:
        for element in i:
            if element != 0:
                count += 1
    
    print(count)
    print('Game: ', game)
    print('Solved: ', solved)