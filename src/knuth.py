from collections import defaultdict;

class AlgorithmX:

    def __init__(self):
        # constrains of hyper sudoku
        self.constrains_upper_left = set()
        self.constrains_upper_right = set()
        self.constrains_botton_left = set()
        self.constrains_botton_right = set()

    def solveSudoku(self, board):
        # mark as (0, row, value) to record values in row
        rows = set() 
        # (1, col, value) to record values in column
        cols = set() 
        # (2, cell, value) to record values in each 3x3 spot
        cells = set() 
        # (3, row, col) to record cell index
        spots = set()
        # count how many spots to be filled
        count_spots = 0

        for row_index in range(9):
            row = board[row_index]
            for col_index in range(9):
                # find the spot that needs to be filled
                if row[col_index] == "0":
                    count_spots += 1
                    continue

                val = int(row[col_index])
                rows.add((0, row_index, val))
                cols.add((1, col_index, val))

                cell_spot = self.get_cell_spot(row_index, col_index)
                cells.add((2, cell_spot, val))

                spots.add((3, row_index, col_index))

                self.set_constrains(row_index, col_index, val)
        
        # build index mapping
        resource_to_values_mapping = defaultdict(set)
        values_to_resource_mapping = defaultdict(set)

        for row in range(9):
            for col in range(9):
                for val in range(1, 10):
                    row_res = (0, row, val)
                    col_res = (1, col, val)
                    cell_res = (2, self.get_cell_spot(row, col), val)
                    small_cell_res = (3, row, col)

                    if (row_res not in rows) and (col_res not in cols) and (cell_res not in cells) and (small_cell_res not in spots) and self.check_constrains(row, col, val):
                        curr_val = (row, col, val)
                        resource_to_values_mapping[row_res].add(curr_val)
                        resource_to_values_mapping[col_res].add(curr_val)
                        resource_to_values_mapping[cell_res].add(curr_val)
                        resource_to_values_mapping[small_cell_res].add(curr_val)
                        values_to_resource_mapping[curr_val].add(row_res)
                        values_to_resource_mapping[curr_val].add(col_res)
                        values_to_resource_mapping[curr_val].add(cell_res)
                        values_to_resource_mapping[curr_val].add(small_cell_res)

        solution = []
        self.solve(resource_to_values_mapping, values_to_resource_mapping, solution, count_spots)

        for r, c, val in solution:
            board[r][c] = str(val)

    # backtrack solving 
    def solve(self, resource_to_values_mapping, values_to_resource_mapping, solution, count_spots):
        if len(solution) == count_spots:
            return True

        if len(resource_to_values_mapping) == 0:
            return False
        
        min_res, values = min(resource_to_values_mapping.items(), key=lambda rv: len(rv[1]))

        for val in list(values):

            if not self.check_constrains(val[0], val[1], val[2]):
                continue

            rv_pairs_to_remove = set()

            for vr in values_to_resource_mapping[val]:
                for rv in resource_to_values_mapping[vr]:
                    for vtr in values_to_resource_mapping[rv]:
                        rv_pairs_to_remove.add((vtr, rv))

            for r, v in rv_pairs_to_remove:
                resource_to_values_mapping[r].remove(v)
                values_to_resource_mapping[v].remove(r)

                if len(resource_to_values_mapping[r]) == 0:
                    del resource_to_values_mapping[r]

            solution.append(val)
            self.set_constrains(val[0], val[1], val[2])

            if self.solve(resource_to_values_mapping, values_to_resource_mapping, solution, count_spots):
                return True

            solution.pop()
            self.reset_constrains(val[0], val[1], val[2])

            for r, v in rv_pairs_to_remove:
                resource_to_values_mapping[r].add(v)
                values_to_resource_mapping[v].add(r)

        return False

    def reset_constrains(self, row, col, val):
        hyper_spot = self.get_cell_hyper_spot(row, col)

        if hyper_spot == -1:
            return
        
        if (hyper_spot == 0) and (val in self.constrains_upper_left):
            self.constrains_upper_left.remove(val)
        elif (hyper_spot == 1) and (val in self.constrains_upper_right):
            self.constrains_upper_right.remove(val)
        elif (hyper_spot == 2) and (val in self.constrains_botton_left):
            self.constrains_botton_left.remove(val)
        elif (hyper_spot == 3) and (val in self.constrains_botton_right):
            self.constrains_botton_right.remove(val)


    # return true if the value is not in constrain sets, otherwise not
    def check_constrains(self, row, col, val):
        hyper_spot = self.get_cell_hyper_spot(row, col)

        if (hyper_spot == 0) and (val in self.constrains_upper_left):
            return False
        if (hyper_spot == 1) and (val in self.constrains_upper_right):
            return False
        if (hyper_spot == 2) and (val in self.constrains_botton_left):
            return False
        if (hyper_spot == 3) and (val in self.constrains_botton_right):
            return False
        return True

    # add hyper sudoku constrains
    def set_constrains(self, row, col, val):
        hyper_spot = self.get_cell_hyper_spot(row, col)

        if hyper_spot == -1:
            return
        
        if (hyper_spot == 0) and (val not in self.constrains_upper_left):
            self.constrains_upper_left.add(val)
        elif (hyper_spot == 1) and (val not in self.constrains_upper_right):
            self.constrains_upper_right.add(val)
        elif (hyper_spot == 2) and (val not in self.constrains_botton_left):
            self.constrains_botton_left.add(val)
        elif (hyper_spot == 3) and (val not in self.constrains_botton_right):
            self.constrains_botton_right.add(val)
        

    def get_cell_hyper_spot(self, row, col):
        # upper left
        if (1 <= row <= 3) and (1 <= col <= 3):
            return 0
        # upper right
        if (1 <= row <= 3) and (5 <= col <= 7):
            return 1
        # botton left
        if (5 <= row <= 7) and (1 <= col <= 3):
            return 2
        # botton right
        if (5 <= row <= 7) and (5 <= col <=7):
            return 3
        return -1

    # divide the 9x9 board to 9 3x3 spots, get the cell belongs to which spot
    def get_cell_spot(self, row, col):
        return row // 3 + (col // 3) * 3