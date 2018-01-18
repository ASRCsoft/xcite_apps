from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

# main page with the map
def index(request):
    template = loader.get_template('hysplit/index.html')
    return HttpResponse(template.render())
