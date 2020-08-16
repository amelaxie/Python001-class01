# 作业二
import time


# 传入单个可迭代对象
def mymap(func, iterable_obj):
    print(iterable_obj)
    map_seq = []
    # 迭代将参数一个个传给函数执行并获取结果
    for obj in iterable_obj:
        map_seq.append(func(obj))
    return map_seq


# 传入多个可变参数
def mymap2(func, *seqs):
    print(*seqs)
    map_seq = []
    # 将多个参数组成一个可迭代对象
    for args in zip(*seqs):
        map_seq.append(func(*args))
    return map_seq


def test_task(number: int):
    time.sleep(number / 10)
    print(f"task {number} is done")
    return number / 10


# 内置map
res = map(test_task, [i for i in range(10, 20)])
print(list(res))

# 模拟map函数1
print(mymap(test_task, [i for i in range(10, 21)]))

# 模拟map函数2
print(mymap2(test_task, [i for i in range(10, 21)]))
