# Generated by Django 2.2.3 on 2019-08-15 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentSearch',
            fields=[
                ('search_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='search.Search')),
            ],
            bases=('search.search',),
        ),
        migrations.CreateModel(
            name='RelationSearch',
            fields=[
                ('search_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='search.Search')),
            ],
            bases=('search.search',),
        ),
    ]
