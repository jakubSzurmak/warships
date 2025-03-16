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
        self.shipFields = []
        self.shipOptions = []

        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()

        self.myOnlineStatus = QtWidgets.QLabel("You are online")
        self.enemyOnlineStatus = QtWidgets.QLabel("Enemy is Online")

        self.selectionBoard = {
            0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []
        }

        self.letterToIndex = {
            'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10
        }

        self.indexToLetter = {v: k for k, v in self.letterToIndex.items()}


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

    def locateSurroundingFields(self, baseX, baseY):
        checks = [-1, 1]
        valid = []

        for i in checks:
            if 1 <= self.letterToIndex[baseX] + i <= 10:
                valid.append((self.indexToLetter[self.letterToIndex[baseX] + i], baseY))
            if 1 <= baseY + i <= 10:
                valid.append((baseX, baseY + i))
        return valid

    def customizeButtonForShip(self):
        pass

    def customizeButtonForNextMove(self):
        pass

    def updateNextMoveOptions(self, baseX, baseY):
        if self.shipMg.getCurrentShipOption() != 1:
            if self.shipMg.getRemainingShipSelections() == 0:
                self.shipMg.setShipAwaitingApproval(self.shipMg.getCurrentShipOption())

            if self.shipMg.getRemainingShipSelections() == self.shipMg.getCurrentShipOption() - 1:
                fieldsToUpdate = self.locateSurroundingFields(baseX, baseY)
                for pair in fieldsToUpdate:

                    pass
            else:
                pass


    def markShipFields(self, x, y):
        if self.shipMg.getCurrentShipOption() is not None:
            self.disableForbiddenFields()
            self.shipFields.append((x, y))
            self.selectionBoard[self.letterToIndex[x]][y].setEnabled(True)
            self.updateNextMoveOptions(x, y)


    def disableForbiddenFields(self):
        for i in range(11):
            for j in range(11):
                if self.selectionBoard[i][j].isEnabled():
                    self.selectionBoard[i][j].setEnabled(False)

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
                                                                     QPushButton:disabled {
                                                                        background-color: gray;
                                                                        border: 2px solid darkgray;
                                                                    }
                                                                """)
                        self.selectionBoard[i][j].clicked.connect(lambda checked, r=az[i], c=j:
                                                                  (self.shipMg.shipFieldSelected(r, c),
                                                                   self.markShipFields(r, c))
                                                                  )

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
