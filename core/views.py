from django.http import HttpResponse


def home(response):
    return HttpResponse("<h1>Did it Work</h1>")


