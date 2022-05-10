import django
import os
import pandas as pd
from tqdm import tqdm
from mainApp.models import Music, Books, Movies, Emotion

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


path = 'dataAnalysis/data/'
movie = pd.read_csv(path+'movie_datasets.csv')
movie2 = pd.read_csv(path+'af_kmdb.csv')
book = pd.read_csv(path+'book_datasets.csv')
book2 = pd.read_csv(path+'naver_books.csv')
music = pd.read_csv(path+'music_datasets.csv')
music2 = pd.read_csv(path+'music_datasets_4000.csv')


def insert_music():
    music_instances = [Music(
          title=i['title'], artist=i['artists'], genre=i['genre'],
          lyrics=i['new_lyrics'],
          emotion=Emotion.objects.create(description=i['emotions']))
                              for i in tqdm(music.to_dict('records'))]
    Music.objects.bulk_create(music_instances)


def insert_book():
    book_instances = [Books(
          title=i['title'], author=i['author'], summary=i['description'],
          emotion=Emotion.objects.create(description=i['emotions']))
                        for i in tqdm(book.to_dict('records'))]
    Books.objects.bulk_create(book_instances)


def insert_movie():
    movie_instances = [Movies(
          title=i['title'], category=i['category'], genre=i['genre'],
          actors=i['actors'], description=i['content'], release_year=i['year'],
          emotion=Emotion.objects.create(description=i['emotions'])
                              )
                        for i in tqdm(movie.to_dict('records'))]
    Movies.objects.bulk_create(movie_instances)


insert_music()
insert_book()
insert_movie()
