# Generated by Django 5.0.2 on 2024-02-12 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=100, verbose_name='邮箱'),
        ),
    ]
