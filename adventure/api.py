from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json
from util import world



# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))


def mapv(f, coll):
    return list(map(f, coll))


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.player_names(player_id)
    return JsonResponse({'uuid': uuid, 'name': player.user.username, 'title': room.title,
            'description': room.description, 'players': players}, safe=False)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()

    nextRoom = None
    for i, room_direction in enumerate(room.room_directions):
        if direction == room_direction:
            nextRoom = Room.objects.get(id=room.targets[i])


    if nextRoom is not None:
        player.currentRoom = nextRoom.id # uses id
        player.save()
        players = nextRoom.player_names(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)

        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})

        return JsonResponse({'name': player.user.username, 'title': nextRoom.title,
                            #'description': nextRoom.description,
                             'biome': nextRoom.biome,
                            'players': players, 'error_msg':""},
                safe=False)

    else:
        players = room.player_names(player_id)
        return JsonResponse({'name': player.user.username, 'title': room.title,
                            #'description': room.description,
                            'biome': room.biome,
                            'players': players,
                            'error_msg': "You cannot move that way."},
                safe=False)


@csrf_exempt
@api_view(["POST"])
def say(request):
    player = request.user.player
    room = player.room()
    data = json.loads(request.body)
    cm = ChatMessage.objects.create(message=data['message'], player=player, room=room)
    cm.save()

    return JsonResponse({'message': f'You said {cm.message}', 'error': ""}, safe=False, status=500)


@csrf_exempt
@api_view(["GET"])
def rooms(request):
    try:
        rooms = Room.objects.all()

        room_data = []
        for room in rooms:
            room_data.append(eval(str(room)))

        return JsonResponse({'data': room_data}, safe=False)
    except Exception as e:
        return JsonResponse({'error': f'{e}'},status=500)
        #    return JsonResponse({'data' : room_data}, safe=True, status=500)


@csrf_exempt
@api_view(['POST'])
def room_items(request):
    data = json.loads(request.body)
    room = Room.objects.get(id=data['room_id'])
    items = Item.objects.filter(room=room)

    return JsonResponse({'data': items}, safe=False, status=500)


@csrf_exempt
@api_view(['GET'])
def inventory(request):
    player = request.user.player
    items = Item.objects.filter(player=player)
    return JsonResponse({'data': mapv(get_json, items)}, safe=False, status=500)


@csrf_exempt
@api_view(['POST'])
def item(request):
    print('ITEM endpoint')

    data = json.loads(request.body)
    action = data['action']
    item_id = data['item_id']
    item = Item.objects.get(id=item_id)
    item_room = item.room

    player = request.user.player
    room = player.room()

    print(item)

    response = JsonResponse({'error': "Invalid Action"})

    # drop the item into the room
    if item_room != player.room:
        response = JsonResponse({'error': "Item and player are not in the same room."})
        pass
    elif action == 'drop':
        item.room = room
        item.player = None
        response = JsonResponse({'message': 'Dropped the item {item.name}'})
    # take an item from the room, must be in the same room as the item
    elif action == 'take':
        item.room = None
        item.player = player
        response = JsonResponse({'message': 'Picked up the item {item.name}'})

    item.save()
    return response

@csrf_exempt
@api_view(['GET'])
def room(request):
    player = request.user.player
    _room = player.room()
    messages = ChatMessage.objects.filter(room=_room)
    return JsonResponse({'room': eval(str(_room)), 'messages': mapv(get_json, messages)}, safe=False)


