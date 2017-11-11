import libtcodpy as libtcod

"""
This module encapsulates the different menus within the game.
"""

def menu(con, header, options, width, screen_width, screen_height):
    """
    Creates a new console to hold any menus that may be used e.g the inventory.
    It then blits this menu to the root console.
    :param con: The root console.
    :param header: A string that will be printed to the header.
    :type  header: String
    :param options: A list of strings that should be printed to the menu.
    :param width: Width of the menu.
    :type  width: Int
    :param screen_width: Width of the whole screen.
    :param screen_height: Height of the whole screen.
    :return: 
    """
    if len(options) > 26: raise ValueError("Cannot have a menu with more than 26 options.")

    # Calculate total height for the header (after auto-wrap) and one line per option.
    #.console_get_height_rect returns the expected height of the header.
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # Create an off-screen console that represents the menu's window.
    window = libtcod.console_new(width, height)

    # Print the header, without auto-wrap.
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # Print all the options.
    y = header_height # Will grow larger as the text is printed.
    letter_index = ord("a")
    for option_text in options:
        text = "(" + chr(letter_index) + ") " + option_text
        libtcod.console_print_ex(window,0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1 # Uses the next unicode value.

    # Blit the contents of "Window" to the root console.
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def inventory_menu(con, header, inventory, inventory_width, screen_width, screen_height, player):
    """
    Utilises menu() to create an inventory menu.
    :param con: The root console to blit to.
    :param header: 
    :param inventory_width: 
    :param screen_width: 
    :param screen_height: 
    :return: 
    """
    # Show a menu with each item of the inventory as an option.
    if len(player.inventory.items) == 0:
        options = ["Inventory is empty."]
    else:
        options = []

        # Adds item names to inventory menu - also adds which equipment slot they are on if applicable.
        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append("{} - (on main hand)".format(item.name))
            elif player.equipment.off_hand == items:
                options.append("{} - (on off hand)".format(item.name))
            else:
                options.append(item.name)

    # Creates the menu and blits it to the root console.
    menu(con, header, options, inventory_width, screen_width, screen_height)


def main_menu(con, background_image, screen_width, screen_height):
    """
    Creates the main menu and uses menu() to blit it to the console.
    :param con:
    :param background_image:
    :param screen_width:
    :param screen_height:
    """
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             "THE ADVENTURES OF KRULL")
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 3), libtcod.BKGND_NONE, libtcod.CENTER,
                             "By Daniel Bane")

    menu(con, "", ["Start new game", "Continue last game", "Quit"], 24, screen_width, screen_height)

def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    """
    Cretaes the menu that appears when the player levels up. Allows the player to increase a stat.
    """
    options = ["Constitution (+20 HP, from {0})".format(player.fighter.max_hp),
               "Strength (+1 attack, from {0})".format(player.fighter.power),
               "Agility (+1 defense, from {0})".format(player.fighter.defense)]

    menu(con, header, options, menu_width, screen_width, screen_height)

def message_box(con, header, width, screen_width, screen_height):
    """
    Creates and blits a message box to the given console.
    (It is basically just an empty menu with a header as a message)
    """
    # screen_height-12 so the box is not printed directly in the centre ( so it doesn't overlap the main menu options).
    menu(con, header, [], width, screen_width, screen_height - 12)


def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    """
    Unlike the other menus, the character screen doesn't display options for the user to select -
    it directly prints information to the screen.
    """
    window = libtcod.console_new(character_screen_width, character_screen_height)
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Character Information')
    libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Level: {0}'.format(player.level.current_level))
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience: {0}'.format(player.level.current_xp))
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience to Level: {0}'.format(player.level.experience_to_next_level))
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Maximum HP: {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Attack: {0}'.format(player.fighter.power))
    libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Defense: {0}'.format(player.fighter.defense))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)





