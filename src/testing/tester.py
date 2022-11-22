from back_tracking import solve
from time import time_ns
from boards import boards

i = 1
for board in boards:
    start = time_ns()
    solved = solve(board)
    end = time_ns()
    print(f'Rätsel {i}: {solved} in {((end-start)/1000000000)} s')
    i += 1