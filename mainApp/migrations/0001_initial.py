# Generated by Django 3.2.5 on 2022-04-25 13:30

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
            name='Books',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('genre', models.CharField(max_length=50)),
                ('summary', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=400)),
                ('open_status', models.IntegerField(null=True)),
                ('date', models.DateTimeField(null=True)),
                ('image', models.ImageField(blank=True, upload_to='media/')),
            ],
        ),
        migrations.CreateModel(
            name='Emotion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('genre', models.CharField(max_length=50)),
                ('actors', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('release_year', models.CharField(max_length=50)),
                ('emotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.emotion')),
            ],
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('artist', models.CharField(max_length=50)),
                ('genre', models.CharField(max_length=50)),
                ('lyrics', models.CharField(max_length=2000)),
                ('emotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.emotion')),
            ],
        ),
        migrations.CreateModel(
            name='RecommendList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.diary')),
                ('rec_book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mainApp.books')),
                ('rec_movie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mainApp.movies')),
                ('rec_music', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mainApp.music')),
            ],
        ),
        migrations.CreateModel(
            name='EmotionPictures',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='')),
                ('emotion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.emotion')),
            ],
        ),
        migrations.AddField(
            model_name='diary',
            name='emotion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mainApp.emotion'),
        ),
        migrations.AddField(
            model_name='diary',
            name='user_id',
            field=models.ForeignKey(on_delete=models.SET('탈퇴한 사용자'), to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='books',
            name='emotion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.emotion'),
        ),
    ]
