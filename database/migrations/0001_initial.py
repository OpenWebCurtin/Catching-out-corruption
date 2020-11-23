# Generated by Django 2.2.6 on 2019-10-31 16:18

import database.uploadFile
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='agenda_items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agendaCode', models.CharField(max_length=200, unique=True)),
                ('agendaName', models.CharField(max_length=200)),
                ('wordCount', models.IntegerField()),
            ],
            options={
                'db_table': 'agenda_items',
            },
        ),
        migrations.CreateModel(
            name='attended',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'attended',
            },
        ),
        migrations.CreateModel(
            name='documents',
            fields=[
                ('documentName', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('documentDate', models.DateTimeField()),
                ('wordCount', models.IntegerField()),
                ('isMinute', models.BooleanField()),
                ('council', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'documents',
            },
        ),
        migrations.CreateModel(
            name='files',
            fields=[
                ('virtualName', models.CharField(max_length=50)),
                ('fileName', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('uploadDateTime', models.DateTimeField()),
                ('docFile', models.FileField(upload_to=database.uploadFile.uploadFile.fileUp)),
            ],
            options={
                'db_table': 'files',
            },
        ),
        migrations.CreateModel(
            name='is_within_nm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wordCount', models.IntegerField(null=True)),
                ('documentName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.documents')),
            ],
            options={
                'db_table': 'is_within_nm',
            },
        ),
        migrations.CreateModel(
            name='key_phrases',
            fields=[
                ('keyPhrase', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('phraseType', models.CharField(max_length=25)),
                ('attended', models.ManyToManyField(related_name='attendedKeyPhrases', through='database.attended', to='database.documents')),
                ('isWithinNM', models.ManyToManyField(through='database.is_within_nm', to='database.documents')),
            ],
            options={
                'db_table': 'key_phrases',
            },
        ),
        migrations.CreateModel(
            name='jobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobType', models.CharField(max_length=50)),
                ('jobStatus', models.CharField(max_length=50)),
                ('jobNumber', models.IntegerField()),
                ('jobCreation', models.DateTimeField()),
                ('startDateTime', models.DateTimeField()),
                ('completionDateTime', models.DateTimeField()),
                ('fileName', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='database.files')),
            ],
            options={
                'db_table': 'jobs',
                'unique_together': {('jobCreation', 'jobNumber')},
            },
        ),
        migrations.AddField(
            model_name='is_within_nm',
            name='keyPhrase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.key_phrases'),
        ),
        migrations.CreateModel(
            name='is_within',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wordCount', models.IntegerField(default=0)),
                ('agendaCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.agenda_items')),
                ('keyPhrase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.key_phrases')),
            ],
            options={
                'db_table': 'is_within',
                'unique_together': {('keyPhrase', 'agendaCode')},
            },
        ),
        migrations.AddField(
            model_name='attended',
            name='documentName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.documents'),
        ),
        migrations.AddField(
            model_name='attended',
            name='keyPhrase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendedKeyPhrases', to='database.key_phrases'),
        ),
        migrations.AddField(
            model_name='agenda_items',
            name='documentName',
            field=models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.CASCADE, to='database.documents'),
        ),
        migrations.AddField(
            model_name='agenda_items',
            name='isWithin',
            field=models.ManyToManyField(through='database.is_within', to='database.key_phrases'),
        ),
        migrations.AlterUniqueTogether(
            name='is_within_nm',
            unique_together={('keyPhrase', 'documentName')},
        ),
        migrations.CreateModel(
            name='is_from',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documentName', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='database.documents')),
                ('fileName', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='database.files')),
            ],
            options={
                'db_table': 'is_from',
                'unique_together': {('documentName', 'fileName')},
            },
        ),
        migrations.CreateModel(
            name='found_in',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agendaCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.agenda_items')),
                ('documentName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.documents')),
            ],
            options={
                'db_table': 'found_in',
                'unique_together': {('documentName', 'agendaCode')},
            },
        ),
        migrations.CreateModel(
            name='completes_with',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.files')),
                ('jobCreation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobCreatio', related_query_name='jobsC', to='database.jobs')),
                ('jobNumber', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='jobNumbe', related_query_name='jobN', to='database.jobs')),
            ],
            options={
                'db_table': 'completes_with',
                'unique_together': {('fileName', 'jobNumber', 'jobCreation')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='attended',
            unique_together={('keyPhrase', 'documentName')},
        ),
        migrations.AlterUniqueTogether(
            name='agenda_items',
            unique_together={('documentName', 'agendaCode')},
        ),
    ]