学习笔记

# auth_user 中创建账号
from django.contrib.auth.models import User
user = User.objects.create_user("amela", "amela@qq.com", "12345678")

# 需要登录认证的装饰器，可以指定跳转的登录地址
@login_required(login_url="/index/login")

# 集成的认证，登录，登出的方法
from django.contrib.auth import authenticate, login, logout

# 表单的使用
class MyLoginForm(forms.Form):
    # 表单用户名定义
    username = forms.CharField(label="用户名", min_length=5, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # 表单密码定义
    password = forms.CharField(label="密码", min_length=8, widget=forms.TextInput(attrs={'class': 'form-control', 'type': "password"}))
		# widget 可以自定义html相关属性 比如class，type等
		# min_length 最小长度
		# label 标签文字内容，可定义中文
		
# 在模板中使用表单
<form action="./" role="form" method="post">
<fieldset>
    {# 添加csrf token#}
    {% csrf_token %}
    {# 添加表单 #}
    {{ form }}
    {# 判断是否包含跳转参数，有则跟表单一起发送 #}
    {% if url %}
        <input name="next" type="hidden" value="{{ url }}">
    {% endif %}
    <input type="submit" class="btn btn-lg btn-success btn-block" value="登录">