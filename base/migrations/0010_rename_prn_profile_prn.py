# Generated by Django 3.2.12 on 2022-06-22 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20220622_0829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='prn',
            new_name='PRN',
        ),
    ]