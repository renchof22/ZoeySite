# Generated by Django 2.2.5 on 2019-10-13 08:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Board', '0003_auto_20191009_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='last_updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]