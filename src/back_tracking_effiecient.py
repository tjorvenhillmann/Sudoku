import copy

class Sudoku:
    def __init__(self) -> None:
        self.solved = []
        self.grid = [
                    [2,0,0,0,0,0,0,0,0],
                    [0,9,8,0,0,6,0,0,0],
                    [0,0,0,9,1,0,4,0,8],
                    [7,0,0,0,0,1,0,9,3],
                    [0,0,0,0,0,0,8,0,0],
                    [0,0,0,8,0,3,0,4,7],
                    [0,0,0,0,6,0,0,0,0],
                    [0,0,2,7,0,0,0,0,0],
                    [0,3,5,0,0,0,2,0,1]
                    ]

    #Check if the slected Number is useable
    def possible(self, row:int, col:int, val:int) -> bool:
        #Check in Row for existance
        for r in range(9):
            if self.grid[r][col] == val:
                return False
        #Check in Column for existance
        for c in range(9):
            if self.grid[row][c] == val:
                return False
        
        #Check in 3x3 Square
        c0 = (col//3)*3
        r0 = (row//3)*3
        for r in range(3):
            for c in range(3):
                if self.grid[r0+r][c0+c] == val:
                    return False
        
        #If Number is not in Row, Column or Square
        return True

    #Iter trough the whole grid
    def solve(self):
        #Search for empty
        for row in range(9):
            for col in range(9):
                #Find empty cell
                if self.grid[row][col] == 0:
                    #try all numbers
                    for number in range (1, 10):
                        if self.possible(row, col, number):
                            self.grid[row][col] = number
                            self.solve()
                            self.grid[row][col] = 0
                    return
        self.solved = copy.deepcopy(self.grid)

def main():
    s = Sudoku()
    s.solve()
    print(s.solved)

if __name__ == '__main__':
    main()