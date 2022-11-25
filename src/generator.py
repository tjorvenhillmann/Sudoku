from random import randint, shuffle
from time import sleep

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

        # Value for difficulty
        self.attempts = 5

    def checkGrid(self, grid):
        # This function checks every cell for a value other than zero
        for row in range(0,9):
            for col in range(0,9):
                if grid[row][col] == 0:
                    return False

        # The grid is complete 
        return True

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
                        if value not in (grid[0][col],
                                         grid[1][col],
                                         grid[2][col],
                                         grid[3][col],
                                         grid[4][col],
                                         grid[5][col],
                                         grid[6][col],
                                         grid[7][col],
                                         grid[8][col]):
                            # Identify in which of the 9 squares were are working
                            # Empty square is an a 2D-list 
                            square = []
                            # Top squares 3x3
                            if row < 3: 
                                if col < 3:
                                    square = [grid[k][0:3] for k in range(0,3)]
                                elif col < 6:
                                    square = [grid[k][3:6] for k in range(0,3)]
                                else:
                                    square = [grid[k][6:9] for k in range(0,3)]
                            # Middle squares 3x3
                            elif row < 6:  
                                if col < 3:
                                    square = [grid[k][0:3] for k in range(3,6)]
                                elif col < 6:
                                    square = [grid[k][3:6] for k in range(3,6)]
                                else:
                                    square = [grid[k][6:9] for k in range(3,6)]
                            # Bottom squares 3x3
                            else: 
                                if col < 3:
                                    square = [grid[k][0:3] for k in range(6,9)]
                                elif col < 6:
                                    square = [grid[k][3:6] for k in range(6,9)]
                                else:
                                    square = [grid[k][6:9] for k in range(6,9)]
                            
                            # Check that this number is not already be used on this 3x3 square
                            if value not in (square[0] + square[1] + square[2]):
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
                        if value not in (self.grid[0][col],
                                         self.grid[1][col],
                                         self.grid[2][col],
                                         self.grid[3][col],
                                         self.grid[4][col],
                                         self.grid[5][col],
                                         self.grid[6][col],
                                         self.grid[7][col],
                                         self.grid[8][col]):
                            # Identify in which of the 9 squares were are working
                            # Empty square is an a 2D-list 
                            square = []
                            # Top squares 3x3
                            if row < 3: 
                                if col < 3:
                                    square = [self.grid[k][0:3] for k in range(0,3)]
                                elif col < 6:
                                    square = [self.grid[k][3:6] for k in range(0,3)]
                                else:
                                    square = [self.grid[k][6:9] for k in range(0,3)]
                            # Middle squares 3x3
                            elif row < 6:  
                                if col < 3:
                                    square = [self.grid[k][0:3] for k in range(3,6)]
                                elif col < 6:
                                    square = [self.grid[k][3:6] for k in range(3,6)]
                                else:
                                    square = [self.grid[k][6:9] for k in range(3,6)]
                            # Bottom squares 3x3
                            else: 
                                if col < 3:
                                    square = [self.grid[k][0:3] for k in range(6,9)]
                                elif col < 6:
                                    square = [self.grid[k][3:6] for k in range(6,9)]
                                else:
                                    square = [self.grid[k][6:9] for k in range(6,9)]
                            
                            # Check that this number is not already be used on this 3x3 square
                            if value not in (square[0] + square[1] + square[2]):
                                self.grid[row][col] = value
                                if self.checkGrid(self.grid):
                                    return True
                                else:
                                    if self.fillGrid():
                                        return True 
                break
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

    def reduceGrid(self):
        # Start by removing numbers from random cells
        # With increased number of attemps more numbers are getting removed
        # This increases the difficulty
        while self.attempts > 0:
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
                self.attempts -= 1


def main():
    # From empty grid to a solvable puzzle
    g = Generator()
    g.fillGrid()
    g.print_board()
    print()
    g.reduceGrid()
    g.print_board()
    print("Sudoku Grid Ready")

if __name__ == "__main__":
    main()