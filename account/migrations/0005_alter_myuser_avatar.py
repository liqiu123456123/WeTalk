# Generated by Django 5.0.2 on 2024-02-14 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_myuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars\\0.png', null=True, upload_to='avatars/'),
        ),
    ]
