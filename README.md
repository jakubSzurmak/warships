# Warships

This repository implements a basic version of the classic pen-and-paper *Warships* game in **Python 3** using **PySide6**. 
The game supports multiplayer gameplay using the **UDP protocol**, although it is currently configured to run on a single machine.

---

## Project Structure

The source code is divided into five main files:

### `main.py`
This is the entry point of the application. It initializes the PyQt window and starts the game interface.
Starting configuration requires to specify the name of the client as the argv[1] so the running sript would be main.py client1 and main.py client2 accordingly.
Network addresses used are 127.0.0.1 ports 5000 and 5001 for client1 and client 2 respectively.

### `gameHolder.py`
Once the application starts, the `gameHolder` class is invoked. This component allows players to place their ships on the game field. It provides functionality to:

- Place ships on the board.
- Revert the placement of a ship.
- Reset all ship placements to the initial empty state.
- Exit the game.

<img width="800" alt="warships_initial.png" src="https://github.com/jakubSzurmak/warships/blob/f39619160cc38adbd5ece893afb0cc5256f5b4e9/blobs/warships_initial.png">

### `ShipManager.py`
After ship placement is complete, the user can begin the battle. The `ShipManager` class is responsible for:

- Managing placed ships.
- Handling user options related to ship configuration before the battle starts.

<img width="800" alt="warships_battle_start.png" src="https://github.com/jakubSzurmak/warships/blob/687b715e023ef208f0cad93c944483e2eaa52111/blobs/warships_battle_start.png">

### `BattleManager.py`
When the player initiates the battle, the `BattleManager` class is instantiated. It:

- Maintains the state of the battle.
- Manages network connectivity.
- Utilizes basic concurrency principles via the nested `start_listener_udp` method.

<img width="800" alt="warships_selected_ships.png" src="https://github.com/jakubSzurmak/warships/blob/687b715e023ef208f0cad93c944483e2eaa52111/blobs/warships_selected_ships.png">

### `GameState.py`
The `GameState` class works closely with `BattleManager`. It:

- Calculates coordinate logic.
- Validates the legality and results of each player move.

<img width="950" alt="warships_game_over_in_1.png" src="https://github.com/jakubSzurmak/warships/blob/687b715e023ef208f0cad93c944483e2eaa52111/blobs/warships_game_over_in_1.png">

---

## Libraries Used

- **PySide6**: For GUI creation.
- **socket** (built-in): For UDP-based network communication.
- **threading** (built-in): For managing concurrency during multiplayer sessions.


## Members Contribution

- **Jakub Szurmak**: Ships setup stage and all of the functionalities there, styling of the buttons and theme, network communication between the clients, collaborating on the implementation of battle logic and edge cases (gameHolder.py, shipManager.py, main.py)
- **Kacper Sochacki**: Implementation of the battle phase and most of the functionalities in the BattleManager.py, thread locking, detecting enemy conncetion state changes, shooting and receiving shots logic (battleManager.py, gameState.py)
