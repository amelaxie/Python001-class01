from django.urls import path, re_path, register_converter
from . import views

urlpatterns = [
    # 测试页面
    path('', views.movie_comment),
    # 带搜索的信息展示
    path('search', views.search),
]
