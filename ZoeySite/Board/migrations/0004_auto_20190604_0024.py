# Generated by Django 2.1.2 on 2019-06-03 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Board', '0003_auto_20190604_0023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='board',
            new_name='topic',
        ),
    ]