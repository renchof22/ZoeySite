# Generated by Django 2.1.2 on 2019-06-03 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_user_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
