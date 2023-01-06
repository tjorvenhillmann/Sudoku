from PyQt5.QtCore import (QCoreApplication, QMetaObject, QTimer, QTime, Qt)
from PyQt5.QtGui import (QCursor, QFont)
from PyQt5.QtWidgets import *
from styles import BorderStyleSheets
from copy import deepcopy
from random import choice
from generator import * 

class SudokuCell(QLabel):
    # Sudoku cell class constructor
    def __init__(self, row , column, userGrid):
        super(QLabel, self).__init__()
        self.row = row 
        self.column = column
        # Reference to the userGrid from parent class Sudoku_UI
        # Used to store single cells that only contain a single number
        self.userGrid = userGrid
        self.numberSet = set()
        self.cellFont = QFont()
        self.cellFont.setPointSize(16)
        self.defaultFont = QFont()
        self.defaultFont.setPointSize(8)
        self.readOnlyFlag = 0
        self.styles = BorderStyleSheets.style
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFrameShape(QFrame.NoFrame)
        self.setWordWrap(True)
        # Get cell border outline style from styles.py file
        self.setStyleSheet(str(self.styles[self.row][self.column]))
        self.setAlignment(Qt.AlignCenter)
        self.setFocusPolicy(Qt.TabFocus | Qt.ClickFocus)
        self.setMinimumSize(50, 50)

    # Hightlight background of selected cell
    def focusInEvent(self, event):
        self.setStyleSheet("background-color: rgb(200, 200, 200);" + str(self.styles[self.row][self.column]))
    
    # Remove highlight from cell when unselected
    def focusOutEvent(self, event):
        self.setStyleSheet(str(self.styles[self.row][self.column]))
   
    # Place number inside Sudoku cell 
    def setCellText(self, number):
        # This function is only called when a single number is entered
        if (number != 0):
            self.setFont(self.cellFont)
            self.setText(str(number))
            self.readOnlyFlag = 1
        else:
            self.setText("")

    # Remove cell text 
    def removeCellText(self):
        self.setFont(self.defaultFont)
        self.setText("")
        self.readOnlyFlag = 0

    # Update the number of current cell
    def setElements(self):
        # Local variable definitions
        numberStr = str()

        # If only a single number for this cell, add it to the userGrid
        if len(self.numberSet) == 1:
            self.setFont(self.cellFont)
            self.userGrid[self.row][self.column] = next(iter(self.numberSet))
            # This line extracts the first argument from the set 
            # Needed to display the text in the cell center
            numberStr = str(next(iter(self.numberSet)))
        else:
            self.setFont(self.defaultFont)
            self.userGrid[self.row][self.column] = 0
            # Loop for wrapping text
            for x, number in enumerate(self.numberSet):
                # After 3 numbesr insert line break 
                # Manual line break is needed because of sizePolicy "expanding"
                if not (x % 3) and x != 0:
                    numberStr += "\n"
                numberStr += (str(number) + " ")

        # Display text in cell
        self.setText(numberStr)	

    # Add element to set 
    def addAndRemoveElement(self, elem = 0):
        if elem in self.numberSet:
            self.numberSet.remove(elem)
        else:
            self.numberSet.add(elem)
        self.setElements()

    # Keyboard input
    def keyPressEvent(self, event):
        if (event.key() >= Qt.Key_1 and event.key() <= Qt.Key_9):
            # Check if the cell is not a clue 
            if not self.readOnlyFlag:
                self.addAndRemoveElement(event.key() - Qt.Key_0)


class Sudoku_UI():
    # Gui class constructor
    def __init__(self):
        # Create MainWindow 
        self.MainWindow = QMainWindow()
        # Create empty list for both game and solved boards 
        # -> needed so that the reference always stays the same 
        self.gameGrid = list()
        self.solvedGrid = list()
        # Empty list for storing all Sudoku_Cell instances
        self.cells = [[0]*9 for x in range(9)]
        # List of empty cells for faster hint function 
        # Random selection is way faster when only used on empty cells 
        self.emptyCells = list()
        # Create runtime element 
        self.runtime = QTime()
        # Start time is zero
        self.runtime.setHMS(0,0,0)
        # Create object of generator class
        self.g = Generator()
        
    def setupMainWindow(self):
        self.MainWindow.setWindowModality(Qt.NonModal)
        #self.MainWindow.resize(1024, 768)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainWindow.sizePolicy().hasHeightForWidth())
        self.MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setKerning(True)
        self.MainWindow.setFont(font)
        self.MainWindow.setCursor(QCursor(Qt.ArrowCursor))
        self.MainWindow.setMouseTracking(False)
        self.MainWindow.setWindowOpacity(1.000000000000000)
        self.MainWindow.setAutoFillBackground(False)
        self.MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(self.MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

    def setupWindows(self):
        self.horizontalLayout_14 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.Windows = QStackedWidget(self.centralwidget)
        self.Windows.setObjectName(u"Windows")
        self.Windows.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.Windows.setFrameShape(QFrame.NoFrame)
        self.Windows.setLineWidth(1)
        
        self.setupMenuPage() 
        self.setupGamePage()

        self.MainWindow.setCentralWidget(self.centralwidget)

    def setupMenuPage(self):
        self.Main = QWidget()
        self.Main.setObjectName(u"Main")
        self.Main.setAutoFillBackground(False)
        self.Main.setStyleSheet(u"color: 0 0 0")
        self.verticalLayout_3 = QVBoxLayout(self.Main)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.HeaderPage1 = QLabel(self.Main)
        self.HeaderPage1.setObjectName(u"HeaderPage1")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.HeaderPage1.sizePolicy().hasHeightForWidth())
        self.HeaderPage1.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(32)
        font1.setBold(False)
        font1.setWeight(50)
        self.HeaderPage1.setFont(font1)
        self.HeaderPage1.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.HeaderPage1)

        self.verticalSpacer_2 = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(50, 0, -1, -1)
        self.LabelScoreBoard = QLabel(self.Main)
        self.LabelScoreBoard.setObjectName(u"LabelScoreBoard")
        sizePolicy1.setHeightForWidth(self.LabelScoreBoard.sizePolicy().hasHeightForWidth())
        self.LabelScoreBoard.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setPointSize(14)
        font2.setBold(True)
        font2.setItalic(False)
        font2.setUnderline(False)
        font2.setWeight(75)
        font2.setKerning(True)
        self.LabelScoreBoard.setFont(font2)
        self.LabelScoreBoard.setIndent(0)

        self.horizontalLayout_5.addWidget(self.LabelScoreBoard)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalLayout_2.setContentsMargins(50, -1, 50, -1)
        self.listView = QListView(self.Main)
        self.listView.setObjectName(u"listView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy2)
        self.listView.setStyleSheet(u"")
        self.listView.setFrameShape(QFrame.Box)
        self.listView.setFrameShadow(QFrame.Plain)
        self.listView.setLineWidth(1)
        self.listView.setMidLineWidth(1)
        self.listView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.listView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)

        self.horizontalLayout_2.addWidget(self.listView)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 25, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(50, -1, -1, -1)
        self.LabelNewGame = QLabel(self.Main)
        self.LabelNewGame.setObjectName(u"LabelNewGame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.LabelNewGame.sizePolicy().hasHeightForWidth())
        self.LabelNewGame.setSizePolicy(sizePolicy3)
        font3 = QFont()
        font3.setPointSize(14)
        font3.setBold(True)
        font3.setWeight(75)
        font3.setKerning(True)
        self.LabelNewGame.setFont(font3)
        self.LabelNewGame.setMargin(0)
        self.LabelNewGame.setIndent(0)

        self.horizontalLayout_4.addWidget(self.LabelNewGame)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(50, 0, 50, 25)
        self.Easy = QPushButton(self.Main)
        self.Easy.setObjectName(u"Easy")
        sizePolicy3.setHeightForWidth(self.Easy.sizePolicy().hasHeightForWidth())
        self.Easy.setSizePolicy(sizePolicy3)
        font4 = QFont()
        font4.setPointSize(11)
        self.Easy.setFont(font4)

        self.horizontalLayout.addWidget(self.Easy)

        self.Medium = QPushButton(self.Main)
        self.Medium.setObjectName(u"Medium")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.Medium.sizePolicy().hasHeightForWidth())
        self.Medium.setSizePolicy(sizePolicy4)
        self.Medium.setFont(font4)

        self.horizontalLayout.addWidget(self.Medium)

        self.Hard = QPushButton(self.Main)
        self.Hard.setObjectName(u"Hard")
        sizePolicy4.setHeightForWidth(self.Hard.sizePolicy().hasHeightForWidth())
        self.Hard.setSizePolicy(sizePolicy4)
        self.Hard.setFont(font4)

        self.horizontalLayout.addWidget(self.Hard)

        self.Insane = QPushButton(self.Main)
        self.Insane.setObjectName(u"Insane")
        sizePolicy4.setHeightForWidth(self.Insane.sizePolicy().hasHeightForWidth())
        self.Insane.setSizePolicy(sizePolicy4)
        self.Insane.setFont(font4)

        self.horizontalLayout.addWidget(self.Insane)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalSpacer_3 = QSpacerItem(20, 25, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.Windows.addWidget(self.Main)

    def setupGamePage(self):
        self.Game = QWidget()
        self.Game.setObjectName(u"Game")
        self.Game.setStyleSheet(u"")
        self.horizontalLayout_15 = QHBoxLayout(self.Game)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.ContainerLayout = QHBoxLayout()
        self.ContainerLayout.setObjectName(u"ContainerLayout")
        self.ContainerLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.ContainerLayout.setContentsMargins(0, -1, 0, -1)

        self.BoardLayout = QGridLayout()
        self.BoardLayout.setSpacing(0)
        self.BoardLayout.setObjectName(u"BoardLayout")

        # Pre place the layout for all the sudoku cells 
        self.ContainerLayout.addLayout(self.BoardLayout)

        self.ButtonLayout = QVBoxLayout()
        self.ButtonLayout.setSpacing(25)
        self.ButtonLayout.setObjectName(u"ButtonLayout")
        self.ButtonLayout.setContentsMargins(-1, 10, -1, 10)
        self.TimeViewer = QTimeEdit(self.Game)
        self.TimeViewer.setObjectName(u"Timer")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.TimeViewer.sizePolicy().hasHeightForWidth())
        self.TimeViewer.setSizePolicy(sizePolicy5)
        font5 = QFont()
        font5.setPointSize(18)
        font5.setBold(True)
        font5.setWeight(75)
        self.TimeViewer.setFont(font5)
        self.TimeViewer.setFrame(True)
        self.TimeViewer.setAlignment(Qt.AlignCenter)
        self.TimeViewer.setReadOnly(True)
        self.TimeViewer.setFocusPolicy(Qt.NoFocus)
        self.TimeViewer.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.ButtonLayout.addWidget(self.TimeViewer)

        # Sets an interrupt every second to update the timer
        self.Timer = QTimer(self.Game) 

        self.Hint = QPushButton(self.Game)
        self.Hint.setObjectName(u"Hint")
        sizePolicy5.setHeightForWidth(self.Hint.sizePolicy().hasHeightForWidth())
        self.Hint.setSizePolicy(sizePolicy5)
        font6 = QFont()
        font6.setPointSize(11)
        self.Hint.setFont(font6)


        self.ButtonLayout.addWidget(self.Hint)

        self.AutoSolve = QPushButton(self.Game)
        self.AutoSolve.setObjectName(u"AutoSolve")
        sizePolicy5.setHeightForWidth(self.AutoSolve.sizePolicy().hasHeightForWidth())
        self.AutoSolve.setSizePolicy(sizePolicy5)
        self.AutoSolve.setFont(font6)


        self.ButtonLayout.addWidget(self.AutoSolve)

        self.Clear = QPushButton(self.Game)
        self.Clear.setObjectName(u"Clear")
        sizePolicy5.setHeightForWidth(self.Clear.sizePolicy().hasHeightForWidth())
        self.Clear.setSizePolicy(sizePolicy5)
        self.Clear.setFont(font6)


        self.ButtonLayout.addWidget(self.Clear)

        self.Check = QPushButton(self.Game)
        self.Check.setObjectName(u"Check")
        sizePolicy5.setHeightForWidth(self.Check.sizePolicy().hasHeightForWidth())
        self.Check.setSizePolicy(sizePolicy5)
        self.Check.setFont(font6)


        self.ButtonLayout.addWidget(self.Check)

        self.Quit = QPushButton(self.Game)
        self.Quit.setObjectName(u"Back")
        sizePolicy5.setHeightForWidth(self.Quit.sizePolicy().hasHeightForWidth())
        self.Quit.setSizePolicy(sizePolicy5)
        self.Quit.setFont(font6)


        self.ButtonLayout.addWidget(self.Quit)


        self.ContainerLayout.addLayout(self.ButtonLayout)

        self.horizontalLayout_15.addLayout(self.ContainerLayout)

        self.Windows.addWidget(self.Game)

        self.horizontalLayout_14.addWidget(self.Windows)

    def retranslateUi(self):
        self.MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sudoku", None))
        self.HeaderPage1.setText(QCoreApplication.translate("MainWindow", u"SUDOKU", None))
        self.LabelScoreBoard.setText(QCoreApplication.translate("MainWindow", u"ScoreBoard:", None))
        self.LabelNewGame.setText(QCoreApplication.translate("MainWindow", u"New Game:", None))
        self.Easy.setText(QCoreApplication.translate("MainWindow", u"\nEasy\n", None))
        self.Medium.setText(QCoreApplication.translate("MainWindow", u"\nMedium\n", None))
        self.Hard.setText(QCoreApplication.translate("MainWindow", u"\nHard\n", None))
        self.Insane.setText(QCoreApplication.translate("MainWindow", u"\nInsane\n", None))
        self.TimeViewer.setDisplayFormat(QCoreApplication.translate("MainWindow", u"HH:mm:ss", None))
        self.AutoSolve.setText(QCoreApplication.translate("MainWindow", u"Auto-Solve", None))
        self.Hint.setText(QCoreApplication.translate("MainWindow", u"Hint", None))
        self.Clear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.Check.setText(QCoreApplication.translate("MainWindow", u"Check", None))
        self.Quit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
      
    def createBoard(self):
        for r in range(9):
            for c in range(9):
                # Create new cell
                newCell = SudokuCell(r, c, self.userGrid)
                # Add the new Cell to the Sudoku-Grid/Board layout
                self.BoardLayout.addWidget(newCell, r, c, 1, 1)
                # Store instance into 2D list for later acces
                self.cells[r][c] = newCell

    def generateBoards(self, clues):
        # In this function the three neeeded boards will be created 
        # Under the use of the included generator class
        self.solvedGrid, self.gameGrid = self.g.sudoku(clues) 
        self.userGrid = deepcopy(self.gameGrid)
        self.createBoard()

    def fillBoard(self):
        for r in range(9):
            for c in range(9):
                # Set text for new cell
                self.cells[r][c].setCellText(self.gameGrid[r][c])
                # Add position of empty cells to a list for the hint function
                if self.gameGrid[r][c] == 0:
                    self.emptyCells.append((r,c))
        
        # Atfer board is filled -> starting the timer
        self.Timer.start(1000)  

    def resetBoard(self):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].removeCellText()

    def removeOldBoardData(self):
        # Remove old data for avoiding double references 
        self.gameGrid.clear()
        self.solvedGrid.clear()

    def solveBoard(self):
        if len(self.emptyCells) > 0:
            for r in range(9):
                for c in range(9):
                    # Display numbers inside the grid 
                    self.cells[r][c].setCellText(self.solvedGrid[r][c])
                    # Empty cells have to be set to zero remaining empty cells 
                    self.emptyCells.clear()
                    # Disable the check button and put the background color to green
                    self.Check.setEnabled(False)
                    self.Check.setStyleSheet(u"background-color: rgba(0, 200, 0, 0.4)")

    def setHint(self):
        # Check if there are empty cells left in the board
        if len(self.emptyCells) > 0:
            # Choice lets us randomly choose an element from sequence
            r, c = choice(self.emptyCells)
            self.emptyCells.remove((r,c))
            
            # Take element from solved grid and set it inside the cell
            self.cells[r][c].setCellText(self.solvedGrid[r][c])
            #self.cells[r][c].focusInEvent(event = 1)
            # Store the number inside the userGrid as solved number
            self.userGrid[r][c] = self.solvedGrid[r][c]
        else:
            # Board is fully filled and check button can be set to green and disabled
            self.Check.setStyleSheet(u"background-color: rgba(0, 200, 0, 0.4)")
            self.Check.setEnabled(False)

    def checkBoard(self):
        # Compare user and check grid 
        if self.userGrid == self.solvedGrid:
            self.Check.setStyleSheet(u"background-color: rgba(0, 200, 0, 0.4)")
            # When board is correctly solved Timer can be stopped 
            self.Timer.stop()
            return True
        else:
            self.Check.setStyleSheet(u"background-color: rgba(200, 0, 0, 0.4)")
            return False

    def updateTime(self):
        # Adding a second to the runtime
        self.runtime = self.runtime.addSecs(1) # addSecs retruns a new runtime object 
        
        # Print for debugging purposes
        #print("Runtime: ", self.runtime.toString("hh:mm:ss"))
        
        # Update the timer inside the game window
        self.TimeViewer.setTime(self.runtime) 

    def resetTime(self):
        # Reset time on quit or clear button clicked events -> done through the eventHandler()
        self.Timer.stop()
        self.runtime.setHMS(0,0,0)
        self.TimeViewer.setTime(self.runtime)

    def eventHandler(self, event):
        # This function represents the event handeling functionality
        # Each UI element(e.g buttons) have diffrent evenst thats beeing handled here  
        # With newly introduced match -> case statement from Python 3.10
        # So Python 3.10 is needed atm --> may be later changed to if -> elif statements 
        match event:
            case "Easy":
                # Generate boards with 50 remaining numbers
                self.generateBoards(50)
                self.fillBoard()
                return self.Windows.setCurrentIndex(1)
            case "Medium":
                self.generateBoards(40)
                self.fillBoard()
                return self.Windows.setCurrentIndex(1)
            case "Hard":
                self.generateBoards(30)
                self.fillBoard()
                return self.Windows.setCurrentIndex(1)
            case "Insane":
                pass
            case "Hint":
                self.setHint()
            case "Solve":
                # Stop timer because board is solved
                self.Timer.stop()
                self.solveBoard()
            case "Clear":
                self.resetTime()
                self.resetBoard()
                self.fillBoard()
                self.Check.setStyleSheet("")
                self.Check.setEnabled(True)
            case "Check":
                self.checkBoard()
            case "Quit":
                self.resetTime()
                self.resetBoard()
                self.removeOldBoardData()
                # Set background color to default
                self.Check.setStyleSheet("")
                self.Check.setEnabled(True)
                # Go back to menu page
                return self.Windows.setCurrentIndex(0)

    def setupUi(self):

        self.setupMainWindow()
        self.setupWindows()
        self.retranslateUi()

        # Events from main page 
        self.Easy.clicked.connect(lambda: self.eventHandler("Easy"))
        self.Medium.clicked.connect(lambda: self.eventHandler("Medium"))
        self.Hard.clicked.connect(lambda: self.eventHandler("Hard"))
        self.Insane.clicked.connect(lambda: self.eventHandler("Insane"))
        
        # Events from game page
        self.Timer.timeout.connect(self.updateTime) 
        self.Hint.clicked.connect(lambda: self.eventHandler("Hint"))
        self.AutoSolve.clicked.connect(lambda: self.eventHandler("Solve"))
        self.Clear.clicked.connect(lambda: self.eventHandler("Clear"))
        self.Check.clicked.connect(lambda: self.eventHandler("Check"))
        self.Quit.clicked.connect(lambda: self.eventHandler("Quit"))

        # Set main page as default window
        self.Windows.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(self.MainWindow)

    def loadUi(self):
        self.MainWindow.show()


def main():

    app = QApplication([])
    ui = Sudoku_UI()
    ui.setupUi()
    ui.loadUi()
    app.exec()

if __name__ == "__main__":
    main()