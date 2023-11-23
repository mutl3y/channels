import dataclasses
import os
from unittest import TestCase

import gui
import user_interfaces


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

test_lookups = {'channel_type': ['BULK UP', 'BULK DOWN', 'L2ACK', 'PRIORITY', 'RTS']}


class TestGraphicalUi(TestCase):
    # def test_decode(self):
    #
    #     a_str, a_list, b_list = gui.decode(channels_as_dict.copy())
    #     self.assertIsInstance(a_str, str)
    #     self.assertIsInstance(a_list, list)
    #     self.assertIsInstance(b_list, list)
    #     print(f'Headers {a_list} \nData : {b_list}')

    # def test_pack(self):
    #     d = channels_as_dict['channels'][0]
    #     print(d)
    #     headers, list_in = list(d.keys()), list(d.values())
    #
    #     a_data = gui.pack(headers, list_in)
    #     print(a_data)
    #     self.assertIsInstance(a_data, dict)
    #     self.assertEqual(headers,list(a_data.keys()))
    #
    #
    #     ch0 = {'name': ['test', 'BULK', {'enabled': True, 'fpga': 200, 'hz': 410850000}]}
    #     print(f'check output \n{a_data} \n{ch0}')
    #     self.assertDictEqual(a_data, ch0)

    def test_edit(self):
        ui = user_interfaces.new_ui('gui')
        changed, ret = ui.edit(title='channels', a_dict=channels_as_dict.copy()['channels'], auto_close=10,
                               lookup=test_lookups)
        # self.assertIsInstance(ret, dict)
        # self.assertIsInstance(changed, bool)
