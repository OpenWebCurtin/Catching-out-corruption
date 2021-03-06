# Generated by Django 2.2.6 on 2019-10-31 16:18

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AsyncJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField()),
                ('status', models.IntegerField(choices=[(0, 'Unprocessed'), (1, 'Finished'), (2, 'Error'), (3, 'Unsupported')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.CharField(max_length=128)),
                ('occurs_total', models.IntegerField(default=0)),
                ('occurs_agenda_items', models.IntegerField(default=0)),
                ('normalised_score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=128)),
            ],
            options={
                'permissions': [('upload', 'Can upload documents using the PDF upload service.'), ('delete', 'Can delete documents using the file deletion service.'), ('recover', 'Can recover deleted documents using the file recovery service.')],
            },
        ),
        migrations.CreateModel(
            name='FileDeletionRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.CharField(max_length=128)),
                ('delete_by', models.IntegerField(choices=[(0, 'Delete files by filename.'), (1, 'Delete files by uploader.')], default=0)),
                ('target_file', models.CharField(blank=True, max_length=128, null=True)),
                ('target_uploader', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FileRecoveryRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.CharField(max_length=128)),
                ('recover_by', models.IntegerField(choices=[(0, 'Recover files by filename.'), (1, 'Recover files by uploader.')], default=0)),
                ('target_file', models.CharField(blank=True, max_length=128, null=True)),
                ('target_uploader', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KeyPhraseOptionSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_phrase', models.CharField(blank=True, default='', max_length=128)),
                ('key_phrase_type', models.IntegerField(choices=[(0, 'Any keyword type'), (1, 'Councillor name'), (2, 'Person name'), (3, 'Business name'), (4, 'Property address')], default=0, null=True)),
                ('key_phrase_importance', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrivilegeModification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.CharField(max_length=128)),
                ('target_user', models.CharField(max_length=128)),
                ('target_group', models.CharField(choices=[('regular user', 'Regular user'), ('privileged user', 'Privileged user'), ('administrator', 'Administrator')], default=0, max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='RelationResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kp1', models.CharField(max_length=128)),
                ('kp2', models.CharField(max_length=128)),
                ('kp3', models.CharField(max_length=128)),
                ('kp4', models.CharField(max_length=128)),
                ('kp5', models.CharField(max_length=128)),
                ('document', models.CharField(blank=True, default='', max_length=128)),
                ('agenda_item_file', models.CharField(blank=True, default='', max_length=128)),
                ('agenda_item', models.CharField(blank=True, default='', max_length=128)),
                ('description', models.CharField(blank=True, default='', max_length=128)),
                ('search_type', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_by', models.IntegerField(choices=[(0, 'Search by relation'), (1, 'Search by document')], default=0)),
                ('search_t', models.IntegerField(choices=[(0, 'Search minutes'), (1, 'Search non-minutes')], default=0)),
                ('fbm', models.BooleanField(default=False)),
                ('fbm_filename', models.CharField(blank=True, default='', max_length=128)),
                ('fbm_uploader', models.CharField(blank=True, default='', max_length=128)),
                ('fbm_upload_date_start', models.DateField(null=True)),
                ('fbm_upload_date_end', models.DateField(null=True)),
                ('fbc', models.BooleanField(default=False)),
                ('fbc_council', models.CharField(blank=True, default='', max_length=128)),
                ('fbc_publish_date_start', models.DateField(null=True)),
                ('fbc_publish_date_end', models.DateField(null=True)),
                ('key_phrase1', models.CharField(blank=True, default='', max_length=128)),
                ('key_phrase2', models.CharField(blank=True, default='', max_length=128)),
                ('key_phrase3', models.CharField(blank=True, default='', max_length=128)),
                ('key_phrase4', models.CharField(blank=True, default='', max_length=128)),
                ('key_phrase5', models.CharField(blank=True, default='', max_length=128)),
                ('key_phrase_type1', models.IntegerField(choices=[(0, 'Any keyword type'), (1, 'Councillor name'), (2, 'Person name'), (3, 'Business name'), (4, 'Property address')], default=0, null=True)),
                ('key_phrase_type2', models.IntegerField(choices=[(0, 'Any keyword type'), (1, 'Councillor name'), (2, 'Person name'), (3, 'Business name'), (4, 'Property address')], default=0, null=True)),
                ('key_phrase_type3', models.IntegerField(choices=[(0, 'Any keyword type'), (1, 'Councillor name'), (2, 'Person name'), (3, 'Business name'), (4, 'Property address')], default=0, null=True)),
                ('key_phrase_type4', models.IntegerField(choices=[(0, 'Any keyword type'), (1, 'Councillor name'), (2, 'Person name'), (3, 'Business name'), (4, 'Property address')], default=0, null=True)),
                ('key_phrase_type5', models.IntegerField(choices=[(0, 'Any keyword type'), (1, 'Councillor name'), (2, 'Person name'), (3, 'Business name'), (4, 'Property address')], default=0, null=True)),
                ('key_phrase_importance1', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('key_phrase_importance2', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('key_phrase_importance3', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('key_phrase_importance4', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('key_phrase_importance5', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
            ],
            options={
                'permissions': [('search', 'Can search using the document search feature.')],
            },
        ),
        migrations.CreateModel(
            name='AsyncJobType',
            fields=[
                ('job_base', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='website.AsyncJob')),
            ],
        ),
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('filename', models.CharField(blank=True, default='', max_length=128)),
                ('type', models.IntegerField(choices=[(0, 'Public minutes document.'), (1, 'Public non-minutes document.'), (2, 'Private non-minutes document.')], default=0)),
                ('document_category', models.CharField(default='generic', max_length=128)),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecoveryRequestItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.FileRecoveryRequest')),
                ('target_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.UploadedFile')),
            ],
        ),
        migrations.CreateModel(
            name='DeletionRequestItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.FileDeletionRequest')),
                ('target_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.UploadedFile')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessingJob',
            fields=[
                ('asyncjobtype_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='website.AsyncJobType')),
                ('file_name', models.CharField(max_length=128)),
            ],
            bases=('website.asyncjobtype',),
        ),
        migrations.CreateModel(
            name='FileRecoveryJob',
            fields=[
                ('asyncjobtype_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='website.AsyncJobType')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.FileRecoveryRequest')),
            ],
            bases=('website.asyncjobtype',),
        ),
        migrations.CreateModel(
            name='FileDeletionJob',
            fields=[
                ('asyncjobtype_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='website.AsyncJobType')),
                ('scheduled_time', models.FloatField()),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.FileDeletionRequest')),
            ],
            bases=('website.asyncjobtype',),
        ),
    ]
