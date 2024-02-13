# Generated by Django 5.0.2 on 2024-02-12 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_myuser_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailValid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=32)),
                ('email_address', models.EmailField(max_length=254)),
                ('times', models.DateTimeField()),
            ],
        ),
    ]