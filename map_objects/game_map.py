from random import randint  # Used for generating random room sizes and positions.

from map_objects.tile import Tile
from map_objects.rectangle import Rect


class GameMap:
    """
    Encapsulates the game map.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialise_tiles()

    def initialise_tiles(self):
        """
        Creates a pseudo 2D array using list comprehensions. Fills this array with tiles.
        :return: A nested 2D list of tiles.
        """
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):
        """
        Creates the map. Chisels out all of the rooms and paths. 
        :param max_rooms: Integer.
        :param room_min_size: Integer.
        :param room_max_size: Integer.
        :param map_width: Integer.
        :param map_height: Integer.
        :param player: The player's entity object.
        :return: None
        """
        # Stores the rooms in a list.
        rooms = []
        # Counts the number of rooms currently created.
        num_rooms = 0

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

                # Finally, append the new room to the room list.
                rooms.append(new_room)
                num_rooms += 1



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

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        else:
            return False


