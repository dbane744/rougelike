

class Item:
    """
    This component is added to an entity if it can be picked up as an item by the player.
    """
    def __init__(self, use_function=None, targeting=False, targeting_message=None, **kwargs):
        self.use_function = use_function
        # If True, the item requires the player to select a target before use.
        self.targeting = targeting
        # Stores a message that will be shown in the message log if the item needs targeting.
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs
