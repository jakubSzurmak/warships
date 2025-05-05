from PySide6 import QtWidgets, QtCore
import gameState

class BattleManager:

    def __init__(self, game_holder):
        self.game_holder = game_holder
        self.game_state = gameState.GameState()

        self.setup_battle_ui()

        self.waiting_for_opponent = False

        self.status_label = QtWidgets.QLabel("Waiting for battle to begin...")
        self.turn_label = QtWidgets.QLabel("Your turn")

        # Dict for tracking enemy board buttons
        self.enemy_board = {
            0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []
        }

        # Dict for tracking own board display (no buttons, just for display)
        self.own_board_display = {
            0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []
        }

        self.own_ships_remaining = QtWidgets.QLabel("Your ships: 10/10")
        self.enemy_ships_remaining = QtWidgets.QLabel("Enemy ships: 10/10")

        self.network_status = QtWidgets.QLabel("Connected")

        self.shot_history = QtWidgets.QTextEdit()
        self.shot_history.setReadOnly(True)


    def setup_battle_ui(self):

        battle_tab = self.game_holder.tab2

        battle_layout = QtWidgets.QGridLayout(battle_tab)

        self.enemy_board_layout = QtWidgets.QGridLayout()
        self.own_board_layout = QtWidgets.QGridLayout()

        self.status_layout = QtWidgets.QVBoxLayout()

        # Add the layouts to the main battle layout
        battle_layout.addLayout(self.enemy_board_layout, 0, 0)
        battle_layout.addLayout(self.status_layout, 0, 1)
        battle_layout.addLayout(self.own_board_layout, 0, 2)

        self.setup_status_panel()

        self.setup_enemy_board()

        self.setup_own_board_display()

    def setup_status_panel(self):

        # Add the status label to the status layout
        self.status_layout.addWidget(self.status_label)
        self.status_layout.addWidget(self.turn_label)

        # Add ship status
        self.status_layout.addWidget(QtWidgets.QLabel("Ship Status:"))
        self.status_layout.addWidget(self.own_ships_remaining)
        self.status_layout.addWidget(self.enemy_ships_remaining)

        # Add network status
        self.status_layout.addWidget(QtWidgets.QLabel("Network:"))
        self.status_layout.addWidget(self.network_status)

        # Add shot history
        self.status_layout.addWidget(QtWidgets.QLabel("Shot History:"))
        self.status_layout.addWidget(self.shot_history)

        # Add spacer to push everything to the top
        self.status_layout.addStretch()

    def setup_enemy_board(self):

        # Add column labels (A-J)
        az = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '']

        self.enemy_board_layout.setSpacing(0)

        # Create the board buttons
        for i in range(len(az)):
            self.enemy_board[i].append(QtWidgets.QPushButton(az[i]))
            self.set_board_band_style(self.enemy_board[i][0])

            for j in range(len(nums)):
                if i == 0:
                    self.enemy_board[i].append(QtWidgets.QPushButton(nums[j]))
                    self.set_board_band_style(self.enemy_board[i][j])
                else:
                    self.enemy_board[i].append(QtWidgets.QPushButton())
                    if j != 0:
                        self.set_board_field_style(self.enemy_board[i][j])
                        # Connect button to fire shot method
                        self.enemy_board[i][j].clicked.connect(
                            lambda checked, r=az[i], c=j: self.fire_shot(r, c)
                        )

                self.enemy_board[i][j].setFixedSize(60, 55)
                self.enemy_board_layout.addWidget(self.enemy_board[i][j], i, j)

    def setup_own_board_display(self):

        # Add column labels (A-J)
        az = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '']


        self.own_board_layout.setSpacing(0)

        # Create the board display
        for i in range(len(az)):
            self.own_board_display[i].append(QtWidgets.QLabel(az[i]))
            self.set_own_board_band_style(self.own_board_display[i][0])

            for j in range(len(nums)):
                if i == 0:
                    self.own_board_display[i].append(QtWidgets.QLabel(nums[j]))
                    self.set_own_board_band_style(self.own_board_display[i][j])
                else:
                    self.own_board_display[i].append(QtWidgets.QLabel())
                    if j != 0:
                        self.set_own_board_field_style(self.own_board_display[i][j])

                self.own_board_display[i][j].setFixedSize(60, 55)
                self.own_board_display[i][j].setAlignment(QtCore.Qt.AlignCenter)
                self.own_board_layout.addWidget(self.own_board_display[i][j], i, j)

    def set_board_band_style(self, button):
        button.setEnabled(False)
        button.setStyleSheet("""
            QPushButton {
                background-color: salmon;
                color: black;
                border: 3px solid black;
                font-size: 20px;
                padding: 0px;
            }
        """)

    def set_board_field_style(self, button):
        button.setStyleSheet("""
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

    def set_own_board_band_style(self, label):
        label.setStyleSheet("""
            QLabel {
                background-color: salmon;
                color: black;
                border: 3px solid black;
                font-size: 20px;
                padding: 0px;
            }
        """)

    def set_own_board_field_style(self, label):
        label.setStyleSheet("""
            QLabel {
                background-color: lightblue;
                border: 2px solid black;
                font-size: 16px;
                padding: 0px;
            }
        """)

    def set_hit_style(self, widget):
        widget.setStyleSheet("""
            background-color: red;
            border: 2px solid black;
            font-size: 16px;
            padding: 0px;
        """)

    def set_miss_style(self, widget):
        widget.setStyleSheet("""
            background-color: white;
            border: 2px solid black;
            font-size: 16px;
            padding: 0px;
        """)

    def set_ship_style(self, widget):
        widget.setStyleSheet("""
            background-color: green;
            border: 2px solid black;
            font-size: 16px;
            padding: 0px;
        """)

    def init_game(self):

        # Import ships from the ship manager
        self.game_state.import_ships_from_shipmanager(self.game_holder.shipMg)

        self.game_state.start_game()

        self.update_battle_ui()

        # Set status message
        self.status_label.setText("Game started!")

        # Enable the battle tab
        self.game_holder.tabs.setTabEnabled(1, True)

        # Switch to the battle tab
        self.game_holder.tabs.setCurrentIndex(1)

        # Update the shot history
        self.shot_history.append("Game started. Your turn to fire!")

    def fire_shot(self, letter, number):

        # Check if it's our turn
        if self.waiting_for_opponent:
            self.status_label.setText("Please wait for opponent's move")
            return

        # Convert the coordinates
        x = self.game_state.letter_to_index(letter)
        y = number

        # Process the shot
        result, ship_id = self.game_state.process_shot(self.game_state.player_role, x, y)

        # Update the UI based on the result
        if result == self.game_state.MISS:
            self.enemy_board[x][y].setEnabled(False)
            self.set_miss_style(self.enemy_board[x][y])
            self.shot_history.append(f"You fired at {letter}{number}: Miss")

        elif result == self.game_state.HIT:
            self.enemy_board[x][y].setEnabled(False)
            self.set_hit_style(self.enemy_board[x][y])
            self.shot_history.append(f"You fired at {letter}{number}: Hit!")

        elif result == self.game_state.SUNK:
            self.enemy_board[x][y].setEnabled(False)
            self.set_hit_style(self.enemy_board[x][y])
            self.shot_history.append(f"You fired at {letter}{number}: Ship sunk!")

            if self.game_state.is_game_over():
                self.game_over(self.game_state.get_winner())
                return

        elif result == self.game_state.INVALID:
            self.status_label.setText("Invalid shot. Try again.")
            return

        self.update_battle_ui()

        # Switch turns
        self.waiting_for_opponent = True
        self.status_label.setText("Waiting for opponent's move...")
        self.turn_label.setText("Enemy's turn")

        # Implement sending the shot to server here <---
        # Simulation for testing remove when server is implemented
        QtCore.QTimer.singleShot(2000, self.simulate_opponent_move)

    def simulate_opponent_move(self):

        # Replace by receiving a move from the server when it is implemented

        import random

        # Get our player role
        our_role = self.game_state.player_role
        opponent_role = 2 if our_role == 1 else 1


        while True:
            x = random.randint(1, 10)
            y = random.randint(1, 10)

            # Process the shot
            result, ship_id = self.game_state.process_shot(opponent_role, x, y)

            if result != self.game_state.INVALID:
                break

        # Convert the coordinates for display
        letter = self.game_state.index_to_letter(x)


        if result == self.game_state.MISS:
            self.set_miss_style(self.own_board_display[x][y])
            self.shot_history.append(f"Enemy fired at {letter}{y}: Miss")

        elif result == self.game_state.HIT:
            self.set_hit_style(self.own_board_display[x][y])
            self.shot_history.append(f"Enemy fired at {letter}{y}: Hit!")

        elif result == self.game_state.SUNK:
            self.set_hit_style(self.own_board_display[x][y])
            self.shot_history.append(f"Enemy fired at {letter}{y}: Ship sunk!")


            if self.game_state.is_game_over():
                self.game_over(self.game_state.get_winner())
                return


        self.update_battle_ui()


        self.waiting_for_opponent = False
        self.status_label.setText("Your turn to fire!")
        self.turn_label.setText("Your turn")

    def update_battle_ui(self):

        # Get the board view for our player
        board_view = self.game_state.get_board_for_player(self.game_state.player_role)

        # Update the own board display
        own_board = board_view['own_board']
        for i in range(1, 11):
            for j in range(1, 11):
                if own_board[i][j] == 1:  # Ship
                    self.set_ship_style(self.own_board_display[i][j])
                elif own_board[i][j] == 2:  # Hit
                    self.set_hit_style(self.own_board_display[i][j])
                elif own_board[i][j] == 3:  # Miss
                    self.set_miss_style(self.own_board_display[i][j])

        # Update ship counts
        own_ships = self.game_state.get_remaining_ships(self.game_state.player_role)
        enemy_ships = self.game_state.get_remaining_ships(2 if self.game_state.player_role == 1 else 1)

        own_intact = sum(1 for ship in own_ships.values() if not ship['sunk'])
        enemy_intact = sum(1 for ship in enemy_ships.values() if not ship['sunk'])

        self.own_ships_remaining.setText(f"Your ships: {own_intact}/10")
        self.enemy_ships_remaining.setText(f"Enemy ships: {enemy_intact}/10")

    def game_over(self, winner):

        # Display game over message
        if winner == self.game_state.player_role:
            self.status_label.setText("Game over! You win!")
            self.shot_history.append("Game over! You win!")
        else:
            self.status_label.setText("Game over! You lose!")
            self.shot_history.append("Game over! You lose!")

        for i in range(1, 11):
            for j in range(1, 11):
                self.enemy_board[i][j].setEnabled(False)
