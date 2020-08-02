from django.http import HttpResponse, request
from django.shortcuts import render
from .models import TMovieComment
from django.db.models import Avg
from django.template.defaulttags import register


# 注册一个用于模板的range函数，模板中不支持python自带的range方法，需要自己实现
@register.filter
def get_range(value):
    return range(value)


# 带搜索功能的影片信息的view
def movie_comment(request):
    # 如果不带搜索关键字就展示所有超过三星的评论
    keyStr = request.GET.get('mykey')
    if keyStr is not None:
        shorts = TMovieComment.objects.filter(comment__icontains=keyStr)
    else:
        condtions = {'star__gt': 3}
        shorts = TMovieComment.objects.filter(**condtions)

    # 评论数量
    counter = TMovieComment.objects.all().count()

    # 平均星级
    star_avg = f" {TMovieComment.objects.aggregate(Avg('star'))['star__avg']:0.1f} "

    # 情感倾向
    sent_avg = f" {TMovieComment.objects.aggregate(Avg('sentiment'))['sentiment__avg']:0.2f} "

    # 正向数量
    queryset = TMovieComment.objects.values('sentiment')
    condtions = {'sentiment__gte': 0.5}
    plus = queryset.filter(**condtions).count()

    # 负向数量
    queryset = TMovieComment.objects.values('sentiment')
    condtions = {'sentiment__lt': 0.5}
    minus = queryset.filter(**condtions).count()

    return render(request, 'result.html', locals())


# 测试一个简单搜索页面
def search(request):
    return render(request, 'search2.html', locals())
