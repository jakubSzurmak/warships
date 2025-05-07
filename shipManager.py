from PySide6 import QtWidgets


# jezeli uzgadniamy że informujemy o tym ile przeciwnikowi zostało poszczególnych statkow to potrzebne
# jako kontener na pola jak nie to do usunięcia
class Ship:
    def __init__(self, size, fields):
        self.size = size
        self.fields = fields

    def __del__(self):
        pass


class ShipManager:

    def __init__(self):
        self.currentShipOption = None
        self.remainingShipSelections = None
        # for 4 ship fields number 4 to appendix for popping purposes, read stack backwards
        self.shipFields = []
        self.shipAppendixStack = []

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
        self.shipFields.append((x, y))

    def getRemainingShipSelections(self):
        return self.remainingShipSelections

    def getShipStackLen(self):
        return len(self.shipAppendixStack)

    def getCurrentShipOption(self):
        return self.currentShipOption

    def setShipAwaitingApproval(self, val):
        self.shipAwaitingApproval = val

    def getShipAwaitingApproval(self):
        return self.shipAwaitingApproval

    def updateShipOptionLabel(self, opt, i):
        # print("mg.updateLabels")
        if opt == 1:
            self.remainingShipOneSelections += i
            self.shipOneOption.setText(f'Single-masted ship, {self.remainingShipOneSelections} remaining')
            if self.remainingShipOneSelections == 0:
                self.shipOneOption.setDisabled(True)
        elif opt == 2:
            self.remainingShipTwoSelections += i
            self.shipTwoOption.setText(f'Two-masted ship, {self.remainingShipTwoSelections} remaining')
            if self.remainingShipTwoSelections == 0:
                self.shipTwoOption.setDisabled(True)
        elif opt == 3:
            self.remainingShipThreeSelections += i
            self.shipThreeOption.setText(f'Three-masted ship, '
                                         f'{self.remainingShipThreeSelections} remaining')
            if self.remainingShipThreeSelections == 0:
                self.shipThreeOption.setDisabled(True)
        elif opt == 4:
            self.remainingShipFourSelections += i
            self.shipFourOption.setText(f'Four-masted ship, '
                                        f'{self.remainingShipFourSelections} remaining')
            self.shipFourOption.setDisabled(True)
        else:
            exit(69)

    # Lekko na odwrót do możliwej poprawki tak jak litery i cyfry w gameholder, teraz switchShipOptions(True) wyłącza XD
    def switchShipOptions(self, bit):
        # print("mg.switchOptions")
        if self.remainingShipOneSelections > 0:
            self.shipOneOption.setDisabled(bit)
        if self.remainingShipTwoSelections > 0:
            self.shipTwoOption.setDisabled(bit)
        if self.remainingShipThreeSelections > 0:
            self.shipThreeOption.setDisabled(bit)
        if self.remainingShipFourSelections > 0:
            self.shipFourOption.setDisabled(bit)

    # Removing ship option selection from radio buttons
    def uncheckShipOptions(self):
        # print("mg.uncheckShipOptions")
        self.guiShipSelector.setExclusive(False)
        for button in self.guiShipSelector.buttons():
            button.setChecked(False)
        self.guiShipSelector.setExclusive(True)

    # Preparing structures for next ship
    def shipSelectionConfirmed(self):
        # print("mg.selectionConfirmed")
        if self.shipAwaitingApproval != 0:
            self.shipAwaitingApproval = 0

            if self.remainingShipSelections == 0:
                self.updateShipOptionLabel(self.currentShipOption, -1)

            self.shipAppendixStack.append(self.currentShipOption)
            self.currentShipOption = None
            self.uncheckShipOptions()

    # Returning fields of lastly selected ship
    def shipSelectionRollback(self):
        rollbackFields = []
       ## self.updateShipOptionLabel(self.shipAppendixStack[-1], 1)
        for i in self.shipFields[-self.shipAppendixStack.pop(-1):]:
            self.shipFields.remove(i)
            rollbackFields.append(i)
        return rollbackFields

    def resetOptions(self):
        self.shipOneOption.setText(f'Single-masted ship, {self.remainingShipOneSelections} remaining')
        self.shipTwoOption.setText(f'Two-masted ship, {self.remainingShipTwoSelections} remaining')
        self.shipThreeOption.setText(f'Three-masted ship, {self.remainingShipThreeSelections} remaining')
        self.shipFourOption.setText(f'Four-masted ship, {self.remainingShipFourSelections} remaining')
        self.switchShipOptions(False)

    def shipsSelectionRestart(self):
        self.currentShipOption = None
        self.remainingShipSelections = None
        self.shipFields = []
        self.shipAppendixStack = []
        self.shipAwaitingApproval = 0
        self.remainingShipOneSelections = 4
        self.remainingShipTwoSelections = 3
        self.remainingShipThreeSelections = 2
        self.remainingShipFourSelections = 1
        self.resetOptions()
        self.uncheckShipOptions()

    # x == a,b,c,...,j
    # y == 1..10
    def shipFieldSelected(self, x, y):
        # print("mg.shipFieldSelected")
        self.switchShipOptions(True)
        self.remainingShipSelections -= 1
        self.appendShipField(x, y)
        if self.remainingShipSelections == 0:
            self.setShipAwaitingApproval(self.currentShipOption)

    def getShipOptionButtons(self):
        # print("mg.getShipOptionButtons")
        return [self.shipFourOption, self.shipThreeOption, self.shipTwoOption, self.shipOneOption]

    def shipOptionSelected(self, uuid):
        # print("mg.shipOptionSelected")
        self.currentShipOption = uuid
        self.remainingShipSelections = uuid
