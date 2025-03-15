import shipManager
from shipManager import QtWidgets


class GameHolder:

    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.shipMg = shipManager.ShipManager()
        self.window = QtWidgets.QMainWindow()
        self.tabs = QtWidgets.QTabWidget()

        self.layout = QtWidgets.QGridLayout()

        self.leftSide = QtWidgets.QVBoxLayout()

        self.rightSide = QtWidgets.QVBoxLayout()
        self.buttonPanel = QtWidgets.QHBoxLayout()

        self.acceptButton = QtWidgets.QPushButton("Appprove")
        self.backButton = QtWidgets.QPushButton("Back")
        self.resetButton = QtWidgets.QPushButton("Reset")
        self.quitButton = QtWidgets.QPushButton("Exit")

        self.boardLayout = QtWidgets.QGridLayout()

        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()

        self.myOnlineStatus = QtWidgets.QLabel("You are online")
        self.enemyOnlineStatus = QtWidgets.QLabel("Enemy is Online")

        self.selectionBoard = {
            0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []
        }

    def getWindow(self):
        return self.window

    def getTabs(self):
        return self.tabs

    def getApp(self):
        return self.app

    def initRightSide(self):
        self.layout.addLayout(self.rightSide, 0, 2)
        self.rightSide.addWidget(self.myOnlineStatus)
        self.rightSide.addWidget(self.enemyOnlineStatus)
        [self.rightSide.addWidget(x) for x in self.shipMg.getShipOptionButtons()]

    def initLeftSide(self):
        self.layout.addLayout(self.leftSide, 0, 0)
        self.initSelectionBoard()

    def connectButtons(self):
        if self.tabs.isTabEnabled(0):
            self.acceptButton.clicked.connect(self.shipMg.shipSelectionConfirmed)
            self.backButton.clicked.connect(self.shipMg.shipSelectionRollback)
            self.resetButton.clicked.connect(self.shipMg.shipsSelectionRestart)
            self.quitButton.clicked.connect(quit)
        else:
            pass


    def initButtonPanel(self):
        self.layout.addLayout(self.buttonPanel, 1, 0, 1, 3)
        self.acceptButton.setStyleSheet("""
                                            QPushButton { 
                                                background-color:lightgrey;
                                                border: 2px solid black;
                                                font-size: 16px;
                                                padding: 0px;
                                            }
                                            QPushButton:hover {
                                                background-color: green;
                                                color: white;
                                            }
                                        """)
        self.buttonPanel.addWidget(self.acceptButton)

        self.backButton.setStyleSheet("""
                                            QPushButton { 
                                                background-color:lightgrey;
                                                border: 2px solid black;
                                                font-size: 16px;
                                                padding: 0px;
                                            }
                                            QPushButton:hover {
                                                background-color: yellow;
                                                color: black;
                                            }
                                        """)
        self.buttonPanel.addWidget(self.backButton)

        self.resetButton.setStyleSheet("""
                                            QPushButton { 
                                                background-color:lightgrey;
                                                border: 2px solid black;
                                                font-size: 16px;
                                                padding: 0px;
                                            }
                                            QPushButton:hover {
                                                background-color: red;
                                                color: white;
                                            }
                                        """)
        self.buttonPanel.addWidget(self.resetButton)

        self.quitButton.setStyleSheet("""
                                                    QPushButton { 
                                                        background-color:lightgrey;
                                                        border: 2px solid black;
                                                        font-size: 16px;
                                                        padding: 0px;
                                                    }
                                                    QPushButton:hover {
                                                        background-color: black;
                                                        color: white;
                                                    }
                                                """)

        self.buttonPanel.addWidget(self.quitButton)
        self.connectButtons()

    def initSelectionBoard(self):
        az = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '']
        self.leftSide.addLayout(self.boardLayout)
        self.boardLayout.setSpacing(0)
        for i in range(len(az)):
            self.selectionBoard[i].append(QtWidgets.QPushButton(az[i]))
            self.selectionBoard[i][0].setEnabled(False)
            self.selectionBoard[i][0].setStyleSheet("""
                                                       QPushButton {
                                                           background-color: salmon;
                                                           color: black;
                                                           border: 3px solid black;
                                                           font-size: 20px;
                                                           padding: 0px;
                                                       }
                                                   """)
            for j in range(len(nums)):
                if i == 0:
                    self.selectionBoard[i].append(QtWidgets.QPushButton(nums[j]))
                    self.selectionBoard[i][j].setStyleSheet("""
                                                                QPushButton {
                                                                    background-color: salmon;
                                                                    color: black;
                                                                    border: 3px solid black;
                                                                    font-size: 20px;
                                                                    padding: 0px;
                                                                }
                                                            """)
                    self.selectionBoard[i][j].setEnabled(False)

                else:
                    self.selectionBoard[i].append(QtWidgets.QPushButton())
                    if j != 0:
                        self.selectionBoard[i][j].setStyleSheet("""
                                                                    QPushButton {
                                                                        background-color: lightblue;
                                                                        border: 2px solid black;
                                                                        font-size: 16px;
                                                                        padding: 0px;
                                                                    }
                                                                    QPushButton:hover {
                                                                        background-color: orange;
                                                                    }
                                                                """)
                        self.selectionBoard[i][j].clicked.connect(lambda checked, r=az[i], c=j:
                                                                  self.shipMg.shipFieldSelected(r, c))

                self.selectionBoard[i][j].setFixedSize(60, 55)
                self.boardLayout.addWidget(self.selectionBoard[i][j], i, j)

    def startState(self):
        self.tabs.setLayout(self.layout)
        self.window.setCentralWidget(self.tabs)

        self.tabs.addTab(self.tab1, "Prepare for Battle")
        self.tabs.addTab(self.tab2, "Battle")

        self.tabs.setTabEnabled(1, False)

        self.initLeftSide()
        self.initRightSide()
        self.initButtonPanel()
