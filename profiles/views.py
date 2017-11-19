from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Max, Min, F
from django.template import loader

# get some useful general utilities
import json, datetime

# get some stuff from the common app
from common.models import Lidar, Scan, Mwr, MwrScan
from profiles.models import Lidar5m
from profiles.graphs import get_plot


# main page with the graphs
def index(request):
    template = loader.get_template('profiles/index.html')
    return HttpResponse(template.render())

# data descriptions
def datasets(request):
    template = loader.get_template('profiles/datasets.html')
    return HttpResponse(template.render())


# get the date range of lidar5m data
def date_range(request):
    # get the earliest and most recent profiles
    times = Lidar5m.objects.aggregate(Min('time'), Max('time'))
    json_data = [times['time__min'].date(),
                 times['time__max'].date()]
    return JsonResponse(json_data, safe=False)


# get the available scans for a given time range
def available_scans(request):
    # get the times from the http request
    time_min_str = request.GET['time_min']
    time_min = datetime.datetime.strptime(time_min_str, '%Y-%m-%dT%H:%M:00.000Z')
    time_max_str = request.GET['time_max']
    time_max = datetime.datetime.strptime(time_max_str, '%Y-%m-%dT%H:%M:00.000Z')
    var = request.GET['var']
    if var in Mwr.mwr_vars:
        scans = MwrScan.objects \
                   .filter(mwrprofile__time__range=(time_min, time_max)) \
                   .distinct() \
                   .extra(select={'mode': "'NA'"}) \
                   .values('mode', scan_name=F('processor'), scan_id=F('id'), lidar_name=F('mwr__name'),
                           latitude=F('mwr__site__latitude'), longitude=F('mwr__site__longitude'),
                           site_name=F('mwr__site__name')) \
                   .order_by('lidar_name', 'scan_name')
    else:
        # put together the query
        scans = Scan.objects \
                    .filter(lidar5m__time__range=(time_min, time_max)) \
                    .distinct() \
                    .extra(select={'scan_name': "(xpath('//lidar_scan/@name', xml)::varchar[])[1]",
                                   'mode': "(xpath('//scan/@mode', xml)::varchar[])[1]"}) \
                    .values('scan_name', 'mode', scan_id=F('id'), lidar_name=F('lidar__name'),
                            latitude=F('lidar__site__latitude'), longitude=F('lidar__site__longitude'),
                            site_name=F('lidar__site__name')) \
                    .order_by('lidar_name')
        # (the crazy-looking xpath commands above get info from the
        # scan xml data)
    return JsonResponse(list(scans), safe=False)


# get a nice plot of some data
def plot(request):
    response = HttpResponse(content_type='image/png')
    # this is the binary plot data
    png = get_plot(request.GET)
    # write it to the response
    response.write(png)
    return response
