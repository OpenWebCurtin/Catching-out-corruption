from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from website.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):

        USERS = [
            {
                'username': 'admin',
                'password': 'admin',
                'super': True,
                'groups': [
                    'administrator'
                ]
            },
            {
                'username': 'privileged',
                'password': 'privileged',
                'super': False,
                'groups': [
                    'privileged user'
                ]
            },
            {
                'username': 'regular',
                'password': 'regular',
                'super': False,
                'groups': [
                    'regular user'
                ]
            }
        ]

        # Assign upload permission to Privileged Users and Administrators.
        for item in USERS:
            user = User.objects.create_user(
                item['username'],
                password=item['password']
            )
            user.is_superuser=item['super']

            for group_name in item['groups']:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
                group.save()
            user.save()
