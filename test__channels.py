import os
import tempfile
from dataclasses import asdict
from unittest import TestCase
from dataclasses import dataclass, field

import yaml

from _channels import Frequency, Channel, ConfigData, config_factory


def cleanup(file):
    try:
        file.close()
        os.remove(file.name)
    except WindowsError as e:
        if e.winerror != 2:
            print(f'issues deleting {file.name}')
        pass


class TestChannel(TestCase):
    def test_Frequency(self):
        f = Frequency(enabled=True, hz=409600333)
        c = Channel(name='test', frequency=f, channel_type='BULK UP')
        for k in asdict(c):
            self.assertIn(k, ['name', 'frequency', 'channel_type'])

    def test_Channel(self):
        f = Frequency(hz=409606250, enabled=True)
        c = Channel(name='test', frequency=f, channel_type='BULK UP')
        self.assertListEqual(list(c.__dict__.values()),
                             ['test', 'BULK UP', Frequency(hz=409606250, enabled=True)])

    def test_config_factory_invalid_yaml(self):
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)

        # test with empty file
        app_config = config_factory(configfile.name, verbose=False)
        self.assertNotIsInstance(app_config, dict)
        self.assertIsInstance(app_config,yaml.YAMLError)

    def test_config_factory_missing_file(self):
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)

        # test with file missing
        cleanup(configfile)
        app_config = config_factory(configfile.name, verbose=False)
        self.assertIsInstance(app_config, ConfigData)

    def test_enabled_frequencies(self):
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)
        # test with file missing
        cleanup(configfile)
        app_config = config_factory(configfile.name, verbose=False, enabled_freq_tuple=(100, 200))
        print(f'test print only -- {app_config}')

        self.assertEqual(100, len(app_config.enabled_frequencies()))
        # check datastructures are right before reloading
        self.assertIsInstance(app_config, ConfigData)
        self.assertIsInstance(app_config.frequencies[0], Frequency)
        self.assertIsInstance(app_config.channels[0], Channel)
        self.assertIsInstance(app_config.channels[0].frequency, Frequency)

    def test_save_reload_dataclass_as_yaml(self):
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)
        cleanup(configfile)

        app_config = config_factory(configfile.name, verbose=False, enabled_freq_tuple=(100, 200))
        print(f'test print only -- loading config {app_config}\n')

        app_config = ConfigData(configfile.name)
        app_config.default_config(enabled_freq_tuple=(100, 200))
        app_config.save(configfile.name)


        # reload config
        new_app_config = ConfigData.load(configfile.name)
        self.assertIsInstance(new_app_config, ConfigData)
        self.assertIsInstance(new_app_config.frequencies[0], Frequency)
        self.assertIsInstance(new_app_config.channels[0], Channel)
        self.assertIsInstance(new_app_config.channels[0].frequency, Frequency)

    def test_update_from_dict(self):
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)
        cleanup(configfile)

        app_config = config_factory(configfile.name, verbose=False)

        # check datastructures are right before reloading
        self.assertIsInstance(app_config, ConfigData)
        self.assertIsInstance(app_config.frequencies[0], Frequency)
        self.assertIsInstance(app_config.channels[0], Channel)
        self.assertIsInstance(app_config.channels[0].frequency, Frequency)

        # reload config
        new_app_config = ConfigData(configfile.name)
        print(f'test print only -- reloading config {new_app_config}')
        new_app_config.update(asdict(app_config))

        self.assertIsInstance(new_app_config, ConfigData)
        self.assertIsInstance(new_app_config, ConfigData)
        self.assertIsInstance(new_app_config.frequencies[0], Frequency)
        self.assertIsInstance(new_app_config.channels[0], Channel)
        self.assertIsInstance(new_app_config.channels[0].frequency, Frequency)

        # print(app.enabled_frequencies())
        #
        # @dataclass
        # class config():
        #     channel_types: list = field(default_factory=list)
        #     channels: list = field(default_factory=list)
        #     frequencies: list = field(default_factory=list)
        #     towers: dict = field(default_factory=dict)
        #
        #     def __post_init__(self):
        #         self.channels: list = [{'center': 410850000, 'ch_type': 'BULK', 'name': 'test'}]
        #         self.frequencies: list = [{'enabled': True, 'fpga': fpga, 'hz': (6250 * int(fpga)) + 409600000} for fpga in
        #                              range(200, 210)]
        #
        # enabled_freq_tuple = (200, 210)
        # s = config()
        # s.save(configfile.name)
        #
        # print(s)
        # # load saved dataclass from file and compare
        # t = config().load(configfile.name, verbose=True)
        # for k in s.__dict__.keys():
        #     self.assertEqual(t.__dict__[k], s.__dict__[k])
        #     print(f'Checking {k} \n{t.__dict__[k]}  \n{s.__dict__[k]}\n ')
