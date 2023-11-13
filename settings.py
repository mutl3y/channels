#!/usr/bin/env python3
"""
    setting module
    usage:

    import settings
    settings = settings.Settings()


@author: Mark Heynes

"""

import yaml
from docpie import docpie

debugging = False


def debug(*packed):
    if debugging:
        print('        ', *packed)


def fpga_to_hz(var):
    return (6250 * int(var)) + 409600000


def hz_to_fpga(var):
    return int((var - 409600000) / 6250)


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
                self.config = yaml.load(file_object, Loader=yaml.SafeLoader)
            debug(f'parsed {self.config_file} ok')
            debug(f'found config sections for {list(self.config.keys())}')
        except Exception as e:
            debug(e)
            self.write_default_config()

    def write_default_config(self, fpga_range=(200, 300), enabled=False) -> None:
        """ write default configuration """
        freq_list = [{'fpga': fpga, 'hz': fpga_to_hz(fpga), 'enabled': enabled} for fpga in
                     range(fpga_range[0], fpga_range[1])]

        self.config["frequencies"] = freq_list
        self.config['ch_types'] = ['BULK UP', 'BULK DOWN', 'L2ACK', 'PRIORITY', 'RTS']
        self.config["channels"] = {}
        self.config["channel_groups"] = []
        self.config["towers"] = {}
        self.write_config()
        debug(f'WriteDefaultConfig()')

    def write_config(self) -> None:
        """ write configuration """
        with open(self.config_file, "w") as file_object:
            yaml.dump(self.config, file_object)
        debug(f'Wrote config to {self.config_file}')

    def enabled_frequencies(self) -> list:
        return [i['hz'] for i in self.config['frequencies'] if i['enabled']]


def main():
    settings = Settings()
    settings.write_default_config(fpga_range=(200, 202), enabled=True)
    print(settings.config)


if __name__ == '__main__':
    args = docpie(__doc__)
    print(args)
    main()
