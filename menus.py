import libtcodpy as libtcod


def menu(con, header, options, width, screen_width, screen_height):
    """
    Creates a new console to hold any menus that may be used e.g the inventory.
    It then blits this menu to the root console.
    :param con: 
    :param header: 
    :param options: 
    :param width: 
    :param screen_width: 
    :param screen_height: 
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

def inventory_menu(con, header, inventory, inventory_width, screen_width, screen_height):
    """
    Utilises menu() to create an inventory menu.
    :param con: 
    :param header: 
    :param inventory_width: 
    :param screen_width: 
    :param screen_height: 
    :return: 
    """
    # Show a menu with each item of the inventory as an option.
    if len(inventory.items) == 0:
        options = ["Inventory is empty."]
    else:
        options = [item.name for item in inventory.items]

    # Creates the menu and blits it to the root console.
    menu(con, header, options, inventory_width, screen_width, screen_height)







