

class Item:
    """
    This component is added to an entity if it can be picked up as an item by the player.
    """
    def __init__(self, use_function=None, **kwargs):
        self.use_function = use_function
        self.function_kwargs = kwargs