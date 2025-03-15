from PySide6 import QtWidgets


class Ship:
    def __init__(self, size, fields):
        self.size = size
        self.fields = fields

    def decreaseSize(self):
        self.size -= 1
        # ship is hit, take size -= 1 and change according field, when size 0 call
        # __del__ change color of tiles on board

    def __del__(self):
            pass


class ShipManager:

    def __init__(self):
        self.ships = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': []}
        self.currentShipOption = 0

        self.remainingShipOneSelections = 4
        self.remainingShipTwoSelections = 3
        self.remainingShipThreeSelections = 2
        self.remainingShipFourSelections = 1

        self.guiShipSelector = QtWidgets.QButtonGroup()
        self.shipFourOption = QtWidgets.QRadioButton(f'Four-masted ship, '
                                                     f'{self.remainingShipFourSelections} remaining')
        self.shipThreeOption = QtWidgets.QRadioButton(f'Three-masted ship, '
                                                      f'{self.remainingShipThreeSelections} remaining')
        self.shipTwoOption = QtWidgets.QRadioButton(f'Two-masted ship, {self.remainingShipTwoSelections} remaining')
        self.shipOneOption = QtWidgets.QRadioButton(f'Single-masted ship, {self.remainingShipOneSelections} remaining')

        self.guiShipSelector.addButton(self.shipFourOption, 4)
        self.guiShipSelector.addButton(self.shipThreeOption, 3)
        self.guiShipSelector.addButton(self.shipTwoOption, 2)
        self.guiShipSelector.addButton(self.shipOneOption, 1)

        self.guiShipSelector.idClicked.connect(self.shipOptionSelected)


    def shipSelectionConfirmed(self):
        print("asdasdasd")
        pass

    def shipSelectionRollback(self):
        pass

    def shipsSelectionRestart(self):
        pass


    def collectFields(self, remainingSelections, x, y):
        pass

    # x == a,b,c,...,j
    # y == 1..10
    def shipFieldSelected(self, x, y):
        if self.currentShipOption == 1:
            self.collectFields(0, x, y)
        elif self.currentShipOption == 2:
            self.collectFields(1, x, y)
        elif self.currentShipOption == 3:
            self.collectFields(2, x, y)
        elif self.currentShipOption == 4:
            self.collectFields(3, x, y)
        else:
            exit(69)

    def getShipOptionButtons(self):
        return [self.shipFourOption, self.shipThreeOption, self.shipTwoOption, self.shipOneOption]

    def shipOptionSelected(self, uuid):
        self.currentShipOption = uuid
        #self.disableButtons()

