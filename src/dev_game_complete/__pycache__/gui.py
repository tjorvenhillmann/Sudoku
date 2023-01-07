from PyQt5.QtCore import (QCoreApplication, QMetaObject, QTimer, QTime, Qt)
from PyQt5.QtGui import (QCursor, QFont, QColor)
from PyQt5.QtWidgets import *
from styles import BorderStyleSheets
from copy import deepcopy
from random import choice
from generator import * 

class SudokuCell(QLabel):
    '''
    This class contains all settings and interactive function for 
    a SudokuCell. Labels are used as widget for each cell. 
    We set/remove the text and change background colors if the cell 
    is selected or not. We can also set multiple elements if the user 
    requests that.
    Input of numbers is done by pressing the number on the keyboard once 
    to place the number and again to remove it. 
    '''

    def __init__(self, row , column, userGrid):
        # Call the constructor of the superclass
        super(QLabel, self).__init__()
        # Store position inside the grid
        self.row = row 
        self.column = column
        # Reference to the userGrid from parent class Sudoku_UI
        # Used to store single cells that only contain a single number
        self.userGrid = userGrid
        self.numberSet = set()
        # Set the needed font sizes 
        self.cellFont = QFont()
        self.cellFont.setPointSize(16)
        self.defaultFont = QFont()
        self.defaultFont.setPointSize(8)
        # ReadOnlyFlag indicates that the cell is a solved cell
        self.readOnlyFlag = 0
        # Styles for the border thickness and color
        self.styles = BorderStyleSheets.style
        # SizePolicy set the behaviour of the label in the window
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

    def focusInEvent(self, event):
        '''
        This function changes the background-color when the cell is selected by tab or mouse
        '''

        self.setStyleSheet("background-color: rgb(200, 200, 200);" + str(self.styles[self.row][self.column]))
    
    def focusOutEvent(self, event):
        '''
        This funcion sets background-color back to default when cell is no selected anymore
        '''

        self.setStyleSheet(str(self.styles[self.row][self.column]))
    
    def setCellText(self, number):
        '''
        This function places the text for the solved cells and marks them with the readOnlyFlag 
        '''

        # This function is only called when a single number is entered
        if (number != 0):
            self.setFont(self.cellFont)
            self.setText(str(number))
            self.readOnlyFlag = 1
        else:
            self.setText("")

    def removeCellText(self):
        '''
        This function clears the text and removes the readOnlyFlag.
        Makes it accessible for a new game.
        '''

        self.setFont(self.defaultFont)
        self.setText("")
        self.readOnlyFlag = 0

    def setElements(self):
        '''
        This function uses the number set to update multiple elements in sorted order 
        in the cell.
        With this function it's possible to display more then one number for easier play. 
        When the set only contains one number it is stored in the userGrid. 
        '''

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

    def addAndRemoveElement(self, elem = 0):
        '''
        This function adds the number or removes it whens already inside the set.
        This function is the 'CallBack' for the keyboard inputs. 
        '''

        if elem in self.numberSet:
            self.numberSet.remove(elem)
        else:
            self.numberSet.add(elem)
        self.setElements()

    def keyPressEvent(self, event):
        '''
        This functions handles the keyboard inputs and only allows the key 1-9.
        Every other is beeing ignored. When the cells is solved we ignore the input. 
        '''

        if (event.key() >= Qt.Key_1 and event.key() <= Qt.Key_9):
            # Check if the cell is not a clue 
            if not self.readOnlyFlag:
                self.addAndRemoveElement(event.key() - Qt.Key_0)


class Sudoku_UI():
    '''
    This class is the main GUI class. It contains all widgets and elements 
    with the element settings and properties. 
    The following fucntions control the functionality depend on the users actions,
    mainly through the eventHandler function.
    '''
    
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
        # Solving flag to avoid storing the score if game was quitted before solving
        self.solvedFlag = 0
        # Solving method flag -> when 1 auto-solved
        self.solvingMethodFlag = 0
        # Create hint counter
        self.hintCounter = 0
        # Diffulty string
        self.diffStr = str()
        # Create runtime element 
        self.runtime = QTime()
        # Start time is zero
        self.runtime.setHMS(0,0,0,0)
        # Create object of generator class
        self.g = Generator()
        # Variable fo time needed by the solver (ms)
        self.solverTime = 0
        # In this object the solver time is stored for displaying in the game
        self.displaySolverTime = QTime()

    def setupMainWindow(self):
        '''
        This function sets the parameters for the MainWindow as well
        as create the centralWidget in which everything else is placed.
        '''

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
        '''
        The Gui is build with two windows/pages inside a stackedWidget.
        This function creates these Windows and sets all other elements
        and widget through:
        - setupMenuPage
        - setupGamePage
        At the end the centralWidget is placed inside the MainWindow
        '''

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
        '''
        This function create the layout, widget, elements and their 
        properties for the first default menu page.
        At the end the known game results are loaded as well in here.
        '''

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
        self.ScoreTable = QTableWidget(self.Main)
        self.ScoreTable.setObjectName(u"ScoreTable")
        self.ScoreTable.setColumnCount(4)
        headerFont = QFont()
        headerFont.setPointSize(9)
        headerFont.setBold(True)
        headerFont.setWeight(75)
        diffcultyHeader = QTableWidgetItem()
        diffcultyHeader.setFont(headerFont)
        timeHeader = QTableWidgetItem()
        timeHeader.setFont(headerFont)
        hintHeader = QTableWidgetItem()
        hintHeader.setFont(headerFont)
        solverHeader = QTableWidgetItem()
        solverHeader.setFont(headerFont)
        self.ScoreTable.setHorizontalHeaderItem(0, diffcultyHeader)
        self.ScoreTable.setHorizontalHeaderItem(1, timeHeader)
        self.ScoreTable.setHorizontalHeaderItem(2, hintHeader)
        self.ScoreTable.setHorizontalHeaderItem(3, solverHeader)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.ScoreTable.sizePolicy().hasHeightForWidth())
        self.ScoreTable.setSizePolicy(sizePolicy2)
        self.ScoreTable.setFrameShape(QFrame.Box)
        self.ScoreTable.setFrameShadow(QFrame.Plain)
        self.ScoreTable.setLineWidth(2)
        self.ScoreTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ScoreTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ScoreTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.ScoreTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.horizontalLayout_2.addWidget(self.ScoreTable)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 25, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
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
        self.horizontalLayout.setContentsMargins(0, 0, 0, 25)
        self.Easy = QPushButton(self.Main)
        self.Easy.setObjectName(u"Easy")        
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.Easy.sizePolicy().hasHeightForWidth())
        self.Easy.setSizePolicy(sizePolicy4)
        font4 = QFont()
        font4.setPointSize(11)
        self.Easy.setFont(font4)

        self.horizontalLayout.addWidget(self.Easy)

        self.Medium = QPushButton(self.Main)
        self.Medium.setObjectName(u"Medium")
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

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalSpacer_3 = QSpacerItem(20, 25, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.Windows.addWidget(self.Main)

        self.addScoresToBoard()

    def setupGamePage(self):
        '''
        This function create the layout, widget, elements and their 
        properties for the second, the game page.
        '''

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
        '''
        This funtion sets the default displayed texts/names of all the elements and their formats.
        '''

        self.MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sudoku", None))
        self.HeaderPage1.setText(QCoreApplication.translate("MainWindow", u"SUDOKU", None))
        self.LabelScoreBoard.setText(QCoreApplication.translate("MainWindow", u"GameBoard:", None))
        self.ScoreTable.horizontalHeaderItem(0).setText(QCoreApplication.translate("MainWindow", u"Difficulty", None))
        self.ScoreTable.horizontalHeaderItem(1).setText(QCoreApplication.translate("MainWindow", u"Time", None))
        self.ScoreTable.horizontalHeaderItem(2).setText(QCoreApplication.translate("MainWindow", u"Hints", None))
        self.ScoreTable.horizontalHeaderItem(3).setText(QCoreApplication.translate("MainWindow", u"Solver", None))
        self.LabelNewGame.setText(QCoreApplication.translate("MainWindow", u"New Game:", None))
        self.Easy.setText(QCoreApplication.translate("MainWindow", u"\nEasy\n", None))
        self.Medium.setText(QCoreApplication.translate("MainWindow", u"\nMedium\n", None))
        self.Hard.setText(QCoreApplication.translate("MainWindow", u"\nHard\n", None))
        self.TimeViewer.setDisplayFormat(QCoreApplication.translate("MainWindow", u"HH:mm:ss", None))
        self.AutoSolve.setText(QCoreApplication.translate("MainWindow", u"Auto-Solve", None))
        self.Hint.setText(QCoreApplication.translate("MainWindow", u"Hint", None))
        self.Clear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.Check.setText(QCoreApplication.translate("MainWindow", u"Check", None))
        self.Quit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))

    def generateBoards(self, clues:int):
        '''
        This function calls the sudoku(clues) function and gets the boards 
        for the current game as well the time the solver needed for solving.
        The userGrid is also created in here, it is needed for not changing 
        the gameGrid, if the user wants to start over.
        The userGrid is also used to check if the board is solved correctly.
        '''

        # In this function the three neeeded boards will be created 
        # Under the use of the included generator class
        self.solvedGrid, self.gameGrid, self.solverTime = self.g.sudoku(clues)
        self.userGrid = deepcopy(self.gameGrid)
        self.createBoard()

    def createBoard(self):
        '''
        This function creates the instance for each SudokuCell.
        '''

        for r in range(9):
            for c in range(9):
                # Create new cell
                newCell = SudokuCell(r, c, self.userGrid)
                # Add the new Cell to the Sudoku-Grid/Board layout
                self.BoardLayout.addWidget(newCell, r, c, 1, 1)
                # Store instance into 2D list for later acces
                self.cells[r][c] = newCell

    def fillBoard(self):
        '''
        This function loads the gameGrid into the board by setting the 
        solved numbers. The empty cells where stored in a list for the 
        hint function.
        When the board is filled the game timer is started.
        '''

        # Reset counters and flags from previous run if multiple games where played 
        self.solvingFlag = 0  
        self.hintCounter = 0
        
        # Main loop for setting sudoku cell text to generated numbers
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
        '''
        This functions clears the cells when the user wanst to restart the game
        or the game is finished and the user quits. This leaves an empyt board for a new game.
        '''

        for r in range(9):
            for c in range(9):
                self.cells[r][c].removeCellText()
        
        # Clear the list of empty cells and renew the userGrid
        self.emptyCells.clear()

    def removeOldBoardData(self):
        '''
        This function clears the data from the last game so the new 
        board data is not mixed with the old.
        '''
 
        self.gameGrid.clear()
        self.solvedGrid.clear()

    def solveBoard(self):
        '''
        This function solves the board by loading the solved board.
        As well as set the solver time and the flags for storing.
        '''
        
        # Stop timer because board is solved
        self.Timer.stop()
        
        if len(self.emptyCells) > 0:
            for r in range(9):
                for c in range(9):
                    # Display numbers inside the grid 
                    self.cells[r][c].setCellText(self.solvedGrid[r][c])
                    # Empty cells have to be set to zero remaining empty cells 
                    self.emptyCells.clear()
                    # Change check button 
                    self.updateButtons("disable")

        # Set the solverTime
        self.setSolverTime()

        self.solvedFlag = 1
        self.solvingMethodFlag = 1

    def setHint(self):
        '''
        This function set a hint. Therefore it randomly picks an empty cell
        from the list and places it into the board. The empyt cell was saved 
        as tuple with its coordinates inside the board, so these coordinates 
        match with the position in the instance-list containing the cell refs.
        '''

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

            # Add 1 to hint counter 
            self.hintCounter += 1

        if len(self.emptyCells) == 0:
            self.Timer.stop()
            # Board is fully filled and check button can be set to green and disabled
            self.updateButtons("disable")
            # Board is solved when last hint was placed 
            self.solvedFlag = 1

    def checkBoard(self):
        '''
        This function compares the userGrid with the solvedGrid and
        sets the check button color as well as the solvedFlag
        '''

        # Compare user and check grid 
        if self.userGrid == self.solvedGrid:
            # Game is solved correctly so we can disable clear and check button
            self.updateButtons("disable")
            self.Timer.stop()
            self.solvedFlag = 1
        else:
            self.Check.setStyleSheet(u"background-color: rgba(200, 0, 0, 0.4)")
            self.solvedFlag = 0

    def setSolverTime(self):
        '''
        This function display the time the solver needed inside the game.
        The time display format has to be changed for that to allow ms.
        '''

        # Rouding the time for solving to ms
        solverTimeMS = int(round(self.solverTime))
        secs = 0 
        ms = 0
        #Check if the time is greater then 1000ms
        if solverTimeMS >= 1000:
            secs = solverTimeMS//1000
            ms = solverTimeMS - (secs*1000)
        else:
            ms = solverTimeMS
        # The time for solving as QTime format to be displayed in game
        self.displaySolverTime.setHMS(0,0,secs,ms) 
        # Set timeViewer to displaySolverTime 
        self.TimeViewer.setDisplayFormat(QCoreApplication.translate("MainWindow", u"mm:ss.zzz", None))
        self.TimeViewer.setTime(self.displaySolverTime)

    def updateTime(self):
        '''
        This function is called every second by the timer from fillBoard 
        to update the TimeViewer to show the current game runtime.
        '''

        # Adding a second to the runtime
        self.runtime = self.runtime.addSecs(1) # addSecs retruns a new runtime object 
        
        # Print for debugging purposes
        #print("Runtime: ", self.runtime.toString("hh:mm:ss"))
        
        # Update the timer inside the game window
        self.TimeViewer.setTime(self.runtime) 

    def resetTime(self):
        '''
        This function resets the timer and timeViewer as well as sets the display format
        back to default (hh:mm:ss).
        '''

        # Reset time on quit or clear button clicked events -> done through the eventHandler()
        self.Timer.stop()
        self.runtime.setHMS(0,0,0,0)
        self.TimeViewer.setDisplayFormat(QCoreApplication.translate("MainWindow", u"hh:mm:ss", None))
        self.TimeViewer.setTime(self.runtime)
    
    def addScoresToBoard(self):
        '''
        This function is laoding all the scores from the text file and 
        displays them inside the table on the menu page. 
        '''

        # First we need to read the content of scores.txt
        file = open('scores.txt', 'r')
        lines = file.readlines()
        # Delete all rows to avoid adding rows twice or more
        self.ScoreTable.setRowCount(0)

        # Go through each line and place elements into column
        for line in lines:
            # Remove the line break so it's not disturbing inside the gameboard
            line = line.strip("\n")
            # Create a list of elements 
            elements = line.split(",")
            # Insert a new row into the table behind the last row
            self.ScoreTable.insertRow(self.ScoreTable.rowCount())
            # Iterate through the element list and get index for column number
            for index, element in enumerate(elements):
                # Create a new tablewidget item in which the element text is placed
                item = QTableWidgetItem(element)
                # Change the background  color of the cell according to the difficulty
                if element == "Easy":
                    item.setBackground(QColor("green"))
                elif element =="Medium":
                    item.setBackground(QColor("orange"))
                elif element == "Hard":
                    item.setBackground(QColor("red"))
                # Disable the item so the user cant change the text + center text
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignCenter)
                # Finally place the item into the table widget to be displayed
                self.ScoreTable.setItem(self.ScoreTable.rowCount()-1, index, item)

    def storeScore(self):
        '''
        This function stores a finished game when the user quits the game page
        by writing difficulty, time, hints and solvingMethod into a txt file.
        According to the solvingMethodFlags the time and solve output is changed.
        '''

        # Check if the board is solved before closing
        if self.solvedFlag == 1:
            # Open to score text file in appeding + reading mode (a+)
            file = open('scores.txt', 'a+')
            # Create default string for solving method and time 
            solvingMethod = "player"
            time = self.runtime.toString("hh:mm:ss")
            # Change solving method string when auto.solving was used
            if self.solvingMethodFlag == 1:
                solvingMethod = "auto"
                # Change time format to get ms as well
                time = self.displaySolverTime.toString("mm:ss.zzz")
            # Generate new Score string 
            newScore = self.diffStr + "," + time + "," + str(self.hintCounter) + "," + solvingMethod + "\n"
            # Write score string to text file
            file.writelines(newScore)
            # Close file properly
            file.close()
            #Reset Flag
            self.solvedFlag = 0

        # When new scores have been safed, we have to update the table 
        self.addScoresToBoard()

    def updateButtons(self, state:str):
        '''
        This function enables or disables the buttons on the game page.
        '''

        if state == "enable":
            self.Hint.setEnabled(True)
            self.AutoSolve.setEnabled(True)
            self.Clear.setEnabled(True)
            self.Check.setStyleSheet("")
            self.Check.setEnabled(True)
        elif state == "disable":
            self.Hint.setEnabled(False)
            self.AutoSolve.setEnabled(False)
            self.Clear.setEnabled(False)
            self.Check.setEnabled(False)
            self.Check.setStyleSheet(u"background-color: rgba(0, 200, 0, 0.4)")
            
    def eventHandler(self, event):
        '''
        This function represents the event handeling for the buttons.
        This function is the state machine of the game.
        '''

        match event:
            case "Easy":
                self.generateBoards(50)
                self.fillBoard()
                self.diffStr = "Easy"
                self.Windows.setCurrentIndex(1)

            case "Medium":
                self.generateBoards(40)
                self.fillBoard()
                self.diffStr = "Medium"
                self.Windows.setCurrentIndex(1)

            case "Hard":
                self.generateBoards(30)
                self.fillBoard()
                self.diffStr = "Hard"
                self.Windows.setCurrentIndex(1)

            case "Hint":
                self.setHint()

            case "Solve":
                self.solveBoard()

            case "Clear":
                self.resetTime()
                self.resetBoard()
                # Renew the userGrid when user wants to start over
                self.userGrid = deepcopy(self.gameGrid)
                self.fillBoard()
                    
            case "Check":
                self.checkBoard()

            case "Quit":
                self.storeScore()
                self.resetTime()
                self.resetBoard()
                self.removeOldBoardData()
                self.updateButtons("enable")
                self.Windows.setCurrentIndex(0)

    def setupUi(self):
        '''
        This function loads main parameters and elements to the game.
        It also creates the events which control the game.
        This function needs to be called inside the main function.
        '''

        self.setupMainWindow()
        self.setupWindows()
        self.retranslateUi()

        # Events from main page 
        self.Easy.clicked.connect(lambda: self.eventHandler("Easy"))
        self.Medium.clicked.connect(lambda: self.eventHandler("Medium"))
        self.Hard.clicked.connect(lambda: self.eventHandler("Hard"))
        
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
        '''
        This function simply shows the MainWindow on the screen.
        '''

        self.MainWindow.show()


def main():
    '''
    This function starts the game.
    '''

    app = QApplication([])
    ui = Sudoku_UI()
    ui.setupUi()
    ui.loadUi()
    app.exec()

if __name__ == "__main__":
    main()