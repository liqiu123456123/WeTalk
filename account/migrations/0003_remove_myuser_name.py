# Generated by Django 5.0.2 on 2024-02-13 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_myuser_file_myuser_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='name',
        ),
    ]