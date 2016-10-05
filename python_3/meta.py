import re

class MyMeta(type):
    def __new__(cls, name, bases, dct):
        upd_regex = dict((name, re.compile(value)) if name == 'regex' else (name, value) for name, value in dct.items())
        return super().__new__(cls, name, bases, upd_regex)

class a(metaclass=MyMeta):
    regex = "a+b"
