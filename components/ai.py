import libtcodpy as libtcod


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
