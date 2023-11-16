#!/usr/bin/env python3
import yaml
from dataclasses import dataclass, field


class To_yaml:

    def save(self, path):
        with open(path, "wb") as f:
            yaml.safe_dump(self.__dict__, f, encoding='utf-8')

    @classmethod
    def load(cls, file_name):
        my_model = {}
        with open(file_name, "rb") as f:
            d = yaml.safe_load(f)
        for name in cls.__annotations__:
            my_model[name] = d[name]
        return cls(**my_model)

# class dataclass_persistence_decorator(object):
#     class Power(object):
#         def __init__(self, arg):
#             self._arg = arg
#
#         def __call__(self, a, b):
#             retval = self._arg(a, b)
#             return retval ** 2
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func()
#         print("Something is happening after the function is called.")
#     return wrapper


if __name__ == '__main__':
    print('Persistence for dataclasses')
