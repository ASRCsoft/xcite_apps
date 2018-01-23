from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from flux.plotly_graph import flux_plot
from plotly.utils import PlotlyJSONEncoder

# main page with the graphs
def index(request):
    template = loader.get_template('flux/index.html')
    return HttpResponse(template.render())

# get the json options for plotly graph
def plot(request):
    # get the earliest and most recent profiles
    # times = Lidar5m.objects.aggregate(Min('time'), Max('time'))
    # json_data = [times['time__min'].date(),
    #              times['time__max'].date()]
    # return JsonResponse(json_data, safe=False)
    
    # get the earliest and most recent profiles
    return JsonResponse(flux_plot(request), encoder=PlotlyJSONEncoder,
                        safe=False)
