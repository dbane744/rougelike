import libtcodpy as libtcod

from game_states import GameStates


def handle_keys(key, game_state):
    """
    Deternmines which handle keys method should be used(and result returned) depending on current game state.
    :param key: 
    :param gamestate: 
    :return: 
    """
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    # Kills 2 birds with one stone - all inventory game states.
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)

    # If none of the above game states:
    return {}

def handle_player_turn_keys(key):
    # Grabs the character of the keypress if there is one.
    key_char = chr(key.c)

    # Movement keys
    if key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
        return {"move": (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
        return {"move": (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
        return {"move": (-1, 0 )}
    elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
        return {"move": (1, 0)}
    elif key.vk == libtcod.KEY_KP7:
        return {"move": (-1, -1)}
    elif key.vk == libtcod.KEY_KP9:
        return {"move": (1, -1)}
    elif key.vk == libtcod.KEY_KP1:
        return {"move": (-1, 1)}
    elif key.vk == libtcod.KEY_KP3:
        return {"move": (1, 1)}
    # Character keys.
    if key_char == "g":
        return {"pickup": True}
    elif key_char == "i":
        return {"show_inventory": True}
    elif key_char == "d":
        return {"drop_inventory": True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: Toggle full screen
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game.
        return {"exit": True}

    # No key was pressed
    return {}

def handle_player_dead_keys(key):
    key_chr = chr(key.c)

    if key_chr == "i":
        return {"show inventory": True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Toggle full screen.
        return {"fullscreen": True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu.
        return {"exit": True}

    return {}

def handle_inventory_keys(key):
    """
    When the game state is on the inventory.
    :param The keyboard key that was pressed.
    :return: Results of the key press.
    """
    # When using ord() - a = 0, b = 1, c = 2 etc.
    # Generates a unique index for each item that corresponds to the inventory item list.
    index = key.c - ord("a")

    # Returns the index of the selected item.
    if index >= 0:
        return {"inventory_index": index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Toggle full screen.
        return {"fullscreen": True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu.
        return {"exit": True}

    return {}