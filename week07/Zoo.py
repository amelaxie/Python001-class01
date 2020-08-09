# _*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty


# 动物类
class Animal(metaclass=ABCMeta):
    def __init__(self, animal_type, animal_shape, animal_nature):
        self._type = animal_type
        self._shape = animal_shape
        self._nature = animal_nature
        if self.shape != "小" and self._type == "食肉":
            self._beast = True
        else:
            self._beast = False

    # 动物类型
    @property
    def type(self):
        return self._type

    # 动物体型
    @property
    def shape(self):
        return self._shape

    # 动物性格
    @property
    def nature(self):
        return self._nature

    # 动物是否属于凶猛动物
    @property
    def beast(self):
        return self._beast


# 猫类
class Cat(Animal):
    # 猫类有叫声
    hassound = True

    def __init__(self, name, animal_type, animal_shape, animal_nature):
        super().__init__(animal_type, animal_shape, animal_nature)
        self._name = name
        # 习性温顺适合当宠物
        if self.nature == "温顺":
            self._be_pet = True
        else:
            self._be_pet = False

    # 猫的名称
    @property
    def name(self):
        return self._name

    # 是否适合当宠物的属性
    @property
    def be_pet(self):
        return self._be_pet


# 动物园类
class Zoo():
    def __init__(self, name):
        # 动物名称
        self._name = name
        # 动物园拥有的动物
        self._animals = {}

    # 动物园名称
    @property
    def name(self):
        return self._name

    # 动物园拥有的动物
    @property
    def animals(self):
        return self._animals

    # 给动物园添加动物的方法
    def add_animal(self, obj):
        if id(obj) not in self._animals:
            self._animals[id(obj)] = obj
            print(f"Add success animal id:{id(obj)}, name:{obj.name}")
            setattr(self, obj.__class__.__name__, True)
        else:
            print(f"Add fail animal id:{id(obj)}, name:{obj.name} has already added")


if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    print(cat1.__dict__)
    print(Cat.__dict__)
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 看是否能重复添加同一个的动物
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = getattr(z, 'Cat')
    print(have_cat)
