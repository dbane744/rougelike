import libtcodpy as libtcod

from random import randint

from game_messages import Message


# This module will contain AI components for different entities.


class BasicMonster:

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            # If the monster is not adjacent to the player it will move towards.
            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)

            elif monster.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results

class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        # Generates a random movement in the x and y directions.
        if self.number_of_turns > 0:
            # Movement of either -1, 0 or 1.
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            # If the tile to move to is not the currently occupied tile the monster will attempt to move there.
            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            # -1 to the number of turns taken while confused.
            self.number_of_turns - 1
        # If the confused timer has run out the monster will reset to its previous AI.
        else:
            self.owner.ai = self.previous_ai
            results.append({"message": Message("The {0} is no longer confused!".format(self.owner.name, libtcod.red))})

        return results