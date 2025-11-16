from django.http import HttpResponse


def task_index(request):
    return HttpResponse("Hello world")
