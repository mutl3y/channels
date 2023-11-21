import dataclasses
import os
import tempfile
from dataclasses import asdict
from unittest import TestCase

import gui
import user_interfaces
from _channels import config_factory, Channel, Frequency


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

# used in tests
channels_as_dict = {'channels': [
    {'name': 'test', 'channel_type': 'BULK', 'frequency': {'enabled': True, 'fpga': 200, 'hz': 410850000}},
    {'name': 'test2', 'channel_type': 'BULK', 'frequency': {'enabled': True, 'fpga': 200, 'hz': 410850000}}
]}

class TestGraphicalUi(TestCase):
    def test_decode(self):

        a_str, a_list, b_list = gui.decode(channels_as_dict.copy())
        self.assertIsInstance(a_str, str)
        self.assertIsInstance(a_list, list)
        self.assertIsInstance(b_list, list)
        print(f'Headers {a_list} \nData : {b_list}')

    def test_pack(self):
        title, headers, data = gui.decode(channels_as_dict.copy())
        a_data = gui.pack(headers[0], data[0])
        print(a_data)
        self.assertIsInstance(a_data, dict)
        self.assertEqual(list(a_data.keys())[0], headers[0])

        ch0 = {'name': ['test', 'BULK', {'enabled': True, 'fpga': 200, 'hz': 410850000}]}

        self.assertDictEqual(a_data, ch0)
    def test_edit(self):
        ui = user_interfaces.new_ui('gui')
        changed, ret = ui.edit(a_dict=channels_as_dict.copy(), auto_close=20)
        self.assertIsInstance(ret, dict)
        self.assertIsInstance(changed, bool)


