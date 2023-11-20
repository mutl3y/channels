import os
from unittest import TestCase
from data_class_storage import *
import tempfile


def cleanup(file):
    try:
        file.close()
        os.remove(file.name)
    except WindowsError as e:
        if e.winerror != 2:
            print(f'issues deleting {file.name}')
        pass

class Test(TestCase):
    def test_saving_diataclass_as_yaml(self):
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)

        @dataclass
        class config(SaveAsYaml):
            channel_types: list = field(default_factory=list)
            channels: list = field(default_factory=list)
            frequencies: list = field(default_factory=list)
            towers: dict = field(default_factory=dict)

            def __post_init__(self):
                self.channels: list = [{'center': 410850000, 'ch_type': 'BULK', 'name': 'test'}]
                self.frequencies: list = [{'enabled': True, 'fpga': fpga, 'hz': (6250 * int(fpga)) + 409600000} for fpga in
                                     range(200, 210)]

        enabled_freq_tuple = (200, 210)
        s = config()
        s.save(configfile.name)

        # load saved dataclass from file and compare
        t = config().load(configfile.name, verbose=True)
        for k in s.__dict__.keys():
            self.assertEqual(t.__dict__[k], s.__dict__[k])
            print(f'Checking {k} \n{t.__dict__[k]}  \n{s.__dict__[k]}\n ')

    def test_saving_diataclass_tuple_as_yaml(self):
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)

        @dataclass
        class yam(SaveAsYaml):
            t: tuple = field(default_factory=tuple)

            def __post_init__(self):
                self.t = (410850000, 'BULK', 'test')

        enabled_freq_tuple = (200, 210)
        s = yam()
        s.save(configfile.name)

        # load saved dataclass from file and compare
        t = yam().load(configfile.name, verbose=True)
        for k in s.__dict__.keys():
            print(f'Checking {k} \n{s.__dict__[k]}  \n{t.__dict__[k]}\n ')
            self.assertEqual(asdict(s)[k], t.__dict__[k])
