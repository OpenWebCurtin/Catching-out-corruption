from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    def handle(self, *args, **options):

        # Parse the document.
        print("Parsing document: %s" % (str(args['filename'])))
