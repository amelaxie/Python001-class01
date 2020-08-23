from django.urls import path, re_path, register_converter
from . import views

urlpatterns = [
    # 主页
    path('', views.index),
    # 登录页面
    path('login/', views.mylogin),
    # 登出
    path('logout/', views.myloginout),
]
