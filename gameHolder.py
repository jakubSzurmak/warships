import shipManager
from shipManager import QtWidgets


def locateSurroundingFields(baseX, baseY, mode):
    print("gh.locateSurr")

    if mode == "surround":
        # Top-left, Top, Top-right, Right, Bottom-left, Bottom, Bottom-right
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    elif mode == "leftRight":
        # Top, right, left, bottom
        directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    elif mode == "diagonals":
        # Top-left, Top-right, bottom-left, bottom-right
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    else:
        exit(69)

    surrounding_fields = [
        (baseX + dx, baseY + dy) for dx, dy in directions
        if 1 <= baseX + dx < 11 and 1 <= baseY + dy < 11
    ]

    return surrounding_fields


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

        self.acceptButton = QtWidgets.QPushButton("Approve")
        self.backButton = QtWidgets.QPushButton("Back")
        self.resetButton = QtWidgets.QPushButton("Reset")
        self.quitButton = QtWidgets.QPushButton("Exit")

        self.boardLayout = QtWidgets.QGridLayout()
        self.forbiddenFields = []
        self.lastFieldSelections = []

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

        self.moveHistory = []
        self.nextFieldOptions = []

    def getWindow(self):
        print("gh.getWindow")
        return self.window

    def getTabs(self):
        print("gh.getTabs")
        return self.tabs

    def getApp(self):
        print("gh.getApp")
        return self.app

    # save the sequence of ship options approvals, for ship back >
    # pop each code and for code in ship fields remove and restyle

    def initRightSide(self):
        print("gh.initRight")
        self.layout.addLayout(self.rightSide, 0, 2)
        self.rightSide.addWidget(self.myOnlineStatus)
        self.rightSide.addWidget(self.enemyOnlineStatus)
        [self.rightSide.addWidget(x) for x in self.shipMg.getShipOptionButtons()]

    def initLeftSide(self):
        print("gh.initLeft")
        self.layout.addLayout(self.leftSide, 0, 0)
        self.initSelectionBoard()

    def connectButtons(self):
        print("gh.initConnect")
        if self.tabs.isTabEnabled(0):
            self.acceptButton.clicked.connect(self.pullApproval)
            self.backButton.clicked.connect(self.shipMg.shipSelectionRollback)
            self.resetButton.clicked.connect(self.shipMg.shipsSelectionRestart)
            self.quitButton.clicked.connect(quit)
        else:
            pass

    def initButtonPanel(self):
        print("gh.initButtonPanel")
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

    def customizeButtonForShip(self, x, y):
        print("gh.customForShip")
        self.selectionBoard[x][y].setStyleSheet("""
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
                                                        background-color: purple;
                                                        border: 3px solid black;
                                                    }
                                                """)

    def enableBoardFields(self):
        print("gh.enableBoardFields")
        for i in range(11):
            for j in range(11):
                if i != 0 and j != 0 and ((i, j) not in self.forbiddenFields):
                    self.selectionBoard[i][j].setEnabled(True)

    def pullApproval(self):
        print("gh.pullApproval")
        if self.shipMg.getShipAwaitingApproval() == self.shipMg.getCurrentShipOption():
            self.shipMg.shipSelectionConfirmed()
            self.enableBoardFields()
            self.shipMg.switchShipOptions(False)

        # unlock board without ship and fields arround it

    def updateNextMoveOptions(self, baseX, baseY):
        print("gh.updateNextMoveOptions")

        if self.shipMg.getCurrentShipOption() != 1:
            # enable fields in row and col for selected +-3,
            # append to moveHistory the amount of forbidden to remove if back occurs,

            self.forbiddenFields.append((self.letterToIndex[baseX], baseY))
            [self.forbiddenFields.append((x[0], x[1])) for x
             in locateSurroundingFields(self.letterToIndex[baseX], baseY, "diagonals")]

            if self.shipMg.getRemainingShipSelections() != 0:
                self.enableBoardFields()
            else:
                for x in self.moveHistory:
                    for y in locateSurroundingFields(self.letterToIndex[x[0]], x[1], "leftRight"):
                        if y not in self.forbiddenFields:
                            self.forbiddenFields.append(y)

                # forbid right/left/top/bot

        else:
            self.shipMg.setShipAwaitingApproval(self.shipMg.getCurrentShipOption())
            [self.forbiddenFields.append((x[0], x[1])) for x
             in locateSurroundingFields(self.letterToIndex[baseX], baseY, "surround")]
            self.forbiddenFields.append((self.letterToIndex[baseX], baseY))

    def markShipFields(self, x, y):
        print("gh.markShipFields")
        if self.shipMg.getCurrentShipOption() is not None:
            self.shipMg.shipFieldSelected(x, y)

            # self.shipFields.append((x, y))
            self.customizeButtonForShip(self.letterToIndex[x], y)
            self.moveHistory.append((x, y))
            self.disableBoardFields()
            self.updateNextMoveOptions(x, y)

    def disableBoardFields(self):
        print("gh.disableBoardFields")
        for i in range(11):
            for j in range(11):
                if self.selectionBoard[i][j].isEnabled():
                    self.selectionBoard[i][j].setEnabled(False)

    def initSelectionBoard(self):
        print("gh.initSelectionBoard")
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
                                                                  self.markShipFields(r, c))

                self.selectionBoard[i][j].setFixedSize(60, 55)
                self.boardLayout.addWidget(self.selectionBoard[i][j], i, j)

    def startState(self):
        print("gh.startState")
        self.tabs.setLayout(self.layout)
        self.window.setCentralWidget(self.tabs)

        self.tabs.addTab(self.tab1, "Prepare for Battle")
        self.tabs.addTab(self.tab2, "Battle")

        self.tabs.setTabEnabled(1, False)

        self.initLeftSide()
        self.initRightSide()
        self.initButtonPanel()
