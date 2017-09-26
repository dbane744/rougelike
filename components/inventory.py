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

    def use(self, item_entity, **kwargs):
        """
        Uses the item's use function with any additional **kwargs.
        :param item_entity: The item entity to use.
        :type item_entity: Entity
        :param kwargs: Any optional extra kwargs to add to the items own kwargs.
        :return:
        """
        results = []

        # Grabs the item component from the entity.
        item_component = item_entity.item

        # If the item does not have a use_function(a stored function in its attributes).
        if item_component.use_function is None:
            results.append({"message": Message("The {0} cannot be used".format(item_entity.name), libtcod.yellow)})
        else:
            # Grabs the kwargs from the item class e.g the hp potion sets this to a heal amount.
            kwargs = {**item_component.function_kwargs, **kwargs}
            # grabs the use function from the item class - this is a function stored is an attribute.
            item_use_results = item_component.use_function(self.owner, **kwargs)

            # If the items use function returns 'consumed' on use it will call remove_item().
            for item_use_result in item_use_results:
                if item_use_result.get("consumed"):
                    self.remove_item(item_entity)

            # Extends the results then returns them.
            results.extend(item_use_results)

        return results

    def remove_item(self, item):
        "Removes an item from the item list"
        self.items.remove(item)

    def drop_item(self, item):
        results = []

        # The item will be dropped on the same tile as the player.
        # This changes the Entity x and y values of the item.
        item.x = self.owner.x
        item.y = self.owner.y

        # Removes the item from the inventory list.
        self.remove_item(item)
        results.append({"item_dropped": item, "message": Message("You dropped the {}".format(item.name),
                                                                 libtcod.yellow)})
        return results