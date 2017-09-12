import libtcodpy as libtcod

from death_functions import kill_monster, kill_player
from components.fighter import Fighter
from fov_functions import initialise_fov, recompute_fov
from game_states import GameStates
from map_objects.game_map import GameMap
from entity import Entity, get_blocking_entities_at_location
from input_handlers import handle_keys
from render_functions import render_all, clear_all, RenderOrder


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

    # Entity limitations
    max_monsers_per_room = 3

    colors = {
        "dark_wall": libtcod.Color(64, 64, 64),
        "dark_ground": libtcod.Color(68, 36, 52),
        "light_wall": libtcod.Color(133, 149, 161),
        "light_ground": libtcod.Color(133, 76, 48)
    }


    # Creates the player's fighter component.
    fighter_component = Fighter(hp=30, defense=2, power=5)
    # Creates the player object.
    player = Entity(0, 0, "@", libtcod.white, "Player", blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component)
    # Creates a list of initial static entities.
    entities = [player]

    # Sets the font.
    libtcod.console_set_custom_font("arial10x10.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    # Sets up the root console.
    libtcod.console_init_root(screen_width, screen_height, "My First Rougelike", False)
    # Creates the main off-screen console.
    con = libtcod.console_new(screen_width, screen_height)
    # Creates the game map and calls its make_map function.
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
                      max_monsers_per_room)

    # Whether to recompute the fov (Would be false if the player didn't move that turn).
    # True by default because we have to compute it when the game starts.
    fov_recompute = True
    # Computes the fov_map
    fov_map = initialise_fov(game_map)

    # Stores the keyboard and mouse input. This will be updated throughout the game loop.
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Stores the current game state integer value, e.g. PLAYERS_TURN is 1.
    game_state = GameStates.PLAYERS_TURN

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
        render_all(con, entities, player, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)

        # Don't recompute the fov/repaint the tiles until after the player moves.
        fov_recompute = False

        # Flushes/draws the screen.
        libtcod.console_flush()

        # Erases all characters on the off-screen console.
        clear_all(con, entities)

        ### REACTS TO KEY PRESSES ###
        action = handle_keys(key)

        # Stores the value/s returned from dictionary key.
        # Performs an action if one of the variables is not empty.
        move = action.get("move")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")

        ########## PLAYER'S TURN ##########

        # Stores the results from the player's turn.
        # Each index defines what action should be taken.
        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            # Stores the coordinates to move to.
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            # Alters the player's position by dx/dy amount if the destination is not a blocked tile.
            if not game_map.is_blocked(destination_x, destination_y):
                # Stores the blocking entity if the destination if there is one.
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                # If there is a blocking entity:
                if target:
                    # Stores the attack results.
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                # If there is no blocking entity the player will move.
                else:
                    player.move(dx, dy)
                    # Recomputes the FOV map now the player has moved.
                    fov_recompute = True

            # Sets the game state to the enemy's turn.
            game_state = GameStates.ENEMY_TURN

        # EXIT.
        if exit:
            return True

        # FULLSCREEN.
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        ### Acts of player's turn results ###
        for player_turn_result in player_turn_results:
            message = player_turn_result.get("message")
            dead_entity = player_turn_result.get("dead")

            if message:
                print(message)

            if dead_entity:
                # If the dead entity is the player.
                # Gamestate will be set to PLAYER_DEAD
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)

                # If the dead entity is not the player it will be killed.
                else:
                    message = kill_monster(dead_entity)

                # Prints one of the messages.
                print(message)


        ########## ENEMY's TURN ##########
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get("message")
                        dead_entity = enemy_turn_result.get("dead")

                        if message:
                            print(message)

                        if dead_entity:
                            # If the dead entity is the player.
                            # Gamestate will be set to PLAYER_DEAD
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            # If the monster killed another monster.
                            else:
                                message = kill_monster(dead_entity)

                            # Prints one of the death messages.
                            print(message)

                            # Prevents the else/player's turn from occurring again by breaking the for loop.
                            if game_state == GameStates.PLAYER_DEAD:
                                break

            # If break wasn't called do this:
            else:
                # Sets the game state to the player's turn.
                game_state = GameStates.PLAYERS_TURN
############################################################


# Runs the main method if engine.py is ran.
if __name__ == "__main__":
    main()