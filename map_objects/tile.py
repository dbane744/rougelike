class Tile:
    """
    A tile on a map. it may or may not be blocked, and may or may not block sight.
    """

    def __init__(self, blocked, block_sight=None):
        # Can characters walk through this tile?
        self.blocked = blocked

        # By default, if a tile is blocked, it also blocks sights.
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
        # Stores whether the tile has been explored by the player.
        # All tiles start off unexplored.
        self.explored = False
