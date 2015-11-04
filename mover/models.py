from django.db import models


class MoveRequest(models.Model):
    STATUS_QUEUED = 0
    STATUS_RUNNING = 1
    STATUS_COMPLETED = 2
    STATUS_ERROR = 3

    StatusChoices = (
        (STATUS_QUEUED, 'In queue'),
        (STATUS_RUNNING, 'Running'),
        (STATUS_COMPLETED, 'Success'),
        (STATUS_ERROR, 'Error')
    )

    status = models.IntegerField(u'Status', choices=StatusChoices)
    filename = models.CharField(u'File name', max_length=1000)

    class Meta:
        ordering = ('-pk',)
