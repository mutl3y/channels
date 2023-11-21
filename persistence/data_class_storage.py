#!/usr/bin/env python3
import yaml
from dataclasses import dataclass, field, asdict


@dataclass
class SaveAsYaml:
    """will save a dataclass object as yaml

    annotates tuples to a list in a dict with key of _TUPLE
    """

    def save(self, path):
        with open(path, "wb") as f:
            c = asdict(self)
            d = c.copy()

            for k, v in c.items():
                if isinstance(v, tuple):
                    d[k] = {'_TUPLE': list(v)}
                if k != '_filename':
                    d[k] = c[k]
                    continue

            yaml.safe_dump(c, f, encoding='utf-8')
            del c, d

    @classmethod
    def load(cls, path, verbose=False):

        try:
            with open(path, "rb") as f:
                d = yaml.safe_load(f)
                if d is None:
                    return yaml.YAMLError(f'Could not parse yaml from {f.name}')
                if verbose:
                    print(f'Parsing {path}\n{d}')

        except Exception as e:
            return e

        my_model = {}
        for k in cls.__annotations__:
            # try:
            if k != '_filename':
                if isinstance(d[k], dict):
                    if '_TUPLE' in d[k].keys() and isinstance(d[k]['_TUPLE'], list):
                        my_model[k] = tuple(d[k]['_TUPLE'])
                else:
                    my_model[k] = d[k]
        # except TypeError as e:
        #     print(f'{k} not in {path}')
        #     continue
        return cls(**my_model)


if __name__ == '__main__':
    print('Persistence for dataclasses')

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
