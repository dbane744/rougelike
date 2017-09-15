import libtcodpy as libtcod

from game_messages import Message

class Inventory:
    def __init__(self, capacity):
        """
        :param capacity: The maximum number of items the inventory can hold.
        """
        self.capacity = capacity
        self.items = []


    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                "item_added" : None,
                "message" : Message("You cannot carry any more, your inventory is full!", libtcod.yellow)
            })
        else:
            results.append({
                "item_added": item,
                "message": Message("You pick up the {0}.".format(item.name), libtcod.blue)
            })

            # Adds the item to the inventory.
            self.items.append(item)

        # Returns the results for the message log.
        return results