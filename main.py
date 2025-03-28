import gameHolder
import sys


# Application start point
if __name__ == '__main__':

    # Initialization of the gameHolder class which holds data about GUI and sends messages to other holders
    myGame = gameHolder.GameHolder()

    # Setting starting size of GUI window and displaying it
    myGame.getWindow().resize(1280, 920)
    myGame.getWindow().show()

    # Pushing game initialization from here action and checks start
    myGame.startState()
    sys.exit(myGame.getApp().exec())

