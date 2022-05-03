# Generated by Django 3.2.5 on 2022-05-03 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useremotions',
            name='anger',
        ),
        migrations.RemoveField(
            model_name='useremotions',
            name='anxious',
        ),
        migrations.RemoveField(
            model_name='useremotions',
            name='joy',
        ),
        migrations.AddField(
            model_name='useremotions',
            name='angry',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='useremotions',
            name='happy',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='useremotions',
            name='hate',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='useremotions',
            name='neutral',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='useremotions',
            name='terrified',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='useremotions',
            name='sad',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='useremotions',
            name='surprised',
            field=models.IntegerField(default=0),
        ),
    ]
