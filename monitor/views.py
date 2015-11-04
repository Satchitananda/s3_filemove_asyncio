from django.http import JsonResponse

from django.template.response import TemplateResponse

from mover.models import MoveRequest


def index(request):
    if request.is_ajax():
        return JsonResponse([[r.id, r.filename, r.get_status_display()] for r in MoveRequest.objects.all()], safe=False)

    context = {
        'move_requests': MoveRequest.objects.all()
    }
    return TemplateResponse(request, 'index.html', context)
