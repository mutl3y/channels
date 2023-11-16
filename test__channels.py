import pprint
from unittest import TestCase

import channels
# import persistence.data_class_storage as config
import tempfile
import os


def cleanup(file):
    try:
        file.close()
        os.remove(file.name)
    except WindowsError as e:
        if e.winerror != 2:
            print(f'issues deleting {file.name}')
        pass


class TestChannel(TestCase):
    def test_keys(self):
        c = channels.Channel('test', 1, 'BULK UP')
        self.assertEqual(list(c.__dict__.keys()), ['name', 'frequency', 'channel_type'])

    def test_values(self):
        c = channels.Channel('test', channels.Frequency(hz=409606250, enabled=True), 'BULK UP')
        self.assertListEqual(list(c.__dict__.values()),
                             ['test', channels.Frequency(hz=409606250, enabled=True), 'BULK UP'])


class GuiTest(TestCase):
    def test_test_code(self):
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)
        app_config = channels.ConfigData()
        app_config.default_config()

        print(app_config)


#         # app_config.data = default_config()
#
#         # force overwrite of configuration
#         app_config.save(configfile.name)
#
#         # test code
#         c = Channel('test', 409606250, 'BULK UP')
#         # c = channels.Channel('name',1,'str')
#         self.assertListEqual(list(c.__dict__.values()), ['test',409606250, 'BULK UP', 1])
#         app_config.channels.append(c)
#         app_config.channels.append(c)
#         self.assertListEqual(app_config.channels, [c, c])
#
#         print('Test: item to add to channel list', c)
#         print('Test: should show 2 items')
#         pp.pprint(app_config.channels)
#
#         main()
#
#
#     def test_list(self):
#         configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
#         self.addCleanup(cleanup, configfile)
#         app_config = config.To_yaml()
#         print(
#             [f for f in app_config.frequencies]
#         )
#

# pp = pprint.PrettyPrinter(indent=4)


class TestConfigData(TestCase):
    def test_enabled_frequencies(self):
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)
        app_config = channels.ConfigData()
        app_config.default_config()
        self.assertEqual (10, len(app_config.enabled_frequencies()))
