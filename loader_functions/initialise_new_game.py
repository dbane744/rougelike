import libtcodpy as libtcod

from components.fighter import Fighter
from components.inventory import Inventory

from entity import Entity
from game_messages import MessageLog
from game_states import GameStates
from map_objects.game_map import GameMap
from render_functions import RenderOrder

"""
This Module encapsulates functions that setup the game prior to the game loop.
"""

def get_constants():
    """
    Defines the constant values that will be used for the game.
    THESSE VALUES SHOULD NOT CHANGE - Python does not have a 'Final' keyword like Java.
    :return: A dictionary of constants - the keys and values share the same name.
    """
    # Title to appear on the window.
    window_title = "My Rougelike"

    # Screen size.
    screen_width = 80
    screen_height = 50

    # Panel parameters - holds HP bar, message log.
    # HP Bar width
    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    # Message log variables.
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    # Map size.
    map_width = 80
    map_height = 43

    # Room size/number limitations.
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # FOV (Field of view) limitations.
    fov_algorithm = 0 # Uses the default algorithm libtcod uses.
    fov_light_walls = True # Whether to 'light up' the walls we see.
    fov_radius = 10 # Tells us how far the player can see.

    # Entity limitations
    max_monsters_per_room = 3
    max_items_per_room = 3

    colors = {
        "dark_wall": libtcod.Color(64, 64, 64),
        "dark_ground": libtcod.Color(68, 36, 52),
        "light_wall": libtcod.Color(133, 149, 161),
        "light_ground": libtcod.Color(133, 76, 48)
    }

    # Puts each constant into a dictionary.
    constants = {
        "window_title": window_title,
        "screen_width": screen_width,
        "screen_height": screen_height,
        "bar_width": bar_width,
        "panel_height": panel_height,
        "panel_y": panel_y,
        "message_x": message_x,
        "message_width": message_width,
        "message_height": message_height,
        "map_width": map_width,
        "map_height": map_height,
        "room_max_size": room_max_size,
        "room_min_size": room_min_size,
        "max_rooms": max_rooms,
        "fov_algorithm": fov_algorithm,
        "fov_light_walls": fov_light_walls,
        "fov_radius": fov_radius,
        "max_monsters_per_room": max_monsters_per_room,
        "max_items_per_room": max_items_per_room,
        "colors": colors
    }

    return constants


def get_game_variables(constants):
    # Creates the player's components.
    fighter_component = Fighter(hp=30, defense=2, power=5)
    inventory_component = Inventory(26)
    # Creates the player object.
    player = Entity(0, 0, "@", libtcod.white, "Player", blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component)
    # Creates a list of initial static entities.
    entities = [player]

    # Creates the game map and calls its make_map function.
    game_map = GameMap(constants["map_width"], constants["map_height"])
    game_map.make_map(constants["max_rooms"], constants["room_min_size"], constants["room_max_size"],
                      constants["map_width"], constants["map_height"], player, entities,
                      constants["max_monsters_per_room"], constants["max_items_per_room"])

    # Creates the message log that will store text messages.
    message_log = MessageLog(constants["message_x"], constants["message_width"], constants["message_height"])

    # Stores the current game state integer value, e.g. PLAYERS_TURN is 1.
    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state