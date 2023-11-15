import settings.config as settings
import gui, utils
from dataclasses import dataclass,field

@dataclass
class Channel:
    name: str
    center: int
    channel_type: str
    fpga: int = field(init=False) #, repr=False)
    def __post_init__(self):
        self.fpga = ((6250 * self.center) + 409600000)


def default_config() -> dict:
    # todo test code
    h = Channel('test', 1, 'BULK UP')
    headers = [header.capitalize() for header in h.__dict__.keys()]
    freq_list = [{'fpga': fpga, 'hz': utils.fpga_to_hz(fpga), 'enabled': True} for fpga in
                 range(200, 202)]

    return dict(frequencies=freq_list, channel_types=['BULK UP', 'BULK DOWN', 'L2ACK', 'PRIORITY', 'RTS'],
                channels=[], channel_groups=[], towers=[], max_channels=48, theme='bluePurple',
                channel_headers=headers,
                )


def enabled_frequencies(d: dict) -> list:
    if 'frequencies' not in d.keys():
        return []
    else:
        return [i['hz'] for i in d['frequencies'] if i['enabled']]


def main():
    app_settings = settings.Settings()
    # app_settings.read_config()
    if isinstance(app_settings, object):
        print('Creating default config')

    # force overwrite of configuration
    app_settings.data = default_config()
    # app_settings.write_default_config(default_config())

    ch = Channel('test', 1, 'BULK UP')
    # print('item to add ', h.values())
    # print(ch.__dict__)
    # time.sleep(10)
    # exit(1)
    app_settings.channels.append(ch.__dict__)
    # app_settings.data['channels'].append(ch.__dict__.items())
    print(app_settings.channels)
    app_settings.save('config.yaml')
    l = app_settings.channels
    print(l)

    changed, config = gui.channels_window(app_settings.__dict__)
    app_settings.save('config.yaml')
    del config


if __name__ == '__main__':
    main()
