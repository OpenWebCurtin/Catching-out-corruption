from django.db import connection
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from website import models

class Command(BaseCommand):

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("DROP DATABASE openweb")
            cursor.execute("CREATE DATABASE openweb")
            # Other scripts e.g.
            #   python manage.py migrate
            # will handle the reconstruction.
