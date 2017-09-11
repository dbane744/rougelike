import libtcodpy as libtcod

from game_states import GameStates


def kill_player(player):
    player.char = "%"
    player.color = libtcod.dark_red

    # Returns a string and a game state.
    return "You died!", GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = "{0} is dead!".format(monster.name.capitalize())

    # Turns the monster's entity into a passive corpse.
    monster.char = "%"
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.Name = "remains of " + monster.name

    return death_message