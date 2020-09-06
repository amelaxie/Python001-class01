from django.forms import Form, CharField, TextInput


class MyLoginForm(Form):
    # 表单用户名定义
    username = CharField(label="用户名", min_length=5,
                         widget=TextInput(attrs={'class': 'form-control'}))
    # 表单密码定义
    password = CharField(label="密码", min_length=6,
                         widget=TextInput(attrs={'class': 'form-control', 'type': "password"}))
