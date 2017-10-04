

class Stairs:
    """
    Encapsulates the stairs as a component of Entity.
    These stairs only allow one directional movement.
    (Can't go back up the stairs if you travel downwards)
    """
    def __init__(self, floor):
        """
        :param floor: This integer tells us which floor the stair takes us to if the player uses the stairs.
        """
        self.floor = floor
