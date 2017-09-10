class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    def __init__(self, x, y, char, color, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks  # Does the entity block the player's movement?

    def move(self, dx, dy):
        # Moves the entity by the given amount.
        self.x += dx
        self.y += dy

###### STANDALONE FUNCTIONS ######

def get_blocking_entities_at_location(entities, destination_x, destination_y):
    """
    Returns the blocking entity at the given location.
    :param entities: 
    :param destination_x: 
    :param destination_y: 
    :return: Returns the blocking Entity object or None.
    """
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y ==  destination_y:
            return entity

    # Returns None if there is no blocking entity.
    return None

