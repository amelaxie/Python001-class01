from django.urls import path, include
from . import views

urlpatterns = [
    # dashboard 信息概览页面
    path('console/', views.console),
    # 商品信息查询页面
    path('show_goods/', views.show_goods_page),
    # 评论信息查询页面
    path('show_comment/', views.show_comment_page),
    # 商品详情页面
    path('detail/<str:goods_id>/', views.detail),
    # 商品信息接口
    path('api/get_goods/<str:goods_id>/', views.get_goods_info),
    # 评论信息接口
    path('api/get_comment/<str:comment_id>/', views.get_comment_info),
]
