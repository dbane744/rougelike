import os

import shelve

"""
This module encapsulates saving and loading of the game.
This includes the player's index in the entity list, entity list, the game map, the message log and the current game state.
"""

def save_game(player, entities, game_map, message_log, game_state):
    """
    Saves the game to a .dat file using the shelve module which is built in to the python standard library.
    The shelve module allows complex objects to be seriazlied in similar fashion to the pickle module but is different
    because it allows different serialized objects to be associated with a key (a dictionary of serizalized objects).
    :param player: The player entity.
    :param entities: The entities list.
    :param game_map: The game map objects.
    :param message_log: The message log objects.
    :param game_state: The current game state.
    :return:
    """

    # 'n' always creates a new file for reading and writing.
    with shelve.open("savegame", "n") as data_file:
        data_file["player_index"] = entities.index(player)
        data_file["entities"] = entities
        data_file["game_map"] = game_map
        data_file["message_log"] = message_log
        data_file["game_state"] = game_state

def load_game():
    """
    Attempts to load a previous save file(shelve dictionary) from a .dat file.
    :return: Returns each variable separately - returns the same variables as get_game_variables() in initialise_new_game.py.
    """
    # If the .dat file does not exist an exception will be raised.
    if not os.path.isfile("savegame.dat"):
        raise FileNotFoundError

    # 'r' is opening the shelve file just for reading.
    with shelve.open("savegame", "r") as data_file:
        player_index = data_file["player_index"]
        entities = data_file["entities"]
        game_map = data_file["game_map"]
        message_log = data_file["message_log"]
        game_state = data_file["game_state"]

    # Grabs the player entity from the entities list using the newly obtained player_index.
    player = entities[player_index]

    return player, entities, game_map, message_log, game_state