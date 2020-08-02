学习笔记
# 新建Django工程：
F:\Python学习\myenv\env-crawl\Scripts\python3 manage.py startproject [工程名]
# 新建app
F:\Python学习\myenv\env-crawl\Scripts\python3 manage.py startapp [app名]


app 要加入工程中的settings.py 内的INSTALLED_APPS  才能更新models

# makemigrations 根据检测到的模型创建新的迁移。迁移的作用，更多的是将数据库的操作，以文件的形式记录下来，方便以后检查、调用、重做等等。
# 相当于在该app下建立 migrations目录，并记录下你所有的关于modes.py的改动，比如0001_initial.py。
F:\Python学习\myenv\env-crawl\Scripts\python3 manage.py makemigrations

# migrate 使数据库状态与当前模型集和迁移集同步。说白了，就是将对数据库的更改，主要是数据表设计的更改，在数据库中真实执行。例如，新建、修改、删除数据表，新增、修改、删除某数据表内的字段等等。
F:\Python学习\myenv\env-crawl\Scripts\python3 manage.py migrate

# 命令行
F:\Python学习\myenv\env-crawl\Scripts\python3 manage.py shell

# 启动django服务
F:\Python学习\myenv\env-crawl\Scripts\python3 manage.py runserver

# 从数据库反向生成模型文件
python3 manage.py inspectdb > models.py
managed = False，模型更新不会影响数据库表结构等信息
    class Meta:
        managed = False
        db_table = 't_movie_comment'

命令行测试模型的一些使用方法
from index.models import *
# 新建一个模型实例
n = Book()
n.name = '红楼梦'
n.url = '127.0.0.1'
n.desc = '石头记'
# save保存到数据库
n.save()

# 单条代码创建一条记录
Book.objects.create(name='三国演义',url='127.0.0.1',desc='三国')


# 模板测试
# 嵌套循环
<tbody>
{% for short in shorts %}
    <tr>
        <td>{{short.id}}</td>
        <td>
        	{% for _ in short.star|get_range %}
        	<b class="fa fa-star"></b>
        	{% endfor %}
        </td>
        <td>{{short.comment}}</td>
        <td>{{short.sentiment}}</td>
    </tr>
{% endfor %}
</tbody>


# head代码块
{% extends "base_layout.html" %} {% block title %}Welcome{% endblock %} 
{% load static %}
{% block head %}
    {{ block.super }}
    <link rel="stylesheet" href="{% static 'css/timeline.css' %}">
    <link rel="stylesheet" href="{% static 'css/morris.css' %}">
{% endblock %} 

# js代码块
{% block js %}
    {{ block.super }}
    <script src="{% static 'js/raphael-min.js' %}"></script>
    <script src="{% static 'js/morris.min.js' %}"></script>
    <script src="{% static 'js/morris-data.js' %}"></script>

{% endblock %}


