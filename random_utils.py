from random import randint


def from_dungeon_level(table, dungeon_level):
    """Takes in a list of lists where each list is [x, y] where x=value y=dungeon level.
        If the given dungeon level is equal or bigger to a corresponding level, value is returned."""
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value

    return 0

def random_choice_index(chances):
    """From a list of integers, randomly chooses the index of an integer based on a random chance integer and returns it"""
    random_chance = randint(1, sum(chances))
    
    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        if random_chance <= running_sum:
            return choice
        choice += 1


def random_choice_from_dict(choice_dict):
    """Takes in a dict of choice:chance(int). Splits the keys and values into lists and uses random_choice_index() to 
        randomly choose one of the choices dependant on the chance values."""

    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    return choices[random_choice_index(chances)]