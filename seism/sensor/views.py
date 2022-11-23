from django.shortcuts import render
from django.http import JsonResponse
from .models import Sens
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

import os


def startpage(request):
    return render(request, 'sensor/showsens.html')

def sensplot(request, namesens):
    return render(request, 'sensor/sensplot.html')

def sensprepere(request):
    bucket = request.headers['Referer'].split(sep='/', maxsplit=-1)[-2]
    token = 'Jwy6P1S9gVVnfgFyT65-ov_KQrQFycgz7k7nlPtEYREIRvLizX0I8GFIFFekB9yiAKZKycfR51kHDL9ic6XVow=='
    client = InfluxDBClient(url="http://localhost:8086", token=token, org="orn")
    query_api = client.query_api()
    
    labels = []
    data = []

    query = 'from(bucket: "' + str(bucket) + '")\
    |> range(start: -10000m)\
    |> filter(fn: (r) => r._measurement == "measurement1")'
    tables = query_api.query(query, org="orn")

    i = 0 
    for table in tables:
        for record in table.records:
            labels.append(i)
            data.append(record.values['_value'])
            i+=1

    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'name':bucket,
    })

def showsens(request):
    name = []
    user = []
    idx = []
    maxid = Sens.objects.latest('id').id

    if str(request.user) == 'roman':
        queryset = Sens.objects.all()
    else:
        queryset = Sens.objects.filter(ownuser = request.user)

    for entry in queryset:
        name.append(entry.name)
        user.append(str(entry.ownuser))
        idx.append(entry.id)

    if len(queryset) == 0:
        return JsonResponse(data={
        'user':[str(request.user)],
        'id':'netu',
        'maxid':maxid,
        })
    
    return JsonResponse(data={
        'name': name,
        'user': user,
        'id':idx,
        'maxid':maxid,
    })

@csrf_exempt
def ajaxpost(request):
    name = request.POST.get('name')
    user = User.objects.get(username = request.POST.get('user'))
    id = request.POST.get('id')
    Sens.objects.create(name = name, ownuser = user, id = id)
    return JsonResponse(data = {})

@csrf_exempt
def ajaxdel(request):
    name = request.POST.get('name')
    user = User.objects.get(username = request.POST.get('user'))
    id = request.POST.get('id')

    a = Sens.objects.get(id = id)
    a.delete()
    return JsonResponse(data = {})
