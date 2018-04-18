from django.core.management.base import BaseCommand, CommandError
from urlshortenerapp.models import Line


class Command(BaseCommand):
    help = 'Add words.txt in database'

    def handle(self, *args, **options):

        with open('words.txt') as file:
            self.stdout.write('Creating........')
            for words in file:
                Line.objects.create(text=words)

        self.stdout.write(self.style.SUCCESS('Task Successful !'))
