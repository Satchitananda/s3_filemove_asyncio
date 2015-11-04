from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from mover.async_backends import AsyncIOBackend


class Command(BaseCommand):
    help = 'Creating sample files at AWS Storage'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        backend = AsyncIOBackend(settings.FROM, settings.TO)
        files = ['sample/%s.txt' % i for i in range(options['count'])]
        backend.create_sample_files(files, 'Sample content')