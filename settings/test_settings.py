import os
from unittest import TestCase
import config
import tempfile

def fpga_to_hz(var):
    return (6250 * int(var)) + 409600000


def hz_to_fpga(var):
    return int((var - 409600000) / 6250)

def cleanup(file):
    try:
        file.close()
        os.remove(file.name)
    except WindowsError as e:
        if e.winerror != 2:
            print(f'issues deleting {file.name}')
        pass


class Test(TestCase):


    def test_fpga_to_hz(self):
        self.assertEqual(fpga_to_hz(200), 410850000)

    def test_hz_to_fpga(self):
        self.assertEqual(410850000, fpga_to_hz(200))

    def test_settings_1(self):
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)

        s = config.Settings(config_file=configfile.name)
        self.assertTrue(os.path.exists(configfile.name))

    def test_supplying_default_configuration(self):
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)

        enabled_freq_tuple = (200,210)
        s = config.Settings(config_file=configfile.name)

        test_config = dict()
        freq_list = [{'fpga': fpga, 'hz': fpga_to_hz(fpga), 'enabled': True} for fpga in
                     range(enabled_freq_tuple[0], enabled_freq_tuple[1])]
        test_config["frequencies"] = freq_list
        test_config['channel_types'] = ['BULK UP', 'BULK DOWN', 'L2ACK', 'PRIORITY', 'RTS']
        test_config["channels"] = []
        test_config["channel_groups"] = []
        test_config["towers"] = []
        s.write_default_config(config=test_config)
        self.assertTrue(len( [i['hz'] for i in s.config['frequencies'] if i['enabled']]) == (enabled_freq_tuple[1] - enabled_freq_tuple[0]))






