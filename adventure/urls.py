from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url('rooms', api.rooms),
    url('item', api.item),
    url('inventory', api.inventory),
    url('room_items', api.room_items),
]
