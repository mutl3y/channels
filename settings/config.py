#!/usr/bin/env python3
import json
import time

import yaml
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

debugging = False


def debug(*packed):
    if debugging:
        print(' ' * 4, *packed)


# @dataclass_json
@dataclass
class Settings():
    # data: dict = field(default_factory=dict)
    channels: list = field(init=True, default_factory=list)
    channel_groups: dict = field(init=True, default_factory=list)
    frequencies: dict = field(init=True, default_factory=dict)
    channel_types: list = field(init=True, default_factory=list)
    channel_headers: list = field(init=True, default_factory=list)

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

    # def read_config(self) -> None:
    #     """ read configuration """
    #     try:
    #         with open(self.config_file, "r") as file_object:
    #             self.config = yaml.safe_load(file_object)
    #         debug(f'parsed {self.config_file} ok')
    #         debug(f'found config sections for {list(self.config.keys())}')
    #     except Exception as e:
    #         debug(e)
    #         self.write_default_config()
    #
    # def write_default_config(self, config: dict = None) -> None:
    #     """ write supplied configuration """
    #     self.config = config
    #     self.write_config()
    #     debug(f'WriteDefaultConfig()')
    #
    # def write_config(self) -> None:
    #     """ write configuration """
    #     with open(self.config_file, "w") as file_object:
    #         yaml.safe_dump(self.config, file_object, encoding='utf-8')
    #     debug(f'Wrote config to {self.config_file}')
    #
    # # def enabled_frequencies(self) -> list:
    # #     t[i['hz'] for i in self.config['frequencies'] if i['enabled']]
    # #     return


def main():
    print('Being called directly, showing config')
    settings = Settings()
    print(settings.config)


if __name__ == '__main__':
    main()
