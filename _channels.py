import dataclasses
import yaml
import persistence.data_class_storage
import enum


# @dataclasses.dataclass
# class ChannelTypes(enum.Enum):
#     BULKUP = 'BULK UP', 1
#     BULKDOWN = 'BULK DOWN', 2
#     L2ACK = 'L2ACK', 3
#     PRIORITY = 'PRIORITY', 4
#     RTS = 'RTS', 5


@dataclasses.dataclass
class Frequency:
    enabled: bool
    fpga: int = dataclasses.field(init=False)
    hz: int

    def __post_init__(self):
        self.fpga = int((self.hz - 409600000) / 6250)


@dataclasses.dataclass(order=True)
class Channel():
    name: str
    channel_type: str
    frequency: Frequency


@dataclasses.dataclass
class ConfigData(persistence.data_class_storage.SaveAsYaml):
    _filename: str = dataclasses.field(init=True, default='config.yaml', hash=False, repr=False)
    channels: list = dataclasses.field(init=True, default_factory=list)
    channel_groups: list = dataclasses.field(init=True, default_factory=list)
    frequencies: list = dataclasses.field(init=True, default_factory=list)
    channel_types: list = dataclasses.field(init=True, default_factory=list)
    channel_headers: list = dataclasses.field(init=True, default_factory=list)

    @property
    def filename(self):
        return self._filename

    def default_config(self, **kwargs):
        if 'enabled_freq_tuple' not in kwargs.keys():
            enabled_freq_tuple: tuple = (200, 210)
        else:
            enabled_freq_tuple = kwargs['enabled_freq_tuple']

        self.frequencies = [Frequency(hz=int(6250 * int(fpga)) + 409600000, enabled=True) for fpga in
                            range(enabled_freq_tuple[0], enabled_freq_tuple[1])]
        self.channel_types = ['BULK UP', 'BULK DOWN', 'L2ACK', 'PRIORITY', 'RTS']
        self.channels = [Channel(frequency=self.frequencies[0], channel_type='BULK', name='test')]
        return self

    def enabled_frequencies(self) -> list:
        return [freq for freq in self.frequencies if freq.enabled]

    def update(self, d: dict):
        for k in self.__annotations__:
            if k in d.keys():
                setattr(self, k, d[k])
        self.save(self.filename)




def config_factory(filename='config.yaml', **kwargs) -> ConfigData:
    cfg = ConfigData().load(filename, kwargs)
    if isinstance(cfg, FileNotFoundError):
        if 'verbose' in kwargs.keys() and kwargs['verbose']:
            print('Creating default config')

        if 'enabled_freq_tuple' in kwargs.keys():
            cfg = ConfigData().default_config(enabled_freq_tuple=kwargs['enabled_freq_tuple'])
        else:
            cfg = ConfigData().default_config()

        cfg._fileName = filename

        cfg.save(filename)
    elif isinstance(cfg, yaml.YAMLError):
        if 'verbose' in kwargs.keys() and kwargs['verbose']:
            print(f'{cfg}')
        return None
    return cfg
