import dataclasses

import yaml

from persistence import data_class_storage


@dataclasses.dataclass
class Frequency:
    enabled: bool
    hz: int
    fpga: int = dataclasses.field(init=False)

    def __post_init__(self):
        self.fpga = int((self.hz - 409600000) / 6250)

    @property
    def _fpga(self):
        return int((self.hz - 409600000) / 6250)


@dataclasses.dataclass(order=True)
class Channel:
    name: str
    channel_type: str
    frequency: Frequency


@dataclasses.dataclass
class ConfigData(data_class_storage.SaveAsYaml):
    _filename: str = dataclasses.field(init=True, default='Config.yaml', hash=False, repr=False)
    channels: list = dataclasses.field(init=True, default_factory=list)
    channel_groups: list = dataclasses.field(init=True, default_factory=list)
    frequencies: list = dataclasses.field(init=True, default_factory=list)
    channel_types: list = dataclasses.field(init=True, default_factory=list)

    # channel_headers: list = dataclasses.field(init=True, default_factory=list)

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
                    if verbose:
                        print(f'{k}:{d[k]}')
                    my_model[k] = d[k]
        return cls(**my_model).fix_data_types()

    @property
    def filename(self):
        return self._filename

    def default_config(self, enabled_freq_tuple: tuple = (200, 210)):
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
        self.fix_data_types()
        self.save(self.filename)

    def fix_data_types(self):
        self.fix_frequency_list()
        self.fix_channel_lists()
        return self

    def fix_frequency_list(self):
        fixed_frequency_list = list()
        for f in self.frequencies:
            if isinstance(f, Frequency):
                fixed_frequency_list.append(f)
            else:
                fr = Frequency(hz=f['hz'], enabled=f['enabled'])
                fixed_frequency_list.append(fr)
        self.frequencies = fixed_frequency_list

    def fix_channel_lists(self):
        fixed_channel_list = list()
        for c in self.channels:
            if isinstance(c, Channel):
                fixed_channel_list.append(c)
            else:
                f = Frequency(hz=c['frequency']['hz'], enabled=c['frequency']['enabled'])
                ch = Channel(name=c['name'], channel_type=c['channel_type'], frequency=f)
                fixed_channel_list.append(ch)
        self.channels = fixed_channel_list

    def lookups(self) -> dict:
        print(self.enabled_frequencies())
        d = dict()
        d['hz'] = self.enabled_frequencies()
        d['channel_type'] = self.channel_types
        return d


def config_factory(filename='Config.yaml', verbose=False, enabled_freq_tuple=None) -> ConfigData:
    cfg = ConfigData.load(path=filename, verbose=verbose)

    if isinstance(cfg, FileNotFoundError):
        if verbose:
            print('Creating default Config')

        if isinstance(enabled_freq_tuple, tuple):
            cfg = ConfigData().default_config(enabled_freq_tuple=enabled_freq_tuple)
        else:
            cfg = ConfigData().default_config()

        cfg._fileName = filename

        cfg.save(filename)

        return cfg
    elif isinstance(cfg, yaml.YAMLError):
        print(f'Issues reading your Config file, check yaml syntax')
        return cfg
    else:
        if verbose:
            print(f'{cfg}')
            return cfg.fix_data_types()
