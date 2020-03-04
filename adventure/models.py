from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# array fields must be rectangular (same size for each row)
from django.contrib.postgres.fields import ArrayField
import uuid
import json


def get_json(obj):
    data = obj.__dict__.copy()
    data.pop('_state')
    return data

tiles = ['nothing', 'grass']

room_width = 40
room_height = 40
room_size = room_width * room_height

def set_rectangle(tiles, start_x, start_y, width, height, tile_type):
    for y in range(start_y, start_y + height):
        for x in range(start_x, start_x + width):
            tiles[y*room_width + x] = tile_type
    return tiles




# def print

class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    # text [][]

    size = room_width * room_height
    tiles = ArrayField(models.IntegerField(default=0), size=size,
            default=lambda:( [0] * room_size))

    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)


    def generate_interior(self):
        set_rectangle(self.tiles, 5, 5, 10, 20, 1)
        self.save()

    def connectRooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        try:
            destinationroom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
            elif direction == "s":
                self.s_to = destinationRoomID
            elif direction == "e":
                self.e_to = destinationRoomID
            elif direction == "w":
                self.w_to = destinationRoomID
            else:
                print("Invalid direction")
                return
            self.save()

    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]




class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()

    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()


def get_a_room():
    r = Room.objects.all()[0]
    return r


def partition(array, n):
    for i in range(0, len(array), n):
        yield array[i:i+n]

    if i < len(array):
        yield array[i:]


def get_room_matrix(room):
    return partition(room.tiles, room_width)


if __name__ =='__main__':
    r = Room.objects.all()
    r.generate_interior()
    print(r.tiles[5:20])
    print(r.tiles[room_width+5:room_width+25])

