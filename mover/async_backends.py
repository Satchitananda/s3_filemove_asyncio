import asyncio
import aiobotocore

from django.conf import settings

from mover.models import MoveRequest


class AsyncIOBackend(object):
    def __init__(self, from_, to):
        self.move_from = from_
        self.move_to = to

    @asyncio.coroutine
    def _create_sample_file(self, s3, filename, content):
        yield from s3.put_object(Bucket=self.move_from, Body=content, Key=filename)
        print(filename)

    @asyncio.coroutine
    def _move_file(self, s3, filename):
        if MoveRequest.objects.filter(filename=filename, status=MoveRequest.STATUS_RUNNING).count():
            print("There is already a running task for the  file %s" % filename)
            return True

        request = MoveRequest.objects.filter(filename=filename, status__in=[MoveRequest.STATUS_ERROR, MoveRequest.STATUS_QUEUED]).first()

        if not request:
            request = MoveRequest(filename=filename)

        request.status = MoveRequest.STATUS_RUNNING
        request.save()

        try:
            yield from s3.copy_object(Key=filename, Bucket=self.move_to, CopySource="%s/%s" % (self.move_from, filename))
            yield from s3.delete_object(Bucket=self.move_from, Key=filename)
            request.status = MoveRequest.STATUS_COMPLETED
            request.save()
        except Exception as e:
            print(e)
            request.status = MoveRequest.STATUS_ERROR
            request.save()
            return False
        return True

    def move_files(self, filenames):
        loop = asyncio.get_event_loop()
        session = aiobotocore.get_session(loop=loop)
        s3 = session.create_client('s3', aws_secret_access_key=settings.AWS_SECRET,
                                   aws_access_key_id=settings.AWS_KEY)
        return loop.run_until_complete(asyncio.wait([asyncio.Task(self._move_file(s3, fname)) for fname in filenames]))

    def restart_failed(self):
        files = list(MoveRequest.objects.filter(status=MoveRequest.STATUS_ERROR).values_list('filename', flat=True))
        return self.move_files(files)

    def create_sample_files(self, filenames, content):
        loop = asyncio.get_event_loop()
        session = aiobotocore.get_session(loop=loop)
        s3 = session.create_client('s3', aws_secret_access_key=settings.AWS_SECRET,
                                   aws_access_key_id=settings.AWS_KEY)
        return loop.run_until_complete(asyncio.wait([asyncio.Task(self._create_sample_file(s3, fname, content)) for fname in filenames]))
