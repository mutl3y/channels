import dataclasses
import os
from unittest import TestCase

# from user_interfaces import gui
# from AppConfig.settings import config_factory
import tempfile
import gui


def cleanup(file):
    try:
        file.close()
        os.remove(file.name)
    except WindowsError as e:
        if e.winerror != 2:
            print(f'issues deleting {file.name}')
        pass


@dataclasses.dataclass
class ConfigData:
    channels: list = dataclasses.field(init=True, default_factory=list)


@dataclasses.dataclass
class ConfigData2(dict):
    _filename: str = dataclasses.field(init=True, default='config.yaml', hash=False, repr=False)
    channels: list = dataclasses.field(init=True, default_factory=list)
    channel_groups: list = dataclasses.field(init=True, default_factory=list)
    frequencies: list = dataclasses.field(init=True, default_factory=list)
    channel_types: list = dataclasses.field(init=True, default_factory=list)


config_as_dict = {'_filename': 'config.yaml', 'channels': [
    {'name': 'test', 'channel_type': 'BULK', 'frequency': {'enabled': True, 'hz': 410850000, 'fpga': 200}}],
                  'channel_groups': [], 'frequencies': [{'enabled': True, 'hz': 410850000, 'fpga': 200},
                                                        {'enabled': True, 'hz': 410856250, 'fpga': 201},
                                                        {'enabled': True, 'hz': 410862500, 'fpga': 202},
                                                        {'enabled': True, 'hz': 410868750, 'fpga': 203},
                                                        {'enabled': True, 'hz': 410875000, 'fpga': 204},
                                                        {'enabled': True, 'hz': 410881250, 'fpga': 205},
                                                        {'enabled': True, 'hz': 410887500, 'fpga': 206},
                                                        {'enabled': True, 'hz': 410893750, 'fpga': 207},
                                                        {'enabled': True, 'hz': 410900000, 'fpga': 208},
                                                        {'enabled': True, 'hz': 410906250, 'fpga': 209}],
                  'channel_types': ['BULK UP', 'BULK DOWN', 'L2ACK', 'PRIORITY', 'RTS']}

# used in tests
channels_as_dict = {'channels': [
    {'name': 'test', 'channel_type': 'BULK', 'frequency': {'enabled': True, 'fpga': 200, 'hz': 410850000}},
    {'name': 'test2', 'channel_type': 'BULK', 'frequency': {'enabled': True, 'fpga': 200, 'hz': 410850000}}
]}

test_lookups = {'channel_type': ['BULK UP', 'BULK DOWN', 'L2ACK', 'PRIORITY', 'RTS']}


class TestGraphicalUi(TestCase):
    def test_pack(self):
        d = channels_as_dict['channels'][0]
        print(f'test data {d}')
        headers, list_in = list(d.keys()), list(d.values())

        a_data = gui.pack(headers, list_in)
        print(f'packed data {a_data}')
        self.assertIsInstance(a_data, dict)
        self.assertEqual(headers, list(a_data.keys()))
        # ch0 = {'name': ['test', 'BULK', {'enabled': True, 'fpga': 200, 'hz': 410850000}]}

        # packed item should be dict
        ch0 = {'name': 'test', 'channel_type': 'BULK', 'frequency': {'enabled': True, 'fpga': 200, 'hz': 410850000}}

        self.assertDictEqual(a_data, ch0)

    def test_edit_item_window(self):
        # ui = user_interfaces.new_ui('gui')
        changed, ret = gui.edit_item_window(title='channels', dict_in=channels_as_dict['channels'][0],
                                            auto_close=1,
                                            lookup=test_lookups)
        self.assertIsInstance(ret, dict)
        self.assertIsInstance(changed, bool)

    def test_edit_table_window(self):
        # ui = user_interfaces.new_ui('gui')
        changed, ret = gui.edit_table_window(title='channels', list_in=channels_as_dict['channels'],
                                             auto_close=1,
                                             lookup=test_lookups)
        self.assertIsInstance(ret, dict)
        self.assertIsInstance(changed, bool)

    def test_home(self):
        # ui = gui.new_ui('gui')
        # changed, ret = gui.home(config_as_dict)
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)
        cleanup(configfile)
        conf = config_as_dict
        print(conf)
        changed, ret = gui.edit_item_window(title='channels', dict_in=conf,
                                            auto_close=100,
                                            lookup=test_lookups)
        self.assertIsInstance(ret, dict)
        self.assertIsInstance(changed, bool)
