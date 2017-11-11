import libtcodpy as libtcod

from enum import Enum, auto

from game_states import GameStates
from menus import character_screen, inventory_menu, level_up_menu


class RenderOrder(Enum):
    """
    Enumerates the render order for each entity for ease of use.
    Entities listed first will be drawn first.
    """
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


def get_names_under_mouse(mouse, entities, fov_map):
    """
    Finds the entity names of those on a clicked tile and returns the names as a string.
    :param mouse: The libtcod mouse object.
    :param entities: The entities list.
    :param fov_map: The fov map.
    :return: A string that specifies which entities are on the clicked tile.
    """
    # Stores mouse position.
    (x, y) = (mouse.cx, mouse.cy)

    # List comprehension to add all the entity names at that point to a list.
    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]

    # Joins each element of the list with a string seperator.
    names = ", ".join(names)

    #Capitalises and returns the names string.
    return names.capitalize()


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    """
    Draws the health bar in the bottom panel.
    :param panel: 
    :param x: 
    :param y: 
    :param total_width: 
    :param name: 
    :param value: 
    :param maximum: 
    :param bar_color: 
    :param back_color: 
    :return: 
    """
    # Stores the width of the current HP rectangle.
    bar_width = int(float(value) / maximum * total_width)

    # The colour of the back/maximum hp rectangle.
    libtcod.console_set_default_background(panel, back_color)
    # Creates the maximum HP rectangle.
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    # The colour of the HP portion of the HP bar *(probably best to set it to red).
    libtcod.console_set_default_background(panel, bar_color)
    # If the player has any hp left.
    if bar_width > 0:
        # Draws the inner HP rectangle.
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    # Prints the HP text next to the bar.
    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             "{0}: {1}/{2}".format(name, value, maximum))

def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
               bar_width, panel_height, panel_y, mouse, colors, game_state):

    ########## RENDERS TILES ##########

    # Only renders walls if the fov has changed or game just started.
    if fov_recompute:
        # Draw all tiles in the game map.
        for y in range(game_map.height):
            for x in range(game_map.width):
                # Stores whether the tile is in the fov (field of view).
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                # Stores whether the wall is blocked or not.
                wall_block = game_map.tiles[x][y].block_sight

                # Colours the visible tiles.
                if visible:
                    if wall_block:
                        libtcod.console_set_char_background(con, x, y, colors.get("light_wall"), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x , y, colors.get("light_ground"), libtcod.BKGND_SET)
                    # Sets the visible tile as 'explored'.
                    game_map.tiles[x][y].explored = True
                # Colours the tiles outside the fov if they have been explored.
                elif game_map.tiles[x][y].explored:
                    if wall_block:
                        libtcod.console_set_char_background(con, x, y, colors.get("dark_wall"), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get("dark_ground"), libtcod.BKGND_SET)

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    ########## RENDERS ENTITIES ##########

    # Draw all entities in the list.
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)

    ########## BLITS MAIN CONSOLE ##########

    # Blits the main off-screen console onto the root console.
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    # Clears the HP panel.
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    ########## RENDERS MESSAGE LOG ##########

    # Prints the game messages, one line at a time.
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    ########## RENDERS HP BAR ##########

    render_bar(panel, 1, 1, bar_width, "HP", player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)

    ########## DEPTH LEVEL / FLOOR COUNTER ##########

    libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT,
                             "Dungeon level: {0}".format(game_map.dungeon_level))

    ########## RENDERS entities-under-mouse message ##########

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_names_under_mouse(mouse, entities, fov_map))

    ########## BLITS BOTTOM PANEL ##########

    # Blits the bottom panel to the screen.
    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    ########## BLITS THE INVENTORY MENU IF APPLICABLE ##########

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = "Press the key next to an item to use it, or Esc to cancel.\n"
        else: # Else the inventory must be the drop inventory...
            inventory_title = "Press the key next to an item to drop it, or Esc to cancel.\n"

        # Creates the inventory menu and blits it to the screen.
        inventory_menu(con, inventory_title,
                       player, 50, screen_width, screen_height)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, "Level up! Choose a state to raise:", player, 40, screen_width, screen_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map, game_map):
    # Only draws the entity if it is in the player's fov OR if the entity is stairs and has been explored.
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        # Sets the default font colour.
        libtcod.console_set_default_foreground(con, entity.color)
        # Places the entity on the console.
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # Erase the character that represents this object.
    libtcod.console_put_char(con, entity.x, entity.y, " ", libtcod.BKGND_NONE)