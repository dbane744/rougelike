import libtcodpy as libtcod
from fov_functions import initialise_fov
from fov_functions import recompute_fov
from map_objects.game_map import GameMap
from entity import Entity
from input_handlers import handle_keys
from render_functions import render_all, clear_all


def main():
    # Screen size.
    screen_width = 80
    screen_height = 50

    # Map size.
    map_width = 80
    map_height = 45

    # Room size/number limitations.
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # FOV (Field of view) limitations.
    fov_algorithm = 0 # Uses the default algorithm libtcod uses.
    fov_light_walls = True # Whether to 'light up' the walls we see.
    fov_radius = 10 # Tells us how far the player can see.

    colors = {
        "dark_wall": libtcod.Color(64, 64, 64),
        "dark_ground": libtcod.Color(68, 36, 52),
        "light_wall": libtcod.Color(133, 149, 161),
        "light_ground": libtcod.Color(133, 76, 48)
    }

    # Creates the player object.
    player = Entity(int(screen_width/2), int(screen_height/2), "@", libtcod.white)
    # Creates an npc object.
    npc = Entity(int(screen_width/2 - 5), int(screen_height/2), "@", libtcod.yellow)
    # Creates a list of all entities.
    entities = [npc, player]

    # Sets the font.
    libtcod.console_set_custom_font("arial10x10.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    # Sets up the root console.
    libtcod.console_init_root(screen_width, screen_height, "My First Rougelike", False)
    # Creates the main off-screen console.
    con = libtcod.console_new(screen_width, screen_height)
    # Creates the game map and calls its make_map function.
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    # Whether to recompute the fov (Would be false if the player didn't move that turn).
    # True by default because we have to compute it when the game starts.
    fov_recompute = True
    # Computes the fov_map
    fov_map = initialise_fov(game_map)

    # Stores the keyboard and mouse input. This will be updated throughout the game loop.
    key = libtcod.Key()
    mouse = libtcod.Mouse()

############################################################
                        # GAME LOOP
############################################################
    while not libtcod.console_is_window_closed():
        # Captures input - will update key and mouse variables with the input.
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # Recomputes the FOV if necessary.
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        # Draws all entities to the off-screen console and blits the console to the root.
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)

        # Don't recompute the fov/repaint the tiles until after the player moves.
        fov_recompute = False

        # Flushes/draws the screen.
        libtcod.console_flush()

        # Erases all characters on the off-screen console.
        clear_all(con, entities)

        ### REACTS TO KEY PRESSES ###
        action = handle_keys(key)

        # Stores the value/s returned from dictionary key.
        move = action.get("move")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")

        # Performs an action if one of the above variables is not empty.
        if move:
            # 'move' will be storing two integers.
            dx, dy = move
            # Alters the player's position by dx/dy amount.
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)
                # Recomputes the FOV map now the player has moved.
                fov_recompute = True

        # Exits the loop which exits the game.
        if exit:
            return True

        # Toggles fullscreen.
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

############################################################


# Runs the main method if engine.py is ran.
if __name__ == "__main__":
    main()