import os
import tempfile
from dataclasses import asdict
from unittest import TestCase

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
        self.assertNotIsInstance(app_config, ConfigData)

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

        self.assertEqual(100, len(app_config.enabled_frequencies()))
