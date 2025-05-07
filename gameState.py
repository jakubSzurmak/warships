class GameState:
    def __init__(self):

        self.MISS = "MISS"
        self.HIT = "HIT"
        self.SUNK = "SUNK"
        self.INVALID = "INVALID"

        self.player1_board = [[0 for _ in range(11)] for _ in range(11)]
        self.player2_board = [[0 for _ in range(11)] for _ in range(11)]

        self.player1_ships = {}
        self.player2_ships = {}

        self.turn = 1

        self.game_active = False
        self.winner = None

        self.player1_shots = []
        self.player2_shots = []

        self.player_role = 1  # 1 = host/player1, 2 = client/player2

    def add_ship(self, player, ship_id, ship_size, ship_fields):
        ships = self.player1_ships if player == 1 else self.player2_ships
        board = self.player1_board if player == 1 else self.player2_board

        ships[ship_id] = {
            "size": ship_size,
            "fields": ship_fields,
            "hits": []
        }

        for x, y in ship_fields:
            board[x][y] = 1

    def process_shot(self, player, x, y):
        target_board = self.player2_board if player == 1 else self.player1_board
        target_ships = self.player2_ships if player == 1 else self.player1_ships

        if player != self.turn:
            return self.INVALID, None

        if not (1 <= x <= 10 and 1 <= y <= 10):
            return self.INVALID, None

        if target_board[x][y] == 2 or target_board[x][y] == 3:
            return self.INVALID, None

        shots = self.player1_shots if player == 1 else self.player2_shots
        shots.append((x, y))

        self.turn = 2 if player == 1 else 1

        if target_board[x][y] == 1:
            target_board[x][y] = 2

            hit_ship_id = None
            for ship_id, ship in target_ships.items():
                if (x, y) in ship["fields"]:
                    hit_ship_id = ship_id
                    ship["hits"].append((x, y))

                    if len(ship["hits"]) == ship["size"]:
                        all_sunk = all(len(s["hits"]) == s["size"] for s in target_ships.values())
                        if all_sunk:
                            self.game_active = False
                            self.winner = player

                        return self.SUNK, hit_ship_id

                    return self.HIT, hit_ship_id
        else:
            target_board[x][y] = 3
            return self.MISS, None

    def is_game_over(self):
        return not self.game_active

    def get_winner(self):
        return self.winner

    def start_game(self):
        self.game_active = True
        self.turn = 1

    def get_board_for_player(self, player, include_ships=True):

        own_board = self.player1_board if player == 1 else self.player2_board
        opponent_board = self.player2_board if player == 1 else self.player1_board

        opponent_view = [[0 for _ in range(11)] for _ in range(11)]
        for i in range(1,11):
            for j in range(1,11):
                if opponent_board[i][j] == 2:
                    opponent_view[i][j] = 2
                elif opponent_board[i][j] == 3:
                    opponent_view[i][j] = 3


        result = {
            'own_board': own_board if include_ships else opponent_view,
            'opponent_board': opponent_view
        }

        return result

    def get_remaining_ships(self, player):

        ships = self.player1_ships if player == 1 else self.player2_ships
        result = {}

        for ship_id, ship in ships.items():
            result[ship_id] = {
                'size': ship['size'],
                'hits': len(ship['hits']),
                'sunk': len(ship['hits']) == ship['size']
            }

        return result

    def letter_to_index(self, letter):
        return ord(letter.upper()) - ord('A') +1

    def index_to_letter(self, index):
        return chr(ord('A') + index -1)

    def convert_position(self, position):
        letter, number = position
        return self.letter_to_index(letter), number

    def import_ships_from_shipmanager(self, shipmanager):
        player = self.player_role
        ship_id = 0

        for i, size in enumerate(shipmanager.shipAppendixStack):
            if i == 0:
                start_idx = 0
            else:
                start_idx = sum(shipmanager.shipAppendixStack[:i])

            ship_fields = []

            for j in range(size):
                letter,number = shipmanager.shipFields[start_idx + j]
                x = self.letter_to_index(letter)
                y = number
                ship_fields.append((x, y))

            self.add_ship(player, f"ship_{ship_id}", size, ship_fields)
            ship_id += 1

        return True


    def set_player_role(self,role):
        self.player_role = role

