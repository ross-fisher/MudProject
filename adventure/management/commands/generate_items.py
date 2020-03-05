from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
import util.items as items
import adventure.models as models

class Command(BaseCommand):
    help = 'Create random items'

    def add_arguments(self, parser):
#        parser.add_argument('total', type=int, help='Indicates the number of users to be created')
        pass

    def handle(self, *args, **kwargs):
        models.Item.objects.all().delete()
        items.generate_items()
