from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
import sys
import knuth
import csv
import copy

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        self.resize(300, 300)
        self.setWindowTitle('Sudoku Game Solver')

        frame = QtWidgets.QFrame()
        self.setCentralWidget(frame)

        layout = QtWidgets.QHBoxLayout()
        frame.setLayout(layout)

        self.file_button = QtWidgets.QPushButton('Click to upload your sudoku board')
        layout.addWidget(self.file_button)

        self.file_button.clicked.connect(self.handle_button_click)
    
    def handle_button_click(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'OpenFile', "", "Excel (*.csv)")

        if file_name[0]:
            sudoku_board = self.parse_file(file_name[0])
            original_board = copy.deepcopy(sudoku_board)
            solver = knuth.AlgorithmX()
            solver.solveSudoku(sudoku_board)
            self.open_dialog(original_board, sudoku_board)
        else:
            print('Can not open the file, the file should be CSV only')

    
    def parse_file(self, file_name):
        board = []
        with open(file_name, mode='r') as file:
            out = csv.reader(file)
            for lines in out:
                board.append(lines)
        if len(board) != 9 or len(board[0]) != 9:
            raise 'Invalid input, expect a 9 x 9 sudoku board'
        return board     

    def open_dialog(self, original_board, solved_board):
        dialog = MyDialog()
        dialog.set_boards(original_board, solved_board)
        dialog.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        dialog.exec_()

class MyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(300, 300, 315, 315)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_board(qp)
        self.fill_board(qp)
        qp.end()
    
    def set_boards(self, original_board, solved_board):
        self.original_board = original_board
        self.solved_board = solved_board

    def fill_board(self, qp):
        x = 0
        y = 0

        for i in range(9):
            y = 18 * (2 * i + 1)
            for j in range(9):
                x = 17 * (2 * j + 1)
                if self.original_board[i][j] != self.solved_board[i][j]:
                    qp.setPen(QPen(Qt.red))
                    qp.drawText(x, y, self.solved_board[i][j])
                else:
                    qp.setPen(QPen(Qt.black))
                    qp.drawText(x, y, self.original_board[i][j])
                 
    def draw_board(self, qp):
        qp.setPen(QPen(Qt.black, 2, Qt.PenStyle.SolidLine))

        for i in range(10):
            qp.drawLine(0, i * 35, 315, i * 35)

        for i in range(10):
            qp.drawLine(i * 35, 0, i * 35, 315)

        qp.setPen(QPen(Qt.black, 5, Qt.PenStyle.SolidLine))

        for i in range(3):
            qp.drawLine(0, i * 105, 315, i * 105)

        for i in range(3):
            qp.drawLine(i * 105, 0, i * 105, 315)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()