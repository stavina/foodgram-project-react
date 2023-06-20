import csv

from django.conf import settings
from django.core.management import BaseCommand
from recipes.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title)
from users.models import User

TABLES = {
    Category: 'category.csv',
    Comment: 'comments.csv',
    Genre: 'genre.csv',
    GenreTitle: 'genre_title.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    User: 'users.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, csv_f in TABLES.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{csv_f}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(
                    model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Импорт завершен!'))
