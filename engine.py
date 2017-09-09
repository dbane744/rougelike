import libtcodpy as libtcod
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

    colors = {
        "dark_wall": libtcod.Color(117, 113, 97),
        "dark_ground": libtcod.Color(133, 76, 48)

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

    # Stores the keyboard and mouse input. This will be updated throughout the game loop.
    key = libtcod.Key()
    mouse = libtcod.Mouse()

############################################################
                        # GAME LOOP
############################################################
    while not libtcod.console_is_window_closed():
        # Captures input - will update key and mouse variables with the input.
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # Draws all entities to the off-screen console and blits the console to the root.
        render_all(con, entities, game_map, screen_width, screen_height, colors)

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