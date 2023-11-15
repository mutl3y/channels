from unittest import TestCase
from channels import Channel, default_config, main
import settings.config as config
import tempfile, os


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
        c = Channel('test', 1, 'BULK UP')
        self.assertListEqual(list(c.__dict__.values()), ['test', 1, 'BULK UP', 409606250])



class GUI_Test(TestCase):
    def test_test_code(self):
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)
        app_settings = config.Settings()
        app_settings.data = default_config()

        # force overwrite of configuration
        app_settings.save(configfile.name)

        # test code
        c = Channel('test', 1, 'BULK UP')
        # c = channels.Channel('name',1,'str')
        print('item to add ', c.__dict__.values())
        self.assertListEqual(list(c.__dict__.values()), ['test', 1, 'BULK UP', 409606250])
        # app_settings.data['channels'] = []
        # # += c.__dict__
        # app_settings.data['channels'].append(c.__dict__.values())
        print(app_settings.data['channels'])
        # app_settings.write_config()
        # self.assertDictEqual(dict(app_settings.config['channels']), c.__dict__)

        print('should show 2 items',list(app_settings.data['channels']))

        main()
