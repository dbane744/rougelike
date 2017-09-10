import libtcodpy as libtcod


def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
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

    # Draw all entities in the list.
    for entity in entities:
        draw_entity(con, entity, fov_map)

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