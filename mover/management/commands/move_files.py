from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from mover.async_backends import AsyncIOBackend


class Command(BaseCommand):
    help = 'Moving files between AWS Storages async with asyncio'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', dest='files', type=str)
        parser.add_argument('-r', '--restart_failed', dest='restart_failed', action='store_true', default=False)

    def handle(self, *args, **options):
        if not options.get('restart_failed') and not options.get('files'):
            raise CommandError('One of the options --restart_failed or --file must be provided')

        backend = AsyncIOBackend(settings.FROM, settings.TO)
        if options['restart_failed']:
            backend.restart_failed()
            print('Failed task has been restarted')
        else:
            files = list(map(str.strip, open(options['files'], 'r+').readlines()))
            backend.move_files(files)
