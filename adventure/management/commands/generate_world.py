from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
import util.world as world
import adventure.models as models

class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
#        parser.add_argument('total', type=int, help='Indicates the number of users to be created')
        pass

    def handle(self, *args, **kwargs):
        models.Room.objects.all().delete()
        # total = kwargs['total']
        # for i in range(total):
        #     User.objects.create_user(username=get_random_string(), email='', password='123')
        world_width = 10
        world_height = 10

        world.generate_rooms(world_width, world_height)
