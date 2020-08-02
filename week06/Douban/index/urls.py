from django.urls import path, re_path, register_converter
from . import views, converters

register_converter(converters.IntConverter, 'year_num')

urlpatterns = [
    path('', views.index),
    path('book', views.books_short),
    path('<year_num:year>', views.year),
    path('<int:cntid>', views.cntid),
    path('<str:userid>/<str:token>', views.login),
    re_path('(?P<mp3name>[0-9]+).mp3', views.mp3, name='mp3url'),
]
