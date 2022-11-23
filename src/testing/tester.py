from back_tracking import solve
from time import time_ns
from boards import boards

def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -  ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


i = 1
for board in boards:
    start = time_ns()
    solved = solve(board)
    end = time_ns()
    print(f'Rätsel {i}: {solved} in {((end-start)/1000000000)} s')
    print_board(board)
    i += 1