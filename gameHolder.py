import shipManager
import battleManager
from shipManager import QtWidgets


# Static function for getting coordinates arround (baseX, baseY) field
def locateSurroundingFields(baseX, baseY, mode):
    # print("gh.locateSurr")

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

    def __init__(self, clientId):
        self.app = QtWidgets.QApplication([])
        self.networkMg = None
        self.clientId = clientId

        self.shipMg = shipManager.ShipManager()
        self.window = QtWidgets.QMainWindow()
        self.tabs = QtWidgets.QTabWidget()

        self.tabSignalsConnected = False

        
        self.battleMg = None #Initialized when all the ships are placed and battle starts

        # Layout scheme: Main window -> 2 tabs -> (1st tab):
        # Main layout   3 columns and 2 rows
        #               -> left side[ inside it boardLayout for keeping button grid] 2 columns in 1st row
        #               -> right side[ inside it control labels for informing the user and selecting ship option]
        #                   1 col in 1st row
        #               -> Button panel underneath left and right side for every button 3 columns in 2nd row
        self.layout = QtWidgets.QGridLayout()

        self.leftSide = QtWidgets.QVBoxLayout()

        self.rightSide = QtWidgets.QVBoxLayout()
        self.buttonPanel = QtWidgets.QHBoxLayout()

        self.acceptButton = QtWidgets.QPushButton("Approve")
        self.backButton = QtWidgets.QPushButton("Back")
        self.resetButton = QtWidgets.QPushButton("Reset")
        self.quitButton = QtWidgets.QPushButton("Exit")

        self.boardLayout = QtWidgets.QGridLayout()

        # Array holding fields disallowed from user selection
        self.forbiddenFields = []

        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()

        self.myOnlineStatus = QtWidgets.QLabel("You are online")
        self.enemyOnlineStatus = QtWidgets.QLabel("Enemy is Online")

        # Dict for holding buttons on the board, access via matrix(row, column) not x,y
        self.selectionBoard = {
            0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []
        }

        # Helping dictionary for converting indeces to letters and letters to indeces
        # Row 0 is always inactive as it is the legend for displaying the column number -> A = 1
        self.letterToIndex = {
            'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10
        }
        self.indexToLetter = {v: k for k, v in self.letterToIndex.items()}

        # After selecting ship option each selected field lands here, flushed after confirmation
        self.moveHistory = []

        self.allShipsPlaced = False

    def getWindow(self):
        # print("gh.getWindow")
        return self.window

    def getNetworkMg(self):
        return self.networkMg

    def getClientId(self):
        return self.clientId

    def getTabs(self):
        # print("gh.getTabs")
        return self.tabs

    def getApp(self):
        # print("gh.getApp")
        return self.app

    def initRightSide(self):
        # print("gh.initRight")
        self.layout.addLayout(self.rightSide, 0, 2)
        self.rightSide.addWidget(self.myOnlineStatus)
        self.rightSide.addWidget(self.enemyOnlineStatus)
        [self.rightSide.addWidget(x) for x in self.shipMg.getShipOptionButtons()]

    def initLeftSide(self):
        # print("gh.initLeft")
        self.layout.addLayout(self.leftSide, 0, 0)
        self.initSelectionBoard()

    def connectButtons(self):
        # print("gh.initConnect")
        # After connect don't do connect(f()) but connect(f) as f() calls immediately on init
        if self.tabs.isTabEnabled(0):
            self.acceptButton.clicked.connect(self.pullApproval)
            self.backButton.clicked.connect(self.revertSingleSelection)
            self.resetButton.clicked.connect(self.resetSelectionState)
            self.quitButton.clicked.connect(quit)
        else:
            # To utilization or deletion
            pass


    def initButtonPanel(self):
        # print("gh.initButtonPanel")
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
        self.backButton.setEnabled(False)

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
        # print("gh.customForShip")
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

    # After clicking Back button removes lastly approved ship
    def revertSingleSelection(self):
        self.forbiddenFields = sorted(self.forbiddenFields)
        lastFields = self.shipMg.shipSelectionRollback()

        # If last ship was 1 block remove everything arround
        if len(lastFields) == 1:
            mode = "surround"
        else:
            # To not duplicate removals we cannot remove all surroundings for all blocks, first and last block manually
            # others automatically but only diagonals
            mode = "diagonals"
            youngest, oldest = sorted(lastFields)[0], sorted(lastFields)[-1]
            if youngest[0] == oldest[0]:
                if (self.letterToIndex[youngest[0]], youngest[1]-1) in self.forbiddenFields:
                    self.forbiddenFields.remove((self.letterToIndex[youngest[0]], youngest[1]-1))

                if (self.letterToIndex[oldest[0]], oldest[1]+1) in self.forbiddenFields:
                    self.forbiddenFields.remove((self.letterToIndex[oldest[0]], oldest[1] + 1))

            if youngest[1] == oldest[1]:
                temp = self.letterToIndex[youngest[0]]
                if (temp - 1, youngest[1]) in self.forbiddenFields:
                    self.forbiddenFields.remove((temp - 1, youngest[1]))

                if (self.letterToIndex[oldest[0]] + 1, oldest[1]) in self.forbiddenFields:
                    self.forbiddenFields.remove((self.letterToIndex[oldest[0]] + 1, oldest[1]))

        for i in lastFields:
            self.forbiddenFields.remove((self.letterToIndex[i[0]], i[1]))
            self.setStockBoardFieldStyle(self.letterToIndex[i[0]], i[1])
            for j in locateSurroundingFields(self.letterToIndex[i[0]], i[1], mode):
                if j in self.forbiddenFields:
                    self.forbiddenFields.remove((j[0], j[1]))

        # After freeing previously taken fields activate them
        self.enableBoardFields()
        # Disable back to not back out of empty stack
        if self.shipMg.getShipStackLen() == 0:
            self.backButton.setEnabled(False)

        self.updateALlShipsPlacedState()


    # Revert all changes, get back to start state
    def resetSelectionState(self):
        self.moveHistory = []
        self.forbiddenFields = []
        self.enableBoardFields()
        self.shipMg.shipsSelectionRestart()
        for i in range(11):
            self.setStockBoardBandStyle(i, 0)
            for j in range(11):
                if j != 0 and i != 0:
                    self.setStockBoardFieldStyle(i, j)

        self.allShipsPlaced = False
        self.acceptButton.setText("Approve")

    # Enables buttons, makes them clickable
    def enableBoardFields(self):
        # print("gh.enableBoardFields")
        for i in range(11):
            for j in range(11):
                if i != 0 and j != 0 and ((i, j) not in self.forbiddenFields):
                    self.selectionBoard[i][j].setEnabled(True)

    # After pressing accept check with shipMg if every block for this ship option is selected
    def pullApproval(self):


        if self.allShipsPlaced:
            self.startBattle()
            return

        # print("gh.pullApproval")
        if self.shipMg.getShipAwaitingApproval() == self.shipMg.getCurrentShipOption():
            self.shipMg.shipSelectionConfirmed()
            self.enableBoardFields()
            self.shipMg.switchShipOptions(False)
            self.moveHistory = []
            # Back only available if ships present
            if self.shipMg.getShipStackLen() > 0:
                self.backButton.setEnabled(True)

            self.updateALlShipsPlacedState()


    def updateALlShipsPlacedState(self):
        all_placed = (
            self.shipMg.remainingShipFourSelections == 0 and
            self.shipMg.remainingShipThreeSelections == 0 and
            self.shipMg.remainingShipTwoSelections == 0 and
            self.shipMg.remainingShipOneSelections == 0
        )

        self.allShipsPlaced = all_placed

        if self.allShipsPlaced:
            self.acceptButton.setText("Start battle")

            self.shipMg.switchShipOptions(True)





    # Calculate the edge fields of the ship
    def calculateYoungestOldest(self):
        comp = []
        [comp.append(i) for i in self.moveHistory]
        comp = sorted(comp)
        return (comp[0], comp[-1])


    def activateNextPossibleFields(self, selectionNum, baseX, baseY):
        # After selecting the first block we can go in 4 directions: up, right, down, left. Below we enable those 4
        if selectionNum == 1:
            [self.selectionBoard[x[0]][x[1]].setEnabled(True) for x
             in locateSurroundingFields(self.letterToIndex[baseX], baseY, "leftRight") if (x[0], x[1]) not in
             self.forbiddenFields and (x[0], x[1]) not in self.moveHistory]
        # From the 2nd move onwards we can only go in 2 directions: to the right/left of the edge blocks we enable them
        else:
            firstBlock, lastBlock = self.calculateYoungestOldest()

            for x in locateSurroundingFields(self.letterToIndex[firstBlock[0]], firstBlock[1], "leftRight"):
                if x not in self.forbiddenFields and x not in self.moveHistory:
                    self.selectionBoard[x[0]][x[1]].setEnabled(True)

            for x in locateSurroundingFields(self.letterToIndex[lastBlock[0]], lastBlock[1], "leftRight"):
                if x not in self.forbiddenFields and x not in self.moveHistory:
                    self.selectionBoard[x[0]][x[1]].setEnabled(True)

    def updateNextMoveOptions(self, baseX, baseY):
        # print("gh.updateNextMoveOptions")
        if self.shipMg.getCurrentShipOption() != 1:
            # For larger ship options a slick idea is to block the ship field itself and the neighbouring diagonals
            # in such way by placing 2 ship fields next to each other we are left with 2 not forbidden fields with no
            # overlaps, those are addressed later
            self.forbiddenFields.append((self.letterToIndex[baseX], baseY))
            [self.forbiddenFields.append((x[0], x[1])) for x
             in locateSurroundingFields(self.letterToIndex[baseX], baseY, "diagonals")]

            # Enabling fields that user can click next
            if self.shipMg.getRemainingShipSelections() != 0:
                self.activateNextPossibleFields((self.shipMg.getCurrentShipOption() -
                                                 self.shipMg.getRemainingShipSelections()), baseX, baseY
                                                )
            else:
                # Here we address the 2 unblocked fields mentioned above, for youngest and oldest we pull their
                # neighbours (up, right, down, left) and check if they are forbidden if not fobidd
                # We allow ourselves such solution as out arrays will never exceed 100 elements so it is efficient
                # memory and time wise
                youngest, oldest = self.calculateYoungestOldest()
                for y in locateSurroundingFields(self.letterToIndex[oldest[0]], oldest[1], "leftRight"):
                   if y not in self.forbiddenFields:
                        self.forbiddenFields.append(y)
                for z in locateSurroundingFields(self.letterToIndex[youngest[0]], youngest[1], "leftRight"):
                  if z not in self.forbiddenFields:
                        self.forbiddenFields.append(z)
        else:
            # After selecting a block for ship option 1 so 1 block we instantly forbid the ship block and surroundings
            self.forbiddenFields.append((self.letterToIndex[baseX], baseY))
            [self.forbiddenFields.append((x[0], x[1])) for x
             in locateSurroundingFields(self.letterToIndex[baseX], baseY, "surround")]

            self.shipMg.setShipAwaitingApproval(self.shipMg.getCurrentShipOption())

    def checkMarkCorrectness(self, x, y):
        if self.shipMg.getCurrentShipOption() is not None:
            if self.shipMg.getCurrentShipOption() != 1:
                pass
              # Tutaj jakoś edgecase żeby na 3 wolne pola nie pakować 4 polowego statku
            return True
        else:
            return False

    # Called after pressing board field with selected ship option
    def markShipFields(self, x, y):
        # print("gh.markShipFields")
        # Procedural calls of operations to perform to ensure proper ship selection
        if self.checkMarkCorrectness(x, y):
            self.shipMg.shipFieldSelected(x, y)
            self.customizeButtonForShip(self.letterToIndex[x], y)
            self.moveHistory.append((x, y))
            self.disableBoardFields()
            self.updateNextMoveOptions(x, y)

    # Disable every field on the board. General approach is that after every move we disable the whole board and then
    # enable only needed fields. After move completion we enable everything that is not forbidden or the board band
    def disableBoardFields(self):
        # print("gh.disableBoardFields")
        for i in range(11):
            for j in range(11):
                if self.selectionBoard[i][j].isEnabled():
                    self.selectionBoard[i][j].setEnabled(False)

    def setStockBoardBandStyle(self, x, y):
        self.selectionBoard[x][y].setEnabled(False)
        self.selectionBoard[x][y].setStyleSheet("""
                                                 QPushButton {
                                                     background-color: salmon;
                                                     color: black;
                                                     border: 3px solid black;
                                                     font-size: 20px;
                                                     padding: 0px;
                                                 }
                                             """)

    def setStockBoardFieldStyle(self, x, y):
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
                                                    background-color: gray;
                                                    border: 2px solid darkgray;
                                                }
                                            """)

    def initSelectionBoard(self):
        # print("gh.initSelectionBoard")
        az = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '']
        self.leftSide.addLayout(self.boardLayout)
        # No spaces in between buttons
        self.boardLayout.setSpacing(0)
        for i in range(len(az)):
            self.selectionBoard[i].append(QtWidgets.QPushButton(az[i]))
            self.setStockBoardBandStyle(i, 0)
            for j in range(len(nums)):
                if i == 0:
                    self.selectionBoard[i].append(QtWidgets.QPushButton(nums[j]))
                    self.setStockBoardBandStyle(i, j)

                else:
                    self.selectionBoard[i].append(QtWidgets.QPushButton())
                    if j != 0:
                        self.setStockBoardFieldStyle(i, j)
                        self.selectionBoard[i][j].clicked.connect(lambda checked, r=az[i], c=j:
                                                                  self.markShipFields(r, c))

                self.selectionBoard[i][j].setFixedSize(60, 55)
                self.boardLayout.addWidget(self.selectionBoard[i][j], i, j)


    def onTabChanged(self,index):
        if index == 0:
            self.showSetupUI()
        elif index ==1 :
            self.hideSetupUI()


    def showSetupUI(self):
        for i in range(11):
            for j in range(11):
                self.selectionBoard[i][j].show()

        self.acceptButton.show()
        self.backButton.show()
        self.resetButton.show()
        self.quitButton.show()
        self.myOnlineStatus.show()
        self.enemyOnlineStatus.show()

        for button in self.shipMg.getShipOptionButtons():
            button.show()

    def hideSetupUI(self):
        for i in range(11):
            for j in range(11):
                self.selectionBoard[i][j].hide()

        self.acceptButton.hide()
        self.backButton.hide()
        self.resetButton.hide()
        self.quitButton.hide()
        self.myOnlineStatus.hide()
        self.enemyOnlineStatus.hide()

        for button in self.shipMg.getShipOptionButtons():
            button.hide()


    def startState(self):
        # print("gh.startState")
        self.tabs.setLayout(self.layout)
        self.window.setCentralWidget(self.tabs)

        self.window.setFixedSize(1500,690)

        self.tabs.addTab(self.tab1, "Prepare for Battle")
        self.tabs.addTab(self.tab2, "Battle")

        self.tabs.setTabEnabled(1, False)

        self.initLeftSide()
        self.initRightSide()
        self.initButtonPanel()


    def startBattle(self):
        if self.battleMg == None:
            self.battleMg = battleManager.BattleManager(self)


        if not self.tabSignalsConnected:
            self.tabs.currentChanged.connect(self.onTabChanged)
            self.tabSignalsConnected = True

        self.tabs.setTabEnabled(1,True)
        self.tabs.setTabEnabled(0,False)

        self.tabs.setCurrentIndex(1)

        self.battleMg.init_game()
