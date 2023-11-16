import persistence.data_class_storage as persistence
import gui, utils
from dataclasses import dataclass, field, asdict, astuple
from persistence.data_class_storage import To_yaml

@dataclass
class Frequency:
    enabled: bool
    fpga: int = field(init=False) #, repr=False)
    hz: int

    def __post_init__(self):
        self.fpga = int((self.hz - 409600000) / 6250)


@dataclass
class Channel(dict):
    name: str
    frequency: Frequency
    channel_type: str


@dataclass
class ConfigData(To_yaml):
    # data: dict = field(default_factory=dict)
    channels: list = field(init=True, default_factory=list)
    channel_groups: dict = field(init=True, default_factory=list)
    frequencies: list = field(init=True, default_factory=list)
    channel_types: list = field(init=True, default_factory=list)
    channel_headers: list = field(init=True, default_factory=list)

    def default_config(self):
        # h = Channel('test', 1, 'BULK UP')
        enabled_freq_tuple = (200, 210)
        self.frequencies = [Frequency(hz=int(6250 * int(fpga)) + 409600000, enabled=True) for fpga in
                            range(enabled_freq_tuple[0], enabled_freq_tuple[1])]
        self.channel_types = ['BULK UP', 'BULK DOWN', 'L2ACK', 'PRIORITY', 'RTS']
        self.channels = [{'center': 410850000, 'ch_type': 'BULK', 'name': 'test'}]

    def enabled_frequencies(self) -> list:
        return [freq for freq in self.frequencies if freq.enabled]
        # if 'frequencies' not in d.keys():
        #     return []
        # else:
        #     return [i['hz'] for i in d['frequencies'] if i['enabled']]
# @classmethod
#
#     return True
# (
# dict(frequencies=freq_list, channel_types=['BULK UP', 'BULK DOWN', 'L2ACK', 'PRIORITY', 'RTS'],
# channels=[], channel_groups=[], towers=[], max_channels=48, theme='bluePurple',
# channel_headers=headers,
# ))





def main():
    app_settings = settings.To_yaml()
    # app_settings.read_config()
    if isinstance(app_settings, object):
        print('Creating default config')

    # force overwrite of configuration
    app_settings.data = default_config()
    # app_settings.write_default_config(default_config())

    ch = Channel('test', 410850000, 'BULK UP')
    # print('item to add ', h.values())
    # print(ch.__dict__)
    # time.sleep(10)
    # exit(1)
    app_settings.channels.append(ch.__dict__)
    app_settings.channels.append(ch.__dict__)
    app_settings.channels.append(ch.__dict__)
    app_settings.save('config.yaml')

    changed, config = gui.channels_window(app_settings)
    app_settings.save('config.yaml')
    del config


if __name__ == '__main__':
    main()
