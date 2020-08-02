from django.http import HttpResponse, request
from django.shortcuts import render
from .models import Book, T1
from django.db.models import Avg


#  from django.http import request

# Create your views here.
def index(request):
    return render(request, 'index.html', locals())


def books_short(request):
    ###  从models取数据传给template  ###
    shorts = T1.objects.all()
    # 评论数量
    counter = T1.objects.all().count()

    # 平均星级
    # star_value = T1.objects.values('n_star')
    star_avg = f" {T1.objects.aggregate(Avg('n_star'))['n_star__avg']:0.1f} "
    # 情感倾向
    sent_avg = f" {T1.objects.aggregate(Avg('sentiment'))['sentiment__avg']:0.2f} "

    # 正向数量
    queryset = T1.objects.values('sentiment')
    condtions = {'sentiment__gte': 0.5}
    plus = queryset.filter(**condtions).count()

    # 负向数量
    queryset = T1.objects.values('sentiment')
    condtions = {'sentiment__lt': 0.5}
    minus = queryset.filter(**condtions).count()

    # return render(request, 'douban.html', locals())
    return render(request, 'result.html', locals())


def year(request, year):
    msg = f"year is {year}"
    return HttpResponse(msg)


def cntid(request, cntid):
    '''
    @type request:request
    '''
    return HttpResponse(cntid)


def mp3(request, mp3name):
    return HttpResponse(mp3name)


def login(request, **kwargs):
    return HttpResponse((kwargs['userid'], kwargs['token']))
