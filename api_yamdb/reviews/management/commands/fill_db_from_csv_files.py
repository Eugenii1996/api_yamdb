import csv
from django.core.management.base import BaseCommand
from reviews.models import Category


class Command(BaseCommand):
    help = 'import csv files into sqlite db'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, encoding='utf-8', newline='') as csv_file:
            data = csv.DictReader(csv_file, delimiter=',', quotechar='"')
            for row in data:
                print(row['id'], row['name'], row['slug'])
                Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
