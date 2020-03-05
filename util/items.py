from adventure.models import Room, Item
import random

items = [
dict(name="Sword", description="Sharp"),
dict(name="Axe", description="Sharp"),
dict(name="Potion", description="Bitter"),
dict(name="Gold", description="Shiny"),
dict(name="Roast", description="Tasty"),
dict(name="Cape", description="Styleish"),
]


def generate_items():
    rooms = list(Room.objects.all())
    print(rooms)
    room_sample = random.sample(rooms, k=50) # sample 50 rooms
    for room in room_sample:
        item_data = random.choice(items)
        item = Item(name=item_data['name'], description=item_data['description'])
        item.room = room
        item.save()


