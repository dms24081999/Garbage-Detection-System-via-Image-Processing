# Generated by Django 3.0.1 on 2020-01-11 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200111_1205'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GarbageData',
            new_name='GarbageDataModel',
        ),
    ]