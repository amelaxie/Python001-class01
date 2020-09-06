from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.mylogin),
    path('logout/', views.mylogout),
    path('password/', views.password),
    path('info/', views.info),
]
