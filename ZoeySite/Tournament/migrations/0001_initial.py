# Generated by Django 2.1.2 on 2019-06-29 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('game', models.CharField(choices=[('Fortnite', 'Fortnite'), ('ApexLegends', 'ApexLegends'), ('BO4', 'BO4'), ('BF5', 'BF5'), ('R6S', 'R6S')], default='Fortnite', max_length=20)),
                ('deadTime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='IndividualTournament',
            fields=[
                ('basetournament_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Tournament.BaseTournament')),
                ('limitParticipant', models.IntegerField(default=4, max_length=100)),
                ('participant', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            bases=('Tournament.basetournament',),
        ),
        migrations.AddField(
            model_name='basetournament',
            name='organizer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]