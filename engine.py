import libtcodpy as libtcod

from components.inventory import Inventory
from game_messages import Message, MessageLog
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
    max_monsers_per_room = 3
    max_items_per_room = 2

    colors = {
        "dark_wall": libtcod.Color(64, 64, 64),
        "dark_ground": libtcod.Color(68, 36, 52),
        "light_wall": libtcod.Color(133, 149, 161),
        "light_ground": libtcod.Color(133, 76, 48)
    }


    # Creates the player's components.
    fighter_component = Fighter(hp=30, defense=2, power=5)
    inventory_component = Inventory(26)
    # Creates the player object.
    player = Entity(0, 0, "@", libtcod.white, "Player", blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component)
    # Creates a list of initial static entities.
    entities = [player]

    # Sets the font.
    libtcod.console_set_custom_font("arial10x10.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    # Sets up the root console.
    libtcod.console_init_root(screen_width, screen_height, "My First Rougelike", False)
    # Creates the main off-screen console.
    con = libtcod.console_new(screen_width, screen_height)
    # Creates the hp bar/log panel.
    panel = libtcod.console_new(screen_width, panel_height)
    # Creates the game map and calls its make_map function.
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
                      max_monsers_per_room, max_items_per_room)

    # Whether to recompute the fov (Would be false if the player didn't move that turn).
    # True by default because we have to compute it when the game starts.
    fov_recompute = True
    # Computes the fov_map
    fov_map = initialise_fov(game_map)

    message_log = MessageLog(message_x, message_width, message_height)

    # Stores the keyboard and mouse input. This will be updated throughout the game loop.
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Stores the current game state integer value, e.g. PLAYERS_TURN is 1.
    game_state = GameStates.PLAYERS_TURN
    # Stores the previous game state. Used for changing gamestate and reverting without wasting a turn.
    # e.g when opening the inventory.
    previous_game_state = game_state

############################################################
                        # GAME LOOP
############################################################
    while not libtcod.console_is_window_closed():
        # Captures input - will update key and mouse variables with the input.
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE_PRESS, key, mouse)

        # Recomputes the FOV if necessary.
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        # Draws all entities to the off-screen console and blits the console to the root.
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
                   bar_width, panel_height, panel_y, mouse, colors, game_state)

        # Don't recompute the fov/repaint the tiles until after the player moves.
        fov_recompute = False

        # Flushes/draws the screen.
        libtcod.console_flush()

        # Erases all characters on the off-screen console.
        clear_all(con, entities)

        ##### REACTS TO KEY PRESSES #####
        action = handle_keys(key, game_state)

        # Stores the value/s returned from dictionary key.
        # Performs an action if one of the variables is not empty.
        move = action.get("move")
        pickup = action.get("pickup")
        show_inventory = action.get("show_inventory")
        drop_inventory = action.get("drop_inventory") # An inventory screen where you can only drop items.
        inventory_index = action.get("inventory_index")
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
                player_turn_results.extend(player.inventory.use(item))
            # If the DROP_INVENTORY state, the item will be dropped.
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))


        # Exits the game. UNLESS a menu is open then it just closes the menu.
        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            else:
                return True

        # FULLSCREEN.
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        ### Acts on player's turn results including adding to message log. ###
        for player_turn_result in player_turn_results:
            message = player_turn_result.get("message")
            dead_entity = player_turn_result.get("dead")
            item_added = player_turn_result.get("item_added")
            item_consumed = player_turn_result.get("consumed")
            item_dropped = player_turn_result.get("item_dropped")

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