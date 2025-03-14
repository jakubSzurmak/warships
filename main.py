import sys

import gameHolder


if __name__ == '__main__':
    running = True
    ships_ready = False
    game_over = False

    myGame = gameHolder.GameHolder()
    myGame.getWindow().resize(1280, 920)
    myGame.getWindow().show()


    while running:
        myGame.startState()
        sys.exit(myGame.getApp().exec())


