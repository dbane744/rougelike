import libtcodpy as libtcod

from enum import Enum


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


def render_all(con, entities, player, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
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

    # Draw all entities in the list.
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map)


    # Prints the hp counter to screen. :02 means the strings include 02 spaces.
    libtcod.console_set_default_foreground(con, libtcod.white)
    libtcod.console_print_ex(con, 1, screen_height - 2, libtcod.BKGND_NONE, libtcod.LEFT,
                             "HP: {0:02}/{1:02}".format(player.fighter.hp, player.fighter.max_hp))

    # Blits the main off-screen console onto the root console.
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map):
    # Only draws the entity if it is in the player's fov.
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        # Sets the default font colour.
        libtcod.console_set_default_foreground(con, entity.color)
        # Places the entity on the console.
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # Erase the character that represents this object.
    libtcod.console_put_char(con, entity.x, entity.y, " ", libtcod.BKGND_NONE)