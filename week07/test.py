# _*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty


class Animal(metaclass=ABCMeta):
    # 动物类型
    @property
    @abstractmethod
    def type(self):
        pass

    # 动物体型
    @property
    @abstractmethod
    def shape(self):
        pass

    # 动物性格
    @property
    @abstractmethod
    def nature(self):
        pass

    # 动物是否属于凶猛动物
    @property
    @abstractmethod
    def nature(self):
        pass


class Test(Animal):
    def __init__(self, type):
        self._type = type

    @property
    def type(self):
        return self._type


print(Test("small").get_type)
