# Generated by Django 5.0.2 on 2024-02-13 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_emailvalid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='photo',
            field=models.FileField(blank=True, upload_to='f_test/', verbose_name='头像'),
        ),
    ]
