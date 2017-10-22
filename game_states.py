from enum import Enum, auto


class GameStates(Enum):
    # Automatically assigns an increasing value to each game state.
    # (Equivalent to 1...2...3...4 e.g ENEMY_TURN = 2)
    PLAYERS_TURN = auto()
    ENEMY_TURN = auto()
    PLAYER_DEAD = auto()
    SHOW_INVENTORY = auto()
    DROP_INVENTORY = auto()
    TARGETING = auto() # A state where the player must select a tile to continue (i.e. when casting spells)
    LEVEL_UP = auto()
    CHARACTER_SCREEN = 8