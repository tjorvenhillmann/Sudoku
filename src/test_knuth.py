import unittest
import knuth

class TestHyperSudoku(unittest.TestCase):

    def setUp(self):
        self.solver = knuth.AlgorithmX()

    def test_Unsolvable_One(self):
        board = [
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
        for i in range(9):
            for j in range(9):
                board[i][j] = str(board[i][j])

        self.solver.solveSudoku(board)
        print(board)


if __name__ == "__main__":
    unittest.main()