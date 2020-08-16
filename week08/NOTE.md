学习笔记

list(列表) 会拷贝列表而不是引用
列表[:] 代表整个列表，切片操作也是会复制的
import copy
copy.copy() 浅拷贝 			子容器只会复制引用，不会复制值
copy.deepcopy() 深拷贝  包括子容器也会复制一份至内存

class kls1(object):
	def __call__(self):
		return 123

__call__ 用此魔术方法后，类实例也可以被调用

Python作用域遵循 LEGB 规则
L local 函数内部名字空间
E Enclosing function local 外部嵌套函数的名字空间 例如 closure
G Global(module)	函数定义所在模块（文件）的名字空间
B Builtin(Python)  Python内置模块的名字空间

动态参数与处理，关注传入参数的对象类型，字典与序列类型。
    *args 序列参数
    **kwargs 关键字参数

装饰器其实是一种设计模式，不改变原有属性，而是去增加属性。增强而不改变原有函数。
强调函数的定义态而不是运行态，底层是通过闭包实现的。
也就是说 装饰器函数写完，装饰到被装饰器函数上的时候，已经被执行。被装饰器函数在定义的时候就已经被装饰器改变了。