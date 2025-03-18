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
        self.currentShipOption = None
        self.remainingShipSelections = None
        self.shipFields = []
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


    def appendShipField(self, x, y):
        pass

    def getRemainingShipSelections(self):
        return self.remainingShipSelections

    def getCurrentShipOption(self):
        return self.currentShipOption

    def setShipAwaitingApproval(self, val):
        self.shipAwaitingApproval = val

    def getShipAwaitingApproval(self):
        return self.shipAwaitingApproval


    def updateShipOptionLabel(self, opt):
        print("mg.updateLabels")
        if opt == 1:
            self.remainingShipOneSelections -= 1
            self.shipOneOption.setText(f'Single-masted ship, {self.remainingShipOneSelections} remaining')
            if self.remainingShipOneSelections == 0:
                self.shipOneOption.setDisabled(True)
        elif opt == 2:
            self.remainingShipTwoSelections -= 1
            self.shipTwoOption.setText(f'Two-masted ship, {self.remainingShipTwoSelections} remaining')
            if self.remainingShipTwoSelections == 0:
                self.shipTwoOption.setDisabled(True)
        elif opt == 3:
            self.remainingShipThreeSelections -= 1
            self.shipThreeOption.setText(f'Three-masted ship, '
                                                      f'{self.remainingShipThreeSelections} remaining')
            if self.remainingShipThreeSelections == 0:
                self.shipThreeOption.setDisabled(True)
        elif opt == 4:
            self.remainingShipFourSelections -= 1
            self.shipFourOption.setText(f'Four-masted ship, '
                                                     f'{self.remainingShipFourSelections} remaining')
            self.shipFourOption.setDisabled(True)
        else:
            exit(69)



    def switchShipOptions(self, bit):
        print("mg.switchOptions")
        if self.remainingShipOneSelections > 0:
            self.shipOneOption.setDisabled(bit)
        if self.remainingShipTwoSelections > 0:
            self.shipTwoOption.setDisabled(bit)
        if self.remainingShipThreeSelections > 0:
            self.shipThreeOption.setDisabled(bit)
        if self.remainingShipFourSelections > 0:
            self.shipFourOption.setDisabled(bit)

    def uncheckShipOptions(self):
        print("mg.uncheckShipOptions")
        self.guiShipSelector.setExclusive(False)
        for button in self.guiShipSelector.buttons():
            button.setChecked(False)
        self.guiShipSelector.setExclusive(True)


    def shipSelectionConfirmed(self):
        print("mg.selectionConfirmed")
        if self.shipAwaitingApproval != 0:
            if self.remainingShipSelections > 0:
                self.remainingShipSelections -= 1

            self.shipAwaitingApproval = 0

            if self.remainingShipSelections == 0:
                self.updateShipOptionLabel(self.currentShipOption)

            #reset current option
            self.currentShipOption = None
            self.uncheckShipOptions()
            pass


    def shipSelectionRollback(self):
        pass

    def shipsSelectionRestart(self):
        pass


    # x == a,b,c,...,j
    # y == 1..10
    def shipFieldSelected(self, x, y):
        print("mg.shipFieldSelected")
        self.switchShipOptions(True)
        if self.remainingShipSelections == 0:
            self.shipAwaitingApproval = self.currentShipOption
            self.appendShipField(x, y)




    def getShipOptionButtons(self):
        print("mg.getShipOptionButtons")
        return [self.shipFourOption, self.shipThreeOption, self.shipTwoOption, self.shipOneOption]

    def shipOptionSelected(self, uuid):
        print("mg.shipOptionSelected")
        self.currentShipOption = uuid
        self.remainingShipSelections = uuid

        #self.disableButtons()

