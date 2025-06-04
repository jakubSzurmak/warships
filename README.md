# Warships

This repository implements a basic version of the classic pen-and-paper *Warships* game in **Python 3** using **PySide6**. 
The game supports multiplayer gameplay using the **UDP protocol**, although it is currently configured to run on a single machine.

---

## Project Structure

The source code is divided into five main files:

### `main.py`
This is the entry point of the application. It initializes the PyQt window and starts the game interface.

### `gameHolder.py`
Once the application starts, the `gameHolder` class is invoked. This component allows players to place their ships on the game field. It provides functionality to:

- Place ships on the board.
- Revert the placement of a ship.
- Reset all ship placements to the initial empty state.
- Exit the game.

### `ShipManager.py`
After ship placement is complete, the user can begin the battle. The `ShipManager` class is responsible for:

- Managing placed ships.
- Handling user options related to ship configuration before the battle starts.

### `BattleManager.py`
When the player initiates the battle, the `BattleManager` class is instantiated. It:

- Maintains the state of the battle.
- Manages network connectivity.
- Utilizes basic concurrency principles via the nested `start_listener_udp` method.

### `GameState.py`
The `GameState` class works closely with `BattleManager`. It:

- Calculates coordinate logic.
- Validates the legality and results of each player move.

---

## Libraries Used

- **PySide6**: For GUI creation.
- **socket** (built-in): For UDP-based network communication.
- **threading** (built-in): For managing concurrency during multiplayer sessions.
