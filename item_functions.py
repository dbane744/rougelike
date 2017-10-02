import libtcodpy as libtcod

from game_messages import Message

from components.ai import ConfusedMonster

def heal(*args, **kwargs):
    """
    Manages a heal - delegates the actual healing to entity.fighter and returns appropriate results.
    :param args: The entity affected by the heal.
    :param kwargs: The amount of hp points to heal.
    :return: The results as key value pairs.
    """
    entity = args[0]
    amount = kwargs.get("amount")

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({"consumed": False, "message": Message("You are already at full health", libtcod.yellow)})
    else:
        # Calls the identically named function in the fighter class to actually heal the entity.
        entity.fighter.heal(amount)
        results.append({"consumed":True, "message": Message("Your wounds start to feel better!", libtcod.green)})

    return results

def cast_lightning(*args, **kwargs):
    """

    :param args: Args[0] should be the caster of the spell.
    :param kwargs: Should include the entities list, the fov_map, the amount of damage and the maximum spell range.
    """
    caster = args[0]
    entities = kwargs.get("entities")
    fov_map = kwargs.get("fov_map")
    damage = kwargs.get("damage")
    maximum_range = kwargs.get("maximum_range")

    results = []

    target = None
    closest_distance = maximum_range + 1 # Will store the distance of each entity.

    # Finds the closest entity to the player (if there is one).
    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({"consumed": True, "target": target, "message": Message("A lightning bolt strikes the {0} "
                                                                               "inflicting {1} damage".format(target.name,
                                                                                                          damage))})
    else:
        results.append({"consumed": False, "target": None, "message": Message("No enemy in range.", libtcod.red)})

    return results


def cast_fireball(*args, **kwargs):
    entities = kwargs.get("entities") # The entities list.
    fov_map = kwargs.get("fov_map")
    damage = kwargs.get("damage")
    radius = kwargs.get("radius")
    target_x = kwargs.get("target_x")
    target_y = kwargs.get("target_y")

    results = []

    # If the target is outside the field of view.
    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({"consumed": False, "message": Message("You cannot target a tile outside your field of view.", libtcod.yellow)})
        return results

    # If the target is in the field of view the spell will cast.

    results.append({"consumed": True, "message": Message("You cast fireball, burning everythin with {0} tiles of the target."
                                                         .format(radius), libtcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({"message": Message("The {0} gets burned for {1} hit points.".format(entity.name, damage))})
            results.extend(entity.fighter.take_damage(damage))

    return results

def cast_confuse(*args, **kwargs):
    entities = kwargs.get("entities") # The entities list.
    fov_map = kwargs.get("fov_map")
    target_x = kwargs.get("target_x")
    target_y = kwargs.get("target_y")

    results = []

    # If the selected tile is not in the FOV.
    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({"consumed": False, "message": Message("You cannot target a tile outside your field of view.",
                                                              libtcod.yellow)})
        return results

    # If the selected tile contains an entity with an AI it will cast confuse on it.
    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            # Creates a new confused_ai for the monster(which takes the previous AI as an argument)
            confused_ai = ConfusedMonster(entity.ai, 10)
            # Must set the owner of the new confused_ai.
            confused_ai.owner = entity
            # Finally, sets the entity's AI to the new confused AI.
            entity.ai= confused_ai

            results.append({"consumed": True, "message": Message("The {0} looks confused!".format(entity.name), libtcod.light_green)})

            break
    # No entity on the target tile was found.
    else:
        results.append({"consumed": False, "message": Message("There is not targetable enemy at that location.",libtcod.yellow)})

    return results