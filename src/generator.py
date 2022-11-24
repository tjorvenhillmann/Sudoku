from random import randint, shuffle
from time import sleep

class GENERARTOR:
    
    def __init__(self):
        #initialise empty 9 by 9 grid
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
        # Number list needed for the shuffel function
        self.numberList = [1,2,3,4,5,6,7,8,9]

    def checkGrid(self):
        # This function checks every cell for a value other than zero
        for row in range(0,9):
            for col in range(0,9):
                if self.grid[row][col] == 0:
                    return False

        # The grid is complete 
        return True

    def solveGrid(self):
        grid = self.grid
        # Find next empty cell to solve
        for i in range(0,81):
            row = i//9 # Needed to get on 9th cell row = 1 and thats the 2nd row of the grid 
            col = i%9  # No integer divison because columns are not affected by line break 
            if grid[row][col] == 0:
                for value in range(1,10):
                    # Check that this number is not alreday used in this row
                    if value not in grid[row]:
                        # Check if this number is not already used in this column
                        if value not in (grid[0][col],grid[1][col],grid[2][col],grid[3][col],grid[4][col],grid[5][col],grid[6][col],grid[7][col],grid[8][col]):
                            # Identify in which of the 9 squares were are working
                            # Empty square is an a 2D-list 
                            square = []
                            # Top squares 3x3
                            if row < 3: 
                                if col < 3:
                                    square = [grid[i][0:3] for i in range(0,3)]
                                elif col < 6:
                                    square = [grid[i][3:6] for i in range(0,3)]
                                else:
                                    square = [grid[i][6:9] for i in range(0,3)]
                            # Middle squares 3x3
                            elif row < 6:  
                                if col < 3:
                                    square = [grid[i][0:3] for i in range(0,3)]
                                elif col < 6:
                                    square = [grid[i][3:6] for i in range(0,3)]
                                else:
                                    square = [grid[i][6:9] for i in range(0,3)]
                            # Bottom squares 3x3
                            else: 
                                if col < 3:
                                    square = [grid[i][0:3] for i in range(0,3)]
                                elif col < 6:
                                    square = [grid[i][3:6] for i in range(0,3)]
                                else:
                                    square = [grid[i][6:9] for i in range(0,3)]
                            
                            # Check that this number is not already be used on this 3x3 square
                            if value not in (square[0], + square[1] + square[2]):
                                grid[row][col] = value
                                if self.checkGrid():
                                    self.counter += 1
                                    break
                                else:
                                    if self.solveGrid():
                                        return True 
                break
        grid[row][col] = 0

    def fillGrid(self):
        # Find next empty cell to solve
        for i in range(0,81):
            row = i//9 # Needed to get on 9th cell row = 1 and thats the 2nd row of the grid 
            col = i%9  # No integer divison because columns are not affected by line break 
            if self.grid[row][col] == 0:
                shuffle(self.numberList)
                for value in self.numberList:
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
                                if self.checkGrid():
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

    def genPuzzle(self):
        # Conatins the mainloop for generating a new sudoku grid
        # This function is the thats later called by the GUI 
        self.fillGrid()
        self.print_board()
        print()
        sleep(1)

        #return self.grid 

def main():
    g = GENERARTOR()
    g.genPuzzle()

if __name__ == "__main__":
    main()