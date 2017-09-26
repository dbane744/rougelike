import libtcodpy as libtcod


def initialise_fov(game_map):
    """
    Generates the FOV map for further use.
    :param game_map: 2D list of Tiles.
    :return: A libtcod map.
    """
    fov_map = libtcod.map_new(game_map.width, game_map.height)

    # "not" for the variables because .map_set_properties has the opposites:
    # ...is_transparent, is_walkable)
    for y in range(game_map.height):
        for x in range(game_map.width):
            libtcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight,
                                       not game_map.tiles[x][y].blocked)
    return fov_map


def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm = 0):
    """
    Recomputes the FOV using a libtcodpy algorithm.
    :param fov_map: The litcodpy map generated in initialise_fov().
    :param x: Current player position.
    :param y: Current player position.
    :param radius: FOV radius.
    :param light_walls: Should the walls be lit?
    :param algorithm: Which libtcodpy algorithm to use.
    :return: 
    """
    libtcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)
