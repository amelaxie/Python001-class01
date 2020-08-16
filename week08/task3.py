# 作业三
import timeit, functools, time
from functools import wraps


def timer(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        ret = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__}, {round(end_time - start_time, 2)}")
        return ret
    return inner


@timer
def mytest(var_a: int, var_b: str):
    print(f"var_a is {var_a}, var_b is {var_b}")
    time.sleep(3)
    print("done")


@timer
def mytest2(var_a: int):
    print(f"var_a is {var_a}")
    time.sleep(var_a)
    print("done")


def mymap_test(func, args):
    for arg in args:
        print(arg)
        func(arg)
