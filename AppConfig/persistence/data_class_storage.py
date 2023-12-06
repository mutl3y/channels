#!/usr/bin/env python3
import yaml
from dataclasses import dataclass, asdict


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
        # noinspection PyArgumentList
        return cls(**my_model)


if __name__ == '__main__':
    print('Persistence for dataclasses')
