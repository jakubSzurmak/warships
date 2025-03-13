from PySide6 import QtWidgets


class GameHolder:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.window = QtWidgets.QMainWindow()
        self.tabs = QtWidgets.QTabWidget()

        self.layout = QtWidgets.QGridLayout()

        self.leftSide = QtWidgets.QVBoxLayout()
        self.rightSide = QtWidgets.QVBoxLayout()
        self.buttonPanel = QtWidgets.QHBoxLayout()

        self.boardLayout = QtWidgets.QGridLayout()

        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()

        self.myOnlineStatus = QtWidgets.QTextEdit()
        self.myOnlineStatus.setReadOnly(True)
        self.myOnlineStatus.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

        self.enemyOnlineStatus = QtWidgets.QTextEdit()
        self.enemyOnlineStatus.setReadOnly(True)
        self.enemyOnlineStatus.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

        self.selectionBoard = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
        }

    def getWindow(self):
        return self.window

    def getTabs(self):
        return self.tabs

    def getApp(self):
        return self.app

    def initRightSide(self):
        self.rightSide.addWidget(self.myOnlineStatus)

    def initButtonPanel(self):
        pass

    def initSelectionBoard(self):
        for i in range(10):
            for j in range(10):
                self.selectionBoard[i].append(QtWidgets.QPushButton(f"{i}, {j}").setFixedSize(40, 30))
                self.boardLayout.addWidget(QtWidgets.QPushButton(), i, j)

    def printSelectionBoard(self):
        pass

    def startState(self):
        self.boardLayout.setSpacing(0)

        self.layout.addLayout(self.leftSide, 0, 0)
        self.layout.addLayout(self.rightSide, 0, 1)
        self.layout.addLayout(self.buttonPanel, 1, 0)

        self.leftSide.addLayout(self.boardLayout, 0)

        self.tabs.setLayout(self.layout)
        self.window.setCentralWidget(self.tabs)

        self.tabs.addTab(self.tab1, "Prepare for Battle")
        self.tabs.addTab(self.tab2, "Battle")

        self.tabs.setTabEnabled(1, False)

        self.initSelectionBoard()
        self.initRightSide()

        ships_ready = False
        while not ships_ready:
            ships_ready = True
        return 1

    def gameState(self):
        pass
