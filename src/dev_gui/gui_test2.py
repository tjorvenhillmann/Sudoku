# ------------------------------------------
# This is a cleaned up version of gui_test1.py 
# ------------------------------------------

# PyQt5 dependencies
from PyQt5.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PyQt5.QtGui import (QCursor, QFont)
from PyQt5.QtWidgets import *

# Main class with all the Window/Widgets properties 
class Gui:
    def __init__(self):
        self.MainWindow = QMainWindow()

    def setupMainWindow(self):
        font = QFont()
        font.setKerning(True)
        # Main Window Properties
        self.MainWindow.resize(1024, 768)
        self.MainWindow.setFont(font)
        self.MainWindow.setCursor(QCursor(Qt.ArrowCursor))
        self.MainWindow.setMouseTracking(False)
        self.MainWindow.setAutoFillBackground(False)
        # Central Widget Properties
        self.centralwidget = QWidget(self.MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

    def setupWindows(self):
        # Windows/Widget setction -> Main and Game Window so far
        self.Windows = QStackedWidget(self.centralwidget)
        self.Windows.setObjectName(u"Windows")
        self.Windows.setGeometry(QRect(0, 0, 1024, 768))
        self.Windows.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.Windows.setFrameShape(QFrame.NoFrame)
        self.Windows.setLineWidth(1)
    
        self.setupMainPage()
        self.setupGamePage()

        self.MainWindow.setCentralWidget(self.centralwidget)

    def setupMainPage(self):
        # Main Window properties
        self.Main = QWidget()
        self.Main.setObjectName(u"Main")
        self.Main.setAutoFillBackground(False)
        self.Main.setStyleSheet(u"color: 0 0 0")

        # Objects inside the main window
        self.HeaderPage1 = QLabel(self.Main)
        self.LabelScoreBoard = QLabel(self.Main)
        self.Scoreboard = QScrollArea(self.Main)
        self.ContentArea = QWidget()
        self.LabelNewGame = QLabel(self.Main)
        self.Easy = QPushButton(self.Main)
        self.Medium = QPushButton(self.Main)
        self.Hard = QPushButton(self.Main)
        self.Insane = QPushButton(self.Main)
        
        # Properties for objects inside Main-Widget
        # -- Label "Sudoku" 
        self.HeaderPage1.setObjectName(u"HeaderPage1")
        self.HeaderPage1.setGeometry(QRect(412, 0, 200, 80))
        font4 = QFont()
        font4.setPointSize(32)
        font4.setBold(False)
        font4.setWeight(50)
        self.HeaderPage1.setFont(font4)
        
        # -- Label "ScoreBoard"
        self.LabelScoreBoard.setObjectName(u"LabelScoreBoard")
        self.LabelScoreBoard.setGeometry(QRect(112, 140, 141, 40))
        font3 = QFont()
        font3.setPointSize(14)
        font3.setBold(True)
        font3.setItalic(False)
        font3.setUnderline(False)
        font3.setWeight(75)
        font3.setKerning(True)
        self.LabelScoreBoard.setFont(font3)
        
        # Properties ScoreBoard
        self.Scoreboard.setObjectName(u"Scoreboard")
        self.Scoreboard.setGeometry(QRect(112, 190, 800, 301))
        self.Scoreboard.setFrameShape(QFrame.StyledPanel)
        self.Scoreboard.setFrameShadow(QFrame.Plain)
        self.Scoreboard.setLineWidth(4)
        self.Scoreboard.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.Scoreboard.setWidgetResizable(True)
        self.ContentArea = QWidget()
        self.ContentArea.setObjectName(u"ContentArea")
        self.ContentArea.setGeometry(QRect(0, 0, 777, 299))
        self.Scoreboard.setWidget(self.ContentArea)
        
        # -- Lable "New Game"
        self.LabelNewGame = QLabel(self.Main)
        self.LabelNewGame.setObjectName(u"LabelNewGame")
        self.LabelNewGame.setGeometry(QRect(112, 520, 141, 40))
        font2 = QFont()
        font2.setPointSize(14)
        font2.setBold(True)
        font2.setWeight(75)
        font2.setKerning(True)
        self.LabelNewGame.setFont(font2)
        
        # Porperties for the 4 diffrent difficulty buttons
        font1 = QFont()
        font1.setPointSize(11)
        self.Easy.setObjectName(u"Easy")
        self.Easy.setGeometry(QRect(112, 560, 160, 80))
        self.Easy.setFont(font1)
        self.Medium.setObjectName(u"Medium")
        self.Medium.setGeometry(QRect(322, 560, 160, 80))
        self.Medium.setFont(font1)
        self.Hard.setObjectName(u"Hard")
        self.Hard.setGeometry(QRect(542, 560, 160, 80))
        self.Hard.setFont(font1)
        self.Insane.setObjectName(u"Insane")
        self.Insane.setGeometry(QRect(752, 560, 160, 80))
        self.Insane.setFont(font1)

        # Adding the widget to the stacked Widget "Windows" 
        self.Windows.addWidget(self.Main)
        
    def setupGamePage(self):
        # Game Window Properties
        self.Game = QWidget()
        self.Game.setObjectName(u"Game")

        # Objects inside the game window
        self.Back = QPushButton(self.Game)
        self.Hint = QPushButton(self.Game)
        self.AutoSolve = QPushButton(self.Game)
        self.Check = QPushButton(self.Game)
        self.Timer = QTimeEdit(self.Game)
        self.Board = QTableWidget(self.Game)
        
        # Properties for objects inside Game-Widget
        # -- Label "Sudoku"
        self.HeaderPage = QLabel(self.Game)
        self.HeaderPage.setObjectName(u"HeaderPage")
        self.HeaderPage.setGeometry(QRect(412, 0, 200, 80))
        font5 = QFont()
        font5.setPointSize(32)
        self.HeaderPage.setFont(font5)
        
        # Back button properties
        self.Back.setObjectName(u"Back")
        self.Back.setGeometry(QRect(10, 10, 50, 50))
        font7 = QFont()
        font7.setPointSize(18)
        self.Back.setFont(font7)
        
        # Hint/AutoSolve/Check button properties
        font1 = QFont()
        font1.setPointSize(11)
        self.Hint.setObjectName(u"Hint")
        self.Hint.setGeometry(QRect(780, 290, 160, 80))
        self.Hint.setFont(font1)
        self.AutoSolve.setObjectName(u"AutoSolve")
        self.AutoSolve.setGeometry(QRect(780, 390, 160, 80))
        self.AutoSolve.setFont(font1)
        self.Check.setObjectName(u"Check")
        self.Check.setGeometry(QRect(780, 490, 160, 80))
        self.Check.setFont(font1)

        # Timer properties
        self.Timer.setObjectName(u"Timer")
        self.Timer.setGeometry(QRect(780, 100, 160, 80))
        font6 = QFont()
        font6.setPointSize(20)
        font6.setBold(True)
        font6.setWeight(75)
        self.Timer.setFont(font6)
        self.Timer.setFrame(True)
        self.Timer.setAlignment(Qt.AlignCenter)
        self.Timer.setButtonSymbols(QAbstractSpinBox.NoButtons)

        # Adding rows and columns to the Board
        if (self.Board.columnCount() < 9):
            self.Board.setColumnCount(9)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setText(u"Col0");
        self.Board.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.Board.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.Board.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.Board.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.Board.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.Board.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.Board.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.Board.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.Board.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        if (self.Board.rowCount() < 9):
            self.Board.setRowCount(9)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.Board.setVerticalHeaderItem(0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.Board.setVerticalHeaderItem(1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.Board.setVerticalHeaderItem(2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.Board.setVerticalHeaderItem(3, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.Board.setVerticalHeaderItem(4, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.Board.setVerticalHeaderItem(5, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.Board.setVerticalHeaderItem(6, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.Board.setVerticalHeaderItem(7, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.Board.setVerticalHeaderItem(8, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        __qtablewidgetitem18.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem18.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsEnabled);

        # Board properties
        self.Board.setItem(0, 0, __qtablewidgetitem18)
        self.Board.setObjectName(u"Board")
        self.Board.setGeometry(QRect(90, 100, 630, 630))
        self.Board.setFrameShape(QFrame.Box)
        self.Board.setFrameShadow(QFrame.Plain)
        self.Board.setLineWidth(3)
        self.Board.setMidLineWidth(0)
        self.Board.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Board.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Board.setShowGrid(True)
        self.Board.setGridStyle(Qt.SolidLine)
        self.Board.setSortingEnabled(False)
        self.Board.setWordWrap(True)
        self.Board.setCornerButtonEnabled(True)
        self.Board.horizontalHeader().setVisible(False)
        self.Board.horizontalHeader().setCascadingSectionResizes(False)
        self.Board.horizontalHeader().setMinimumSectionSize(7)
        self.Board.horizontalHeader().setDefaultSectionSize(70)
        self.Board.horizontalHeader().setHighlightSections(False)
        self.Board.verticalHeader().setVisible(False)
        self.Board.verticalHeader().setMinimumSectionSize(70)
        self.Board.verticalHeader().setDefaultSectionSize(70)
        self.Board.verticalHeader().setHighlightSections(False)

        # Adding thicke horizontal and vertical lines to the grid
        self.Hor1 = QFrame(self.Game)
        self.Hor1.setObjectName(u"Hor1")
        self.Hor1.setGeometry(QRect(90, 310, 630, 3))
        self.Hor1.setFrameShadow(QFrame.Plain)
        self.Hor1.setLineWidth(3)
        self.Hor1.setFrameShape(QFrame.HLine)
        self.Hor2 = QFrame(self.Game)
        self.Hor2.setObjectName(u"Hor2")
        self.Hor2.setGeometry(QRect(90, 520, 630, 3))
        self.Hor2.setFrameShadow(QFrame.Plain)
        self.Hor2.setLineWidth(3)
        self.Hor2.setFrameShape(QFrame.HLine)
        self.Ver1 = QFrame(self.Game)
        self.Ver1.setObjectName(u"Ver1")
        self.Ver1.setGeometry(QRect(300, 100, 3, 630))
        self.Ver1.setFrameShadow(QFrame.Plain)
        self.Ver1.setLineWidth(3)
        self.Ver1.setFrameShape(QFrame.VLine)
        self.Ver2 = QFrame(self.Game)
        self.Ver2.setObjectName(u"Ver2")
        self.Ver2.setGeometry(QRect(510, 100, 3, 630))
        self.Ver2.setFrameShadow(QFrame.Plain)
        self.Ver2.setLineWidth(3)
        self.Ver2.setFrameShape(QFrame.VLine)

        # Adding the widget to the stacked Widget "Windows" 
        self.Windows.addWidget(self.Game)
    
    def retranslateUi(self):
        self.MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sudoku", None))
        self.Medium.setText(QCoreApplication.translate("MainWindow", u"Medium", None))
        self.LabelNewGame.setText(QCoreApplication.translate("MainWindow", u"New Game:", None))
        self.Easy.setText(QCoreApplication.translate("MainWindow", u"Easy", None))
        self.LabelScoreBoard.setText(QCoreApplication.translate("MainWindow", u"ScoreBoard:", None))
        self.Insane.setText(QCoreApplication.translate("MainWindow", u"Insane", None))
        self.Hard.setText(QCoreApplication.translate("MainWindow", u"Hard", None))
        self.HeaderPage1.setText(QCoreApplication.translate("MainWindow", u"SUDOKU", None))
        ___qtablewidgetitem = self.Board.horizontalHeaderItem(1)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Col1", None));
        ___qtablewidgetitem1 = self.Board.horizontalHeaderItem(2)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Col2", None));
        ___qtablewidgetitem2 = self.Board.horizontalHeaderItem(3)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Col3", None));
        ___qtablewidgetitem3 = self.Board.horizontalHeaderItem(4)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Col4", None));
        ___qtablewidgetitem4 = self.Board.horizontalHeaderItem(5)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Col5", None));
        ___qtablewidgetitem5 = self.Board.horizontalHeaderItem(6)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Col6", None));
        ___qtablewidgetitem6 = self.Board.horizontalHeaderItem(7)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Col7", None));
        ___qtablewidgetitem7 = self.Board.horizontalHeaderItem(8)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Col8", None));
        ___qtablewidgetitem8 = self.Board.verticalHeaderItem(0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Row0", None));
        ___qtablewidgetitem9 = self.Board.verticalHeaderItem(1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Row1", None));
        ___qtablewidgetitem10 = self.Board.verticalHeaderItem(2)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Row2", None));
        ___qtablewidgetitem11 = self.Board.verticalHeaderItem(3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Row3", None));
        ___qtablewidgetitem12 = self.Board.verticalHeaderItem(4)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Row4", None));
        ___qtablewidgetitem13 = self.Board.verticalHeaderItem(5)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Row5", None));
        ___qtablewidgetitem14 = self.Board.verticalHeaderItem(6)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Row6", None));
        ___qtablewidgetitem15 = self.Board.verticalHeaderItem(7)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Row7", None));
        ___qtablewidgetitem16 = self.Board.verticalHeaderItem(8)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Row8", None));

        __sortingEnabled = self.Board.isSortingEnabled()
        self.Board.setSortingEnabled(False)
        self.Board.setSortingEnabled(__sortingEnabled)

        self.Hint.setText(QCoreApplication.translate("MainWindow", u"Hint", None))
        self.AutoSolve.setText(QCoreApplication.translate("MainWindow", u"Auto-Solve", None))
        self.Check.setText(QCoreApplication.translate("MainWindow", u"Check", None))
        self.HeaderPage.setText(QCoreApplication.translate("MainWindow", u"SUDOKU", None))
        self.Back.setText(QCoreApplication.translate("MainWindow", u"<-", None))

    def setupUi(self):
        self.setupMainWindow()
        self.setupWindows()
        self.retranslateUi()

        self.Easy.clicked.connect(lambda: self.Windows.setCurrentIndex(1))
        self.Medium.clicked.connect(lambda: self.Windows.setCurrentIndex(1))
        self.Hard.clicked.connect(lambda: self.Windows.setCurrentIndex(1))
        self.Insane.clicked.connect(lambda: self.Windows.setCurrentIndex(1))
        self.Back.clicked.connect(lambda: self.Windows.setCurrentIndex(0))

        self.Windows.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(self.MainWindow)

    def loadGui(self):
        self.MainWindow.show()

def main():
    app = QApplication([])
    gui = Gui()
    gui.setupUi()
    gui.loadGui()
    app.exec()

if __name__ == "__main__":
    main()