""" Component of entity. Encapsulates the slot and stats of an equippable entity. """

class Equippable(object):
    """Tells us which items are equippable."""
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        self.slot = slot
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus

