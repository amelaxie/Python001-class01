from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import TGoodsProcessed, TCommentProcessed
from django.contrib.auth.decorators import login_required
from django.utils import timezone as datetime
from django.core.serializers import serialize
from django.db.models import Avg
import json
from django.db import connection
from django.template.defaulttags import register


# 注册一个用于模板的获取字典值的函数
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


# SQL查询数据函数
def db_query(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        fields = cursor.description
        data_list = []
        for row in result:
            rowdict = {}
            for i in range(len(fields)):
                rowdict[fields[i][0]] = row[i]
            data_list.append(rowdict)
        return data_list
    except Exception as e:
        print(e)
        return None

#  获取排行信息函数
def get_goods_ranking():
    sql = 'select goods_id, name, comment_num from t_goods_processed  ORDER BY comment_num  desc limit 5'
    comment_ranking = db_query(sql)
    sql = """select goods_id,name ,round((worth /(worth + worthless))*100,2) as worth_rate from t_goods_processed where worth+worthless>10 ORDER BY worth_rate desc LIMIT 5"""
    worth_ranking = db_query(sql)
    sql = """select goods_id,name ,round((positive/(positive+neutral+negative))*100,2) as positive_rate from t_goods_processed where comment_num>10 ORDER BY positive_rate desc LIMIT 5"""
    positive_ranking = db_query(sql)
    return comment_ranking, worth_ranking, positive_ranking


#  获取品牌数量排行信息函数
def get_brand_summary():
    name_list = []
    data_list = []
    sql = """
    SELECT
        brand,
        count(brand) AS num
    FROM
        t_goods_processed
    GROUP BY
        brand
    ORDER BY
        num DESC
    """
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        # fields = cursor.description
        total_num = 0
        rank_total_num = 0
        i = 0
        for row in result:
            if i <= 6:
                name_list.append(row[0].split("/")[-1])
                data_list.append(row[1])
            total_num += row[1]
            rank_total_num += 0
            i += 1
    except:
        pass
    print(name_list)
    print(data_list)
    return name_list, data_list


# 首页
@login_required(login_url="/user/login")
def index(request):
    return render(request, 'index.html', {"user": request.user})


#  DashBoard 信息概览页面
@login_required(login_url="/user/login")
def console(request):
    dt = datetime.datetime.now() - datetime.timedelta(days=1)
    query_time = dt.strftime('%Y-%m-%d %H:%M:%S')   # 查询最近一天数据
    name_list, data_list = get_brand_summary()      # 获取前七大 品牌名称和数量，用于柱状图
    goods_num = TGoodsProcessed.objects.all().count()   # 统计商品数量
    comment_num = TCommentProcessed.objects.all().count()   # 统计评论数量
    type_num = TGoodsProcessed.objects.values("brand").distinct().count()   # 统计总品牌数量
    avg_price = f" {TGoodsProcessed.objects.aggregate(Avg('price'))['price__avg']:0.0f}"    # 评价价格
    comment_ranking, worth_ranking, positive_ranking = get_goods_ranking()      # 各大排名信息
    # print(comment_ranking)
    return render(request, 'console.html', locals())


# 显示商品信息页面
@login_required(login_url="/user/login")
def show_goods_page(request):
    keyword = request.GET.get('keyword')
    brand = request.GET.get('brand')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    if not keyword:
        keyword = ""
    if not brand:
        brand = ""
    if not start_time:
        start_time = ""
    if not end_time:
        end_time = ""
    return render(request, 'show_goods.html', locals())


# 显示评论信息页面
@login_required(login_url="/user/login")
def show_comment_page(request):
    keyword = request.GET.get('keyword')
    sentiment = request.GET.get('sentiment')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    if not keyword:
        keyword = ""
    if not sentiment:
        sentiment = ""
    if not start_time:
        start_time = ""
    if not end_time:
        end_time = ""
    return render(request, 'show_comment.html', locals())


# 商品详情页面
@login_required(login_url="/user/login")
def detail(request, goods_id):
    goods = TGoodsProcessed.objects.get(goods_id=goods_id)
    if goods:
        goods.url = '/static/img/' + "/".join(goods.url.split("/")[3:]) # 将图片地址换为本地地址
        return render(request, 'detail.html', locals())
    else:
        return HttpResponse("没有找到该商品")


#  获取评论信息接口
@login_required(login_url="/user/login")
def get_comment_info(request, comment_id):
    total_count = 0
    datalist = []
    try:
        start_time = request.GET.get('start_time')
        if not start_time:
            start_time = None
    except:
        start_time = None
    try:
        end_time = request.GET.get('end_time')
        if not end_time:
            end_time = None
    except:
        end_time = None
    try:
        sentiment = int(request.GET.get('sentiment'))
    except:
        sentiment = None
    try:
        keyword = request.GET.get('keyword')
    except:
        keyword = None
    try:
        goods_id = request.GET.get('goods_id')
    except:
        goods_id = None
    try:
        page = int(request.GET.get('page'))
        plimit = int(request.GET.get('limit'))
    except:
        page = 1
        plimit = 10
    sql = """
    SELECT
        c.comment_id,
        g.goods_id,
        g.name,
        g.brand,
        c.time,
        c.text,
        c.sentiment,
        c.positive_prob,
        c.negative_prob,
        c.confidence
    FROM
        t_goods_processed g,
        t_comment_processed c
    WHERE
        g.goods_id = c.goods_id"""
    if comment_id != "0":
        sql = sql + f" and c.comment_id={comment_id}"
    if goods_id is not None:
        sql = sql + f" and c.goods_id={goods_id}"
    if keyword is not None:
        sql = sql + f" and c.text like '%{keyword}%'"
    if sentiment is not None:
        sql = sql + f" and c.sentiment={sentiment}"
    if start_time is not None:
        sql = sql + f" and c.time>='{start_time}'"
    if end_time is not None:
        sql = sql + f" and c.time<='{end_time}'"
    sql = sql + " order by c.time desc"

    try:
        datalist = db_query(sql)
        start_num = (page - 1) * plimit
        end_num = page * plimit
        total_count = len(datalist)
        datalist = datalist[start_num:end_num]
    except:
        pass
    res_json = {
        "code": 0,
        "msg": "ok",
        "count": total_count,
        "data": datalist
    }
    return JsonResponse(res_json)


#  获取商品信息接口
@login_required(login_url="/user/login")
@csrf_exempt
def get_goods_info(request, goods_id):
    if request.method == 'GET':
        total_count = 0
        datalist = []
        try:
            start_time = datetime.datetime.strptime(request.GET.get('start_time'), '%Y-%m-%d %H:%M:%S')
        except:
            start_time = None
        try:
            end_time = datetime.datetime.strptime(request.GET.get('end_time'), '%Y-%m-%d %H:%M:%S')
        except:
            end_time = None
        try:
            brand = request.GET.get('brand')
        except:
            brand = None
        try:
            keyword = request.GET.get('keyword')
        except:
            keyword = None
        try:
            page = int(request.GET.get('page'))
            plimit = int(request.GET.get('limit'))
        except:
            page = 1
            plimit = 10
        queryset = TGoodsProcessed.objects.order_by("-time").all()
        if goods_id != "0":
            queryset = queryset.filter(goods_id=goods_id)
        if keyword is not None:
            queryset = queryset.filter(name__contains=keyword)
        if brand is not None:
            queryset = queryset.filter(brand__contains=brand)
        if start_time is not None:
            queryset = queryset.filter(time__gte=start_time)
        if end_time is not None:
            queryset = queryset.filter(time__lte=end_time)
        if len(queryset) > 0:
            data = serialize("json", queryset)
            json_data = json.loads(data)
            for info in json_data:
                info['fields']["goods_id"] = info['pk']
                datalist.append(info['fields'])
            # 检查请求页数据是否超出范围，如果正常则过滤出相关页数和条数
            datapages = float(len(datalist) / plimit + 1)
            if page >= datapages:
                return JsonResponse({"code:": 1, "msg": "没有查到符合要求的数据"})
            start_num = (page - 1) * plimit
            end_num = page * plimit
            total_count = len(datalist)
            datalist = datalist[start_num:end_num]
        res_json = {
            "code": 0,
            "msg": "ok",
            "count": total_count,
            "data": datalist
        }
        return JsonResponse(res_json)
