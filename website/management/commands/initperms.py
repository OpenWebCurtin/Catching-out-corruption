from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from website import models

class Command(BaseCommand):

    def handle(self, *args, **options):
        # p_ is permission.
        # g_ is group.

        P_UPLOAD = {
            'content_type': ContentType.objects.get(
                app_label='website',
                model='file'
            ),
            'codename': 'upload',
            'name': 'Can upload documents.'
        }
        P_DELETE = {
            'content_type': ContentType.objects.get(
                app_label='website',
                model='file'
            ),
            'codename': 'delete',
            'name': 'Can delete documents.'
        }
        P_RECOVER = {
            'content_type': ContentType.objects.get(
                app_label='website',
                model='file'
            ),
            'codename': 'recover',
            'name': 'Can recover documents.'
        }
        P_SEARCH = {
            'content_type': ContentType.objects.get(
                app_label='website',
                model='search'
            ),
            'codename': 'search',
            'name': 'Can search for documents.'
        }


        permissions_to_assign = [
            {
                'group_name': 'administrator',
                'permissions': [
                    P_UPLOAD,
                    P_DELETE,
                    P_RECOVER,
                    P_SEARCH
                ]
            },
            {
                'group_name': 'privileged user',
                'permissions': [
                    P_UPLOAD,
                    P_SEARCH
                ]
            },
            {
                'group_name': 'regular user',
                'permissions': []
            }
        ]

        # Assign upload permission to Privileged Users and Administrators.
        for item in permissions_to_assign:
            group, created = Group.objects.get_or_create(name=item['group_name'])
            permissions = item['permissions']
            for p_obj in permissions:
                permission = Permission.objects.get(
                    codename=p_obj['codename'],
                    content_type=p_obj['content_type']
                    #name=p_obj['name']
                )
                group.permissions.add(permission)
                permission.save()
            group.save()
