from enum import Enum, auto


class GameStates(Enum):
    # Automatically assigns an increasing value to each game state.
    # (Equivalent to 1...2...3...4 e.g ENEMY_TURN = 2)
    PLAYERS_TURN = auto()
    ENEMY_TURN = auto()
    PLAYER_DEAD = auto()
    SHOW_INVENTORY = auto()