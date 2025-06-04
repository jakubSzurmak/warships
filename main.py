import gameHolder
import sys


# Application start point
if __name__ == '__main__':

    # Initialization of the gameHolder class which holds data about GUI and sends messages to other holders

    if sys.argv[1] == "client1":
        myGame = gameHolder.GameHolder("client1")
    elif sys.argv[1] == "client2":
        myGame = gameHolder.GameHolder("client2")
    else:
        exit(69)

    # Setting starting size of GUI window and displaying it
    myGame.getWindow().show()

    # Pushing game initialization, from here action and checks start
    myGame.startState()
    sys.exit(myGame.getApp().exec())




