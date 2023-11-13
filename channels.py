import PySimpleGUI as sg
import settings.config as settings
import gui

channelList = []


class ChannelElement:
    def __init__(self, name: str, base: int, center: int, channel_type: str):
        super().__init__()
        self.name = name
        self.base = base
        self.center = center
        self.channel_type = channel_type

    def __str__(self) -> str:
        return f'{self.name}, {self.base}, {self.center}, {self.channel_type} '

    def keys(self) -> list:
        return list(self.__dict__)

    def values(self) -> list:
        return [self.name, self.base, self.center, self.channel_type]

    # def save(self, filename=):


def fpga_to_hz(var):
    return (6250 * int(var)) + 409600000


def hz_to_fpga(var):
    return int((var - 409600000) / 6250)


def default_config() -> dict:
    freq_list = [{'fpga': fpga, 'hz': fpga_to_hz(fpga), 'enabled': True} for fpga in
                 range(200, 201)]

    return dict(frequencies=freq_list, channel_types=['BULK UP', 'BULK DOWN', 'L2ACK', 'PRIORITY', 'RTS'], channels=[],
                channel_groups=[], towers=[], max_channels=48
                )


def enabled_frequencies(d: dict) -> list:
    if 'frequencies' not in d.keys():
        return []
    else:
        return [i['hz'] for i in d['frequencies'] if i['enabled']]


if __name__ == '__main__':
    app_settings = settings.Settings()
    app_settings.read_config()
    if isinstance(app_settings, object):
        print('Creating default config')
        app_settings.write_default_config(default_config())

    # todo test code
    h = ChannelElement('test', 1, 1, 'BULK UP')
    headers = [header.capitalize() for header in h.keys()]

    # del ch
    # print(headers)
    # exit(0)
    app_settings.config['channels'].append(h.values())
    app_settings.config['channels'].append(h.values())
    app_settings.config['channel_headers'] = headers
    app_settings.config['theme'] = 'bluePurple'
    app_settings.write_config()
    changed, config = gui.channels_window(app_settings.config)
    if changed:
        app_settings.write_default_config(config)
        del config
