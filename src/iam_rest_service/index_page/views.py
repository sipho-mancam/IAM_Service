from django.shortcuts import render
from django.http import HttpResponse, Http404
# Create your views here.


def index(request):
    ua = request.META['HTTP_USER_AGENT']

    if not ('android' in ua.lower() or 'iphone' in ua):
        context = {}
        return render(request, 'index/index-desk.html', context)
    else:
        context = {}
        return render(request, 'index/index-mob.html', context)
