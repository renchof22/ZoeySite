# Generated by Django 2.2.5 on 2019-10-09 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Board', '0002_auto_20191008_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='tags',
            field=models.ManyToManyField(blank=True, to='Board.Tag'),
        ),
    ]
