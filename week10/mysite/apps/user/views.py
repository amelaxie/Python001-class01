from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .form import MyLoginForm


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
def mylogout(request):
    #  登出
    logout(request)
    # 返回登录页
    return redirect("/")


# 用户信息展示，暂未实现修改功能
def info(request):
    return render(request, "info.html")


# 用户改密码，暂未实现修改功能
def password(request):
    return render(request, "password.html")
