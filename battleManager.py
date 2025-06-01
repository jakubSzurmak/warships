import math
import gameState
import socket
import threading
from PySide6 import QtWidgets


class BattleManager:

    def __init__(self, game_holder):
        self.game_holder = game_holder
        self.game_state = gameState.GameState(game_holder.getClientId())
        self.localNetworkMsgCounter = 0

        # Initialize UI components first
        self.status_label = QtWidgets.QLabel("Waiting for battle to begin...")
        self.turn_label = QtWidgets.QLabel("Your turn")
        self.own_ships_remaining = QtWidgets.QLabel("Your ships: 10/10")
        self.enemy_ships_remaining = QtWidgets.QLabel("Enemy ships: 10/10")
        self.network_status = QtWidgets.QLabel("Connected")
        self.shot_history = QtWidgets.QTextEdit()
        self.shot_history.setReadOnly(True)

        # Add exit button in battle screen
        self.exit_button = QtWidgets.QPushButton("Exit")
        self.exit_button.setFixedWidth(100)  # Make button smaller
        self.exit_button.clicked.connect(quit)
        self.exit_button.setStyleSheet("""
            QPushButton { 
                background-color:lightgrey;
                border: 2px solid black;
                font-size: 16px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
            }
        """)

        # Dict for tracking enemy board buttons
        self.enemy_board = {
            0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []
        }

        # Dict for tracking own board display (no buttons, just for display)
        self.own_board_display = {
            0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []
        }

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self.game_holder.getClientId() == "client1":
            self.sock.bind(('127.0.0.1', 5000))
            self.target = ('127.0.0.1', 5001)
        else:
            self.sock.bind(('127.0.0.1', 5001))
            self.target = ('127.0.0.1', 5000)

        self.enemyShotX = None
        self.enemyShotY = None
        self.flag = 0

        self.opponent_ready = False
        self.battle_started = False

        self.setup_battle_ui()
        self.start_listener_udp(self.handle_message)

        if game_holder.getClientId() == "client1":
            self.waiting_for_opponent = False
        else:
            self.waiting_for_opponent = True

    def start_listener_udp(self, update_call):
        def listen():
            while True:
                try:
                    data, addr = self.sock.recvfrom(1024)
                    message = data.decode()
                    update_call(message)
                except Exception as e:
                    print(f"Network error: {e}")

        threading.Thread(target=listen, daemon=True).start()

    def handle_message(self, message):
        if message.startswith("SHOT:"):
            coords = message[5:].split(",")
            self.enemyShotX, self.enemyShotY = int(coords[0]), int(coords[1])
            self.receive_shot()
        elif message.startswith("RESULT:"):
            result = message[7:]
            self.handle_shot_result(result)
        elif message == "READY":
            self.opponent_ready = True
            self.check_battle_start()
        elif message == "START_BATTLE":
            self.battle_started = True
            self.enable_battle_controls()

    def send_message_udp(self, msg):
        if isinstance(msg, str):
            msg = msg.encode()
        self.sock.sendto(msg, self.target)

    def setup_battle_ui(self):
        battle_tab = self.game_holder.tab2

        # Create a main container layout with zero spacing
        battle_layout = QtWidgets.QGridLayout(battle_tab)

        # Create board layouts with zero spacing
        self.enemy_board_layout = QtWidgets.QGridLayout()
        self.enemy_board_layout.setSpacing(0)

        self.own_board_layout = QtWidgets.QGridLayout()
        self.own_board_layout.setSpacing(0)

        self.status_layout = QtWidgets.QVBoxLayout()

        # Create a bottom layout for the exit button
        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.exit_button)
        self.bottom_layout.addStretch()

        # Add the layouts to the main battle layout
        battle_layout.addLayout(self.enemy_board_layout, 0, 0)
        battle_layout.addLayout(self.status_layout, 0, 1)
        battle_layout.addLayout(self.own_board_layout, 0, 2)
        battle_layout.addLayout(self.bottom_layout, 1, 0, 1, 3)  # Bottom row spans all columns

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

    def setup_enemy_board(self):
        # Add column labels (A-J)
        az = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '']

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
                self.enemy_board_layout.addWidget(self.enemy_board[i][j], i, j, 1, 1)  # Add row, column span parameters

    def setup_own_board_display(self):
        # Add column labels (A-J)
        az = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '']

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
                # FIXED: Set content margins to zero on the widget
                self.own_board_layout.addWidget(self.own_board_display[i][j], i, j, 1,
                                                1)  # Add row, column span parameters

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

    def disable_battle_controls(self):
        for i in range(1, 11):
            for j in range(1, 11):
                self.enemy_board[i][j].setEnabled(False)

    def enable_battle_controls(self):
        if not self.battle_started:
            return

        for i in range(1, 11):
            for j in range(1, 11):
                if self.enemy_board[i][j].styleSheet() not in [
                    self.get_hit_stylesheet(), self.get_miss_stylesheet()
                ]:
                    self.enemy_board[i][j].setEnabled(True)

    def get_hit_stylesheet(self):
        return """
            background-color: red;
            border: 2px solid black;
            font-size: 16px;
            padding: 0px;
        """

    def get_miss_stylesheet(self):
        return """
            background-color: white;
            border: 2px solid black;
            font-size: 16px;
            padding: 0px;
        """

    def init_game(self):
        # Import ships from the ship manager
        self.game_state.import_ships_from_shipmanager(self.game_holder.shipMg)

        self.game_state.start_game()

        self.update_battle_ui()

        # Set status message
        self.status_label.setText("Waiting for opponent to be ready...")

        # Enable the battle tab
        self.game_holder.tabs.setTabEnabled(1, True)

        # Switch to the battle tab
        self.game_holder.tabs.setCurrentIndex(1)

        self.disable_battle_controls()

        self.send_message_udp("READY")

        self.check_battle_start()

    def check_battle_start(self):

        # Check if both players are ready and start battle

        if self.opponent_ready and not self.battle_started:
            self.battle_started = True
            self.send_message_udp("START_BATTLE")
            self.enable_battle_controls()

            if self.game_holder.getClientId() == "client1":
                self.status_label.setText("Battle started! Your turn to fire!")
                self.shot_history.append("Game started. Your turn to fire!")
                self.waiting_for_opponent = False
            else:
                self.status_label.setText("Battle started! Waiting for opponent's move...")
                self.shot_history.append("Game started. Please wait for opponent's move")
                self.waiting_for_opponent = True

    def fire_shot(self, letter, number):
        # check if the battle has started
        if not self.battle_started:
            self.status_label.setText("Waiting for opponent to be ready...")
            return

        # Check if it's our turn
        if self.waiting_for_opponent:
            self.status_label.setText("Please wait for opponent's move")
            return

        # Convert the coordinates
        x = self.game_state.letter_to_index(letter)
        y = number
        print("Firing shot at", x, y)
        msg = f"SHOT:{x},{y}"
        self.send_message_udp(msg)

        self.last_shot_x = x
        self.last_shot_y = y
        self.last_shot_letter = letter
        self.last_shot_number = number

        self.enemy_board[x][y].setEnabled(False)

        self.waiting_for_opponent = True
        self.status_label.setText("Waiting for opponent's response...")
        self.turn_label.setText("Enemy's turn")

    def handle_shot_result(self, result):
        x = self.last_shot_x
        y = self.last_shot_y
        letter = self.last_shot_letter
        number = self.last_shot_number

        if result == "MISS":
            self.set_miss_style(self.enemy_board[x][y])
            self.shot_history.append(f"You fired at {letter}{number}: Miss")

        elif result == "HIT":
            self.set_hit_style(self.enemy_board[x][y])
            self.shot_history.append(f"You fired at {letter}{number}: Hit!")

        elif result == "SUNK":
            self.set_hit_style(self.enemy_board[x][y])
            self.shot_history.append(f"You fired at {letter}{number}: Ship sunk!")

        elif result.startswith("WIN"):
            self.set_hit_style(self.enemy_board[x][y])
            self.shot_history.append(f"You fired at {letter}{number}: Ship sunk!")
            self.game_over(self.game_state.player_role)
            return

        self.update_battle_ui()

        # Keep our turn if hit
        if result in ["HIT", "SUNK"]:
            self.waiting_for_opponent = False
            self.status_label.setText("Hit! Your turn again!")
            self.turn_label.setText("Your turn")
        else:
            # Opponent's turn if Miss
            self.waiting_for_opponent = True
            self.status_label.setText("Waiting for opponent's move...")
            self.turn_label.setText("Enemy's turn")

    def receive_shot(self):
        # Replace by receiving a move from the server when it is implemented

        x, y = self.enemyShotX, self.enemyShotY
        our_role = self.game_state.player_role
        opponent_role = 2 if our_role == 1 else 1

        # Process the shot
        result, ship_id = self.game_state.process_shot(opponent_role, x, y)

        # Convert the coordinates for display
        letter = self.game_state.index_to_letter(x)

        if result == self.game_state.MISS:
            self.set_miss_style(self.own_board_display[x][y])
            self.shot_history.append(f"Enemy fired at {letter}{y}: Miss")
            self.send_message_udp("RESULT:MISS")

        elif result == self.game_state.HIT:
            self.set_hit_style(self.own_board_display[x][y])
            self.shot_history.append(f"Enemy fired at {letter}{y}: Hit!")
            self.send_message_udp("RESULT:HIT")

        elif result == self.game_state.SUNK:
            self.set_hit_style(self.own_board_display[x][y])
            self.shot_history.append(f"Enemy fired at {letter}{y}: Ship sunk!")

            if self.game_state.is_game_over():
                self.send_message_udp("RESULT:WIN")
                self.game_over(self.game_state.get_winner())
                return
            else:
                self.send_message_udp("RESULT:SUNK")

        self.update_battle_ui()

        if result in [self.game_state.HIT, self.game_state.SUNK]:
            self.waiting_for_opponent = True
            self.status_label.setText("Enemy hit! Waiting for their next move...")
            self.turn_label.setText("Enemy's turn")
        else:
            self.waiting_for_opponent = False
            self.status_label.setText("Enemy missed! Your turn to fire!")
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
        enemy_role = 2 if self.game_state.player_role == 1 else 1
        enemy_ships = self.game_state.get_remaining_ships(enemy_role)

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
