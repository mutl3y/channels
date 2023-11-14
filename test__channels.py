from unittest import TestCase
from _channels import *
import settings.config as config
import tempfile, os
import channels

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
        c = Channel('test', 1, 'BULK UP')
        self.assertEqual(c.keys(), ['name', 'center', 'channel_type'])

    def test_values(self):
        c = Channel('test', 1, 'BULK UP')
        self.assertTupleEqual(tuple(c.values()), ('test', 1, 'BULK UP'))
        self.assertListEqual(list(c.values()), ['test', 1, 'BULK UP'])

    def test_fpga(self):
        c = Channel('test', 1, 'BULK UP')
        self.assertEqual(c.fpga(), 6250 * 1 + 409600000)


class GUI_Test(TestCase):
    def test_test_code(self):
        # configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        # self.addCleanup(cleanup, configfile)
        # app_settings = config.Settings(config_file=configfile.name)

        app_settings = config.Settings()
        # force overwrite of configuration
        app_settings.write_default_config(channels.default_config())

        # test code
        h = channels.Channel('test', 1, 'BULK UP')
        print('item to add ',h.values())
        self.assertTrue(h.values())
        self.assertListEqual(list(h.values()), ['test', 1, 'BULK UP'])
        app_settings.config['channels'].append(h.values())
        app_settings.config['channels'].append(h.values())
        app_settings.write_config()
        self.assertListEqual(list(app_settings.config['channels']), [['test', 1, 'BULK UP'], ['test', 1, 'BULK UP']])

        print('should show 2 items',list(app_settings.config['channels']))

        channels.main()
