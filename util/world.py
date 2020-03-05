from django.contrib.auth.models import User
from adventure.models import Player, Room

from util.sample_generator import *

# players=Player.objects.all()
# for p in players:
#   p.currentRoom=r_outside.id
#   p.save()

# world = World()
# num_rooms = 44
# width = 8
# height = 7
# world.generate_rooms(width, height, num_rooms)

# biomes
biomes = ['Grass lands',
          'Desert lands',
          'Forrest lands',
          'Sea lands',
          'Lava lands',
          'Rock lands',
          'Mountain lands'
          'Ice lands',
          'Jungle lands',
          'Swamp lands']

opposite_direction = {'w' : 'e', 'n' : 's', 's' : 'n', 'e' : 'w'}

def generate_rooms(size_x, size_y):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        grid = [None] * size_y
        width = size_x
        height = size_y
        num_rooms = size_x * size_y
        for i in range( len(grid) ):
            grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1 # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west


        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:

            # Calculate the direction of the room to be created
            if direction > 0 and x < size_x - 1:
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                y += 1
                direction *= -1

            biome_number = room_count // 9
            if biome_number >= len(biomes):
                biome_number = len(biomes) - 1
            biome = biomes[biome_number]


            # Create a room in the given direction
            room = models.Room(title=str(room_count), description="This is a generic room.",
                               x=x, y=y, biome=biome)
            room.save()

            # Note that in Django, you'll need to save the room after you create it

            # Save the room in the World grid
            grid[y][x] = room

            # Connect the new room to the previous room
            if previous_room is not None:
                previous_room.connect_rooms(room, room_direction)
                room.connect_rooms(previous_room, opposite_direction[room_direction])

            # Update iteration variables
            previous_room = room
            room_count += 1

        # return grid of rooms
        return grid
