import libtcodpy as libtcod
from random import randint  # Used for generating random room sizes and positions.

from components.item import Item
from components.stairs import Stairs
from render_functions import RenderOrder
from components.fighter import Fighter
from components.ai import BasicMonster
from entity import Entity
from game_messages import Message
from item_functions import cast_confuse, cast_fireball, cast_lightning, heal
from map_objects.tile import Tile
from map_objects.rectangle import Rect


class GameMap:
    """
    Encapsulates the game map.
    """

    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        # Creates a list of tiles.
        self.tiles = self.initialise_tiles()
        # Stores the current dungeon level.
        self.dungeon_level = dungeon_level

    def initialise_tiles(self):
        """
        Creates a pseudo 2D array using list comprehensions. Fills this array with tiles.
        :return: A nested 2D list of tiles.
        """
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
                 max_monsters_per_room, max_items_per_room):
        """
        Creates the map. Chisels out all of the rooms and paths. Places all entities.
        Places a stairway in the middle of the last room.
        :param max_rooms: Integer.
        :param room_min_size: Integer.
        :param room_max_size: Integer.
        :param map_width: Integer.
        :param map_height: Integer.
        :param player: The player's entity object.
        :param entities: The list of entities
        :param max_monsters_per_room: Integer of max monsters per room.
        :return: None
        """


        # Stores the rooms in a list.
        rooms = []
        # Counts the number of rooms currently created.
        num_rooms = 0

        # Stores the centre of the last room to place the stairs here.
        centre_of_last_room_x = None
        centre_of_last_room_y = None

        ####### SPAWNS ROOMS #######
        for r in range(max_rooms):
            # Generates a random room width and height.
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # Generates a random position without going outside the map boundaries.
            # Subtracts 1 because the top corner is a wall tile not the inside of the room -
            # Without subtracting 1 the outer right/bottom wall could be destroyed.
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # Makes a new rectangular room using the newly generated values.
            new_room = Rect(x, y, w, h)

            # Runs through the other rooms and checks if they intersects with this one.
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # NICE USE OF THIS FOR/ELSE! If the for loop doesn't break else is ran.
                # If the new room did not intersect with any other room it will be built.

                # Creates the room.
                self.create_room(new_room)

                # Stores the centre coordinates of the new room.
                (new_x, new_y) = new_room.center()

                # Will end up storing the centre of the last room for stair placement.
                centre_of_last_room_x = new_x
                centre_of_last_room_y = new_y

                # Puts the player in the centre of the first room.
                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y
                # If the number of rooms in the list is NOT 0.
                else:
                    # All rooms after the first.
                    # Connect it to the previous room with a tunnel.

                    # Centre coordinates of the previous room.
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # Flip a coin (Random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # First move horizontally, then vertically.
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # First move vertically, then horizontally.
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # Spawns entities (the player was already spawned earlier).
                self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)

                # Finally, append the new room to the room list.
                rooms.append(new_room)
                num_rooms += 1

        # Creates the stairs component - sets its level to the next dungeon level directly below.
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(centre_of_last_room_x, centre_of_last_room_y, ">", libtcod.white, "Stairs",
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)


    def create_room(self, room):
        # Goes through the tiles in a rectangle(room) and makes them passable.
        # x1 and y1 adds 1 to prevent rooms from merging - the coordinates include the walls of the room.
        # x2 and y2 do not add 1 because Python's range function does not include the 'end' value in its range.
        # (So it has the same effect as x1 + 1 and x2 + 1)
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    # Create a horizontal tunnel between two points
    # max + 1 because Python's range function does not include the 'end' value.
    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    # Create a vertical tunnel between two points.
    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities, max_monsters_per_room, max_items_per_room):
        """
        Places a random number of entities in a given room.
        :param room: Which room to place the enities in.
        :param entities: The current entities list.
        :param max_monsters_per_room:
        :param max_items_per_room:
        :return:
        """

        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)
        # Get a random number of items.
        number_of_items = randint(0, max_items_per_room)

        ####### SPAWNS MONSTERS #######

        # Chooses random locations in the room to place the monsters.
        for i in range(number_of_monsters):
            # Chooses a random location in the room.
            # +1 and -1 because the first values are the room walls.
            # Unlike in the 'in range()' function, x2 and y2 are included in the randint range.
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # Only places the monster if there is no other entity on that coordinate.
            # It does this by making a list comprehension of entities if the entity overlaps.
            # If this new list is empty it will place the monster.
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                # 80% chance this monster will be an ORC.
                # 20% chance this monster will be a TROLL.
                # SPAWNS ORC
                if randint(0, 100) < 80:
                    fighter_component = Fighter(hp=10, defense=0, power=3, xp=35)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, "o", libtcod.desaturated_green, "Orc", blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                # SPAWNS TROLL.
                else:
                    fighter_component = Fighter(hp=16, defense=1, power=4, xp=100)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, "T", libtcod.darker_green, "Troll", blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

                # Appends the monster to the entities list.
                entities.append(monster)

        ####### SPAWNS ITEMS #######

        # Chooses a random location in the room to place the item.
        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # Places an item if the tile is empty of entities.
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                # Random int that dictates which item should be spawned.
                item_chance = randint(0, 100)

                # SPAWNS HEALING POTION - 70% CHANCE.
                if item_chance < 70:
                    # Giving the potion an item component allows it to be picked up.
                    item_component = Item(use_function=heal, amount=4)
                    item = Entity (x, y, "!", libtcod.violet, "Healing Potion", render_order=RenderOrder.ITEM,
                                   item=item_component)
                # SPAWNS FIREBALL SCROLL - 10% CHANCE.
                elif item_chance < 80:
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        "Left-click a target tile for the fireball, or right-click to cancel.", libtcod.light_cyan),
                                          damage=12, radius=3)
                    item = Entity(x, y, "#", libtcod.red, "Fireball Scroll", render_order=RenderOrder.ITEM,
                                  item=item_component)
                # SPAWNS LIGHTNING SCROLL - 10% CHANCE.
                elif item_chance < 90:
                    item_component = Item(use_function=cast_lightning, damage=20, maximum_range=5)
                    item = Entity(x, y, "#", libtcod.yellow, "Lightning Scroll", render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_chance <= 100:
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        "Left-click an enemy to confuse it, or right-click to cancel.", libtcod.light_cyan))
                    item = Entity(x, y, "#", libtcod.light_pink, "Confusion Scroll", render_order=RenderOrder.ITEM,
                                  item=item_component)

                entities.append(item)


    def is_blocked(self, x, y):
        """
        Checks if the given tile is blocked by a blocking tile.
        :param x: X position of the tile in question.
        :param y: Y position of the tile in question.
        :return: True or False depending on whether the tile is blocked.
        """
        if self.tiles[x][y].blocked:
            return True
        else:
            return False

    def next_floor(self, player, message_log, constants):
        """
        Generates the next floor of the dungeon and heals half of the players max hp.
        :return: A new list of entities for the new floor (contains just the player).
        """
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialise_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities,
                      constants['max_monsters_per_room'], constants['max_items_per_room'])

        # Heals half the player's max hp.
        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message("You take a moment to rest, and recover your strength", libtcod.light_violet))

        return entities
