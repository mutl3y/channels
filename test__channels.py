import pprint
from unittest import TestCase
from channels import Channel, default_config, main
import settings.config as config
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
        c = Channel('test', 1, 'BULK UP')
        self.assertEqual(list(c.__dict__.keys()), ['name', 'center', 'channel_type', 'fpga'])

    def test_values(self):
        c = Channel('test', 409606250, 'BULK UP')
        self.assertListEqual(list(c.__dict__.values()), ['test', 409606250, 'BULK UP', 1])


class GuiTest(TestCase):
    def test_test_code(self):
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)
        app_settings = config.Settings()
        # app_settings.data = default_config()

        # force overwrite of configuration
        app_settings.save(configfile.name)

        # test code
        c = Channel('test', 409606250, 'BULK UP')
        # c = channels.Channel('name',1,'str')
        self.assertListEqual(list(c.__dict__.values()), ['test',409606250, 'BULK UP', 1])
        app_settings.channels.append(c)
        app_settings.channels.append(c)
        self.assertListEqual(app_settings.channels, [c, c])

        print('Test: item to add to channel list', c)
        print('Test: should show 2 items')
        pp.pprint(app_settings.channels)

        main()

pp = pprint.PrettyPrinter(indent=4)
