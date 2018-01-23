from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader


# main page with the graphs
def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())
