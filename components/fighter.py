import libtcodpy as libtcod

from game_messages import Message


class Fighter:
    """
    Encapsulates fighter methods and variables for entities that can fight.
    """
    def __init__(self, hp, defense, power):
        self.max_hp = hp        # Max hp
        self.hp = hp            # Current hp
        self.defense = defense  # Defense
        self.power = power      # Attack power

    def take_damage(self, amount):
        # Stores any game state changes.
        results = []

        self.hp -= amount

        # If the player dies.
        if self.hp <= 0:
            results.append({"dead": self.owner})

        return results

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

