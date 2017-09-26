import libtcodpy as libtcod

from game_messages import Message


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