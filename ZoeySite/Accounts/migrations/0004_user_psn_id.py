# Generated by Django 2.1.2 on 2019-06-20 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_auto_20190604_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='psn_id',
            field=models.CharField(default='test', max_length=30),
            preserve_default=False,
        ),
    ]
