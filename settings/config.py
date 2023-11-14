#!/usr/bin/env python3
"""
    setting module
    usage:

    import settings
    settings = settings.Settings()


@author: Mark Heynes

"""

import yaml

debugging = False


def debug(*packed):
    if debugging:
        print(' ' * 4, *packed)


class Settings:
    """
        Settings class

    usage:
        settings=Settings(config_file="config.yaml")

    :return object: settings object
    """

    def __init__(self, config_file="config.yaml"):
        """ initialise and read configuration """
        self.config_file = config_file
        self.config = dict()
        self.read_config()

    def read_config(self) -> None:
        """ read configuration """
        try:
            with open(self.config_file, "r") as file_object:
                self.config = yaml.safe_load(file_object)
            debug(f'parsed {self.config_file} ok')
            debug(f'found config sections for {list(self.config.keys())}')
        except Exception as e:
            debug(e)
            self.write_default_config()


    def write_default_config(self, config: dict = None) -> None:
        """ write supplied configuration """
        self.config = config
        self.write_config()
        debug(f'WriteDefaultConfig()')

    def write_config(self) -> None:
        """ write configuration """
        with open(self.config_file, "w") as file_object:
            yaml.safe_dump(self.config, file_object, encoding='utf-8')
        debug(f'Wrote config to {self.config_file}')

    # def enabled_frequencies(self) -> list:
    #     t[i['hz'] for i in self.config['frequencies'] if i['enabled']]
    #     return
def main():
    print('Being called directly, showing config')
    settings = Settings()
    print(settings.config)


if __name__ == '__main__':
    main()
