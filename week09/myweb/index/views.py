from django.http import HttpResponse, request
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .form import MyLoginForm
from django.contrib.auth import authenticate, login, logout
import datetime


# Create your views here.

# 测试view视图
@login_required(login_url="/index/login")
def test(request):
    nowtime = datetime.datetime.now()
    msg = f"nowtime is {nowtime}"
    return HttpResponse(msg)


# 首页view视图
@login_required(login_url="/index/login")
def index(request):
    return render(request, "index.html")


# 登录页面视图
def mylogin(request):
    # get方法为登录页面
    if request.method == "GET":
        next_url = request.GET.get('next')
        login_form = MyLoginForm()
        if next_url:
            login_form.next = next_url
        return render(request, 'login.html', {"form": login_form, "url": next_url})
    # post方法为验证登录请求
    elif request.method == "POST":
        login_form = MyLoginForm(request.POST)
        # 判断是否带有跳转参数
        if "next" in request.POST:
            next_url = request.POST['next']
        else:
            next_url = "/"
        # 读取表单参数并验证，验证后保持登录
        if login_form.is_valid():
            login_data = login_form.cleaned_data
            user = authenticate(username=login_data['username'], password=login_data['password'])
            if user:
                login(request, user)
                return redirect(next_url)
        return render(request, 'login.html', {"form": login_form, "url": next_url, "msg": "用户名或密码错误"})


# 登出
def myloginout(request):
    #  登出
    logout(request)
    # 返回首页
    return redirect("/")
