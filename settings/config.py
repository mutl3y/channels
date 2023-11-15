#!/usr/bin/env python3
import json

import yaml
from dataclasses import dataclass, field



debugging = False


def debug(*packed):
    if debugging:
        print(' ' * 4, *packed)


@dataclass
class Settings():
    data: dict = field(default_factory=dict)
    def save(self, path):
        with open(path, "wb") as f:
            yaml.safe_dump(self.data, f, encoding='utf-8')

    @classmethod
    def load(cls, file_name):
        my_data = {}
        with open(file_name, "rb") as f:
            my_data['data'] = yaml.safe_load(f)
        return cls(**my_data)

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
