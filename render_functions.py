import libtcodpy as libtcod


def render_all(con, entities, game_map, screen_width, screen_height, colors):

    # Draw all tiles in the game map.
    for y in range(game_map.height):
        for x in range(game_map.width):
            # Stores whether the wall is blocked or not.
            wall_block = game_map.tiles[x][y].block_sight
            # Alters the tile colour depending on if it is blocked or not.
            if wall_block:
                libtcod.console_set_char_background(con, x, y, colors.get("dark_wall"), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con, x, y, colors.get("dark_ground"), libtcod.BKGND_SET)

    # Draw all entities in the list.
    for entity in entities:
        draw_entity(con, entity)

    # Blits the main off-screen console onto the root console.
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity):
    # Sets the default font colour.
    libtcod.console_set_default_foreground(con, entity.color)
    # Places the entity on the console.
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # Erase the character that represents this object.
    libtcod.console_put_char(con, entity.x, entity.y, " ", libtcod.BKGND_NONE)