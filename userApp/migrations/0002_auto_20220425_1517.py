# Generated by Django 3.2.5 on 2022-04-25 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='users',
            name='full_name',
            field=models.CharField(max_length=100),
        ),
    ]
