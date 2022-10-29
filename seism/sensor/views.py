from django.shortcuts import render
from django.http import JsonResponse
from .models import Sens
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

def startpage(request):
    return render(request, 'sensor/showsens.html')

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
