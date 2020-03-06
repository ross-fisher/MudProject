from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url('rooms', api.rooms),
    url('room', api.room), # django seems to get confused if this is before rooms and a user is not logged in, will throw an error. (kinda dumb)
    url('item', api.item),
    url('inventory', api.inventory),
]
