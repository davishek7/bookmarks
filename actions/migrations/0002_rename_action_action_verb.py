# Generated by Django 3.2.1 on 2021-05-20 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='action',
            old_name='action',
            new_name='verb',
        ),
    ]
