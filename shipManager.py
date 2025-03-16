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
        self.currentShipOption = None
        self.remainingShipSelections = None
        self.currentShipSelectionFields = []
        self.shipAwaitingApproval = 0


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


    def getRemainingShipSelections(self):
        return self.remainingShipSelections

    def getCurrentShipOption(self):
        return self.currentShipOption

    def setShipAwaitingApproval(self, val):
        self.shipAwaitingApproval = val

    def shipSelectionConfirmed(self):
        if self.shipAwaitingApproval != 0:
            #add ship to fields in s.ships
            #del current field selections
            #shipAprroval = 0
            self.shipAwaitingApproval = 0
            #remaining -=1

            #reset current option
            self.currentShipOption = None
            # update board
            pass


    def shipSelectionRollback(self):
        pass

    def shipsSelectionRestart(self):
        pass


    # x == a,b,c,...,j
    # y == 1..10
    def shipFieldSelected(self, x, y):
        if self.currentShipOption is not None:

            if (x, y) not in self.currentShipSelectionFields:
                self.currentShipSelectionFields.append((x, y))

            if self.currentShipOption == 1:
                self.remainingShipSelections -= 1

            elif self.currentShipOption == 2:
                self.remainingShipSelections -= 1


            elif self.currentShipOption == 3:
                self.remainingShipSelections -= 1

            elif self.currentShipOption == 4:
                self.remainingShipSelections -= 1

            else:
                exit(69)
        else:
            pass



    def getShipOptionButtons(self):
        return [self.shipFourOption, self.shipThreeOption, self.shipTwoOption, self.shipOneOption]

    def shipOptionSelected(self, uuid):
        self.shipFourOption = uuid
        self.currentShipOption = uuid
        self.remainingShipSelections = uuid

        #self.disableButtons()

