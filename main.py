import sys

import gameHolder


if __name__ == '__main__':
    running = True
    ships_ready = False
    game_over = False

    myGame = gameHolder.GameHolder()
    myGame.getWindow().resize(1280, 720)
    myGame.getWindow().show()


    while running:
        if not ships_ready:
            myGame.startState()
            ships_ready =True
        elif ships_ready:
            pass
        elif game_over:
            pass

        sys.exit(myGame.getApp().exec())


