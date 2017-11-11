import libtcodpy as libtcod

from game_messages import Message


class Fighter:
    """
    Encapsulates fighter methods and variables for entities that can fight.
    """
    def __init__(self, hp, defense, power, xp=0):
        self.base_max_hp = hp        # Max hp
        self.hp = hp                 # Current hp
        self.base_defense = defense  # Defense
        self.base_power = power      # Attack power
        self.xp = xp                 # The amount of xp rewarded on this fighter's death.

    # Use the properties to get the stats as they include equipment bonuses.
    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    def take_damage(self, amount):
        # Stores any game state changes.
        results = []

        self.hp -= amount

        # If the fighter dies.
        if self.hp <= 0:
            results.append({"dead": self.owner, 'xp' : self.xp})

        return results

    def heal(self, amount):
        """
        Heals the entity by a certain amount.
        Is meant to work in conjunction with the heal function in item_functions.
        :param amount: The number of hp points to heal.
        """
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        results =[]

        damage = self.power - target.fighter.defense

        if damage > 0:

            results.append({"message": Message(("{0} attacks {1} for {2} hit points.").format(self.owner.name.capitalize(),
                  target.name, str(damage)))})

            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({"message": Message(("{0} attacks {1} but does not damage.").format(self.owner.name.capitalize(),
                                                               target.name))})

        return results
