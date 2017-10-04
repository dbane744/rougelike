import libtcodpy as libtcod

from game_messages import Message
from death_functions import kill_monster, kill_player
from fov_functions import initialise_fov, recompute_fov
from game_states import GameStates
from entity import Entity, get_blocking_entities_at_location
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from loader_functions.initialise_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box
from render_functions import render_all, clear_all


def main():
    # Initialises, returns and stores a dictionary of all constant values.
    constants = get_constants()
    # Sets the font.
    libtcod.console_set_custom_font("arial10x10.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    # Sets up the root console.
    libtcod.console_init_root(constants["screen_width"], constants["screen_height"], constants["window_title"], False)
    # Creates the main off-screen console.
    con = libtcod.console_new(constants["screen_width"], constants["screen_height"])
    # Creates the hp bar/log panel.
    panel = libtcod.console_new(constants["screen_width"], constants["panel_height"])

    # Will store the game variables.
    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False

    # Grabs an image from the project directory - it will be used for the main menu background.
    main_menu_background_image = libtcod.image_load("menu_background.png")

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        # Creates the main menu and blits it to the console.
        if show_main_menu:
            main_menu(con, main_menu_background_image, constants["screen_width"], constants["screen_height"])

            if show_load_error_message:
                message_box(con, "No save game found", 50, constants["screen_width"], constants["screen_height"])

            libtcod.console_flush()

            # Handles key presses.
            action = handle_main_menu(key)

            new_game = action.get("new_game")
            load_saved_game = action.get("load_game")
            exit_game = action.get("exit")

            # If the error message is open pressing one of the menu options will close the window.
            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            # If new game is selected get_game_variables() will be called for a the default setup.
            # And the default PLAYERS_TURN gamestate will be set.
            elif new_game:
                player, entities, game_map, message_log, game_state = get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN

                show_main_menu = False
            # Loads the game using load_game().
            elif load_saved_game:
                # Catching the possible FileNotFoundError in load_game().
                try:
                    player, entities, game_map, message_log, game_state = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    # Shows a message_box if the file cannot be loaded.
                    show_load_error_message = True
            # Exits the game by breaking the while loop.
            elif exit_game:
                break

        # If show_main_menu is False the player_game function will be called using the newly obtained game variables.
        else:
            libtcod.console_clear(con)
            play_game(player, entities, game_map, message_log, game_state, con, panel, constants)

            # This is set back to True when the play_game() is finished (the user presses ESC or exits).
            # Brings the user back to the main menu.
            show_main_menu = True

    # Sets up the game variables using the constants and returns each to a stored variable.
    # E.g. sets up the player entity.
    player, entities, game_map, message_log, game_state = get_game_variables(constants)


def play_game(player, entities, game_map, message_log, game_state, con, panel, constants):
    # Whether to recompute the fov (Would be false if the player didn't move that turn).
    # True by default because we have to compute it when the game starts.
    fov_recompute = True
    # Computes the fov_map
    fov_map = initialise_fov(game_map)

    # Stores the keyboard and mouse input. This will be updated throughout the game loop.
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Stores the previous game state. Used for changing gamestate and reverting without wasting a turn.
    # e.g when opening the inventory.
    previous_game_state = game_state

    # Stores which item requires targeting.
    targeting_item = None

    ############################################################
    # GAME LOOP
    ############################################################
    while not libtcod.console_is_window_closed():
        # Captures input - will update key and mouse variables with the input.
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        # Recomputes the FOV if necessary.
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants["fov_radius"], constants["fov_light_walls"],
                          constants["fov_algorithm"])

        # Draws all entities to the off-screen console and blits the console to the root.
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants["screen_width"],
                   constants["screen_height"], constants["bar_width"], constants["panel_height"], constants["panel_y"],
                   mouse, constants["colors"], game_state)

        # Don't recompute the fov/repaint the tiles until after the player moves.
        fov_recompute = False

        # Flushes/draws the screen.
        libtcod.console_flush()

        # Erases all characters on the off-screen console.
        clear_all(con, entities)

        ##### REACTS TO A KEY PRESS OR A MOUSE CLICK #####
        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        # Stores the value/s returned from dictionary key.
        # Performs an action if one of the variables is not empty.

        # Key presses:
        move = action.get("move")
        pickup = action.get("pickup")
        show_inventory = action.get("show_inventory")
        drop_inventory = action.get("drop_inventory")  # An inventory screen where you can only drop items.
        inventory_index = action.get("inventory_index")
        take_stairs = action.get("take_stairs")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")

        # Mouse clicks:
        left_click = mouse_action.get("left_click")
        right_click = mouse_action.get("right_click")

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

        # If the pickup button was pressed (g).
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                # If the overlapping entity can be picked up.
                if entity.item and entity.x == player.x and entity.y == player.y:
                    # Adds the item to the inventory and results the results.
                    # Results include a Message and the grabbed Item object.
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    # Breaks so we can only pickup one item at a time.
                    break
            else:
                message_log.add_message(Message("There is nothing here to pick up", libtcod.yellow))

        # If 'i' was pressed for inventory it changes the gamestate while storing the previous state.
        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY
        # If 'd' was pressed for the drop inventory.
        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        # Selects an item in the inventory using the index value of the item.
        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                player.inventory.items):
            item = player.inventory.items[inventory_index]
            # If the SHOW_INVENTORY state, the item will be used.
            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
            # If the DROP_INVENTORY state, the item will be dropped.
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        # If the player has attempted to move down some stairs.
        if take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                # If the player IS on the same tile as the stairs.
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    # Creates a new dungeon floor and returns and stores a new set of entities for the new floor.
                    entities = game_map.next_floor(player, message_log, constants)
                    # Initialises the fov mapf or the new floor.
                    fov_map = initialise_fov(game_map)
                    fov_recompute = True
                    # Clears the console of the old game map.
                    libtcod.console_clear(con)
                    # Prevents other entities from being checked.
                    break
                else:
                    message_log.add_message(Message("There are no stairs here.", libtcod.yellow))

        # If the game state has bene set to tarrgeting mode it will check if any left or right clicks have been made
        # Left clicks use the item stored in 'targeting_item' and will extend the results to player_turn_results.
        # Right click appends 'targeting_cancelled'. to the player results.
        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click

                item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({"targeting_cancelled": True})

        # Exits the game. UNLESS a menu is open then it just closes the menu.
        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            # If the user is targeting ESC only exist the targeting game state.
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            # Saves the game and exits the game.
            else:
                save_game(player, entities, game_map, message_log, game_state)
                return True

        # Fullscreen.
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        ### Acts on player's turn results including adding to message log. ###
        for player_turn_result in player_turn_results:
            message = player_turn_result.get("message")
            dead_entity = player_turn_result.get("dead")
            item_added = player_turn_result.get("item_added")
            item_consumed = player_turn_result.get("consumed")
            item_dropped = player_turn_result.get("item_dropped")
            targeting = player_turn_result.get("targeting")
            targeting_cancelled = player_turn_result.get("targeting_cancelled")

            if message:
                message_log.add_message(message)

            if dead_entity:
                # If the dead entity is the player.
                # Gamestate will be set to PLAYER_DEAD
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)

                # If the dead entity is not the player it will be killed.
                else:
                    message = kill_monster(dead_entity)

                # Prints one of the messages.
                message_log.add_message(message)

            # If an item was picked up it removes it form the entity list and sets the game state to enemy turn.
            # (The entity is no longer on the map so it is removed)
            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN

            # Consuming an item triggers the enemy turn.
            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            # Switches the game state to TARGETING, stores the targeting item and adds the targeting message to the log.
            if targeting:
                # Changes the previous game state to PLAYERS_TURN rather than INVENTORY so that cancelling the targeting
                # mode (with ESC) returns the playher back to the main console rather than the inventory screen.
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING
                targeting_item = targeting
                message_log.add_message(targeting_item.item.targeting_message)

            # If the user cancelled targeting the previous state will be reverted.
            if targeting_cancelled:
                game_state = previous_game_state
                message_log.add_message(Message("Targeting cancelled"))

            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN

        ########## ENEMY's TURN ##########
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                # If the entity has the ai component.
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get("message")
                        dead_entity = enemy_turn_result.get("dead")

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            # If the dead entity is the player.
                            # Gamestate will be set to PLAYER_DEAD
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            # If the monster killed another monster.
                            else:
                                message = kill_monster(dead_entity)

                            # Prints one of the death messages.
                            message_log.add_message(message)

                            # Prevents the else/player's turn from occurring again by breaking the for loop.
                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    # Prevents the else/player's turn from occurring again by breaking the for loop.
                    if game_state == GameStates.PLAYER_DEAD:
                        break
            # If break wasn't called do this:
            else:
                # Sets the game state to the player's turn.
                game_state = GameStates.PLAYERS_TURN
                ############################################################


# Runs the main method if engine.py is executed.
if __name__ == "__main__":
    main()