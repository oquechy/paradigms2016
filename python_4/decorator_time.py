import time
import sys

sys.setrecursionlimit(2000)


def timing(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print('-' * 25)
        print('time(sec) =', time.time() - start)
    return wrapper


def memoize(func):
    mem = dict()

    def wrapper(n):
        if n not in mem:
            mem[n] = func(n)
        return mem[n]
    return wrapper


@timing
def wiiii(a, b):
    print(a * b)


@timing
@memoize
def call_f(n):
    print(fib(n))


def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)


@timing
@memoize
def call_fact(n):
    print(fact(n))


@timing
def no_wrap_call_fact(n):
    print(fact(n))


def fact(n):
    if n == 1:
        return 1
    return n * fact(n - 1)


def stm(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class qqq:
    def __init__(self):
        self.a = 1

    @stm
    def sum(a, b):
        return a + 2 * b