import os
import time
from unittest import TestCase
import config
import tempfile
import pprint


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

pp = pprint.PrettyPrinter(indent=4)

class Test(TestCase):

    def test_fpga_to_hz(self):
        self.assertEqual(hz_to_fpga(410850000), 200)

    def test_hz_to_fpga(self):
        self.assertEqual(410850000, fpga_to_hz(200))

    def test_settings_1(self):
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)

        s = config.Settings().save(configfile.name)

        self.assertTrue(os.path.exists(configfile.name))




    def test_supplying_default_configuration(self):
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)

        enabled_freq_tuple = (200, 210)
        s = config.Settings()

        # setup test data, order is important for human eyes only loop checks keys
        s.channel_types = ['BULK UP', 'BULK DOWN', 'L2ACK', 'PRIORITY', 'RTS']
        s.channels = [{'center': 410850000, 'ch_type': 'BULK', 'name': 'test'}]
        freq_list = [{'enabled': True, 'fpga': fpga, 'hz': fpga_to_hz(fpga)} for fpga in
                     range(enabled_freq_tuple[0], enabled_freq_tuple[1])]
        s.frequencies = freq_list
        # stowers"] = []

        self.assertTrue(len([i['hz'] for i in s.frequencies if i['enabled']]) == (
                enabled_freq_tuple[1] - enabled_freq_tuple[0]))

        s.save(configfile.name)

        # self.assertTrue(len([i['hz'] for i in s.frequencies if i['enabled']]) == (
        #         enabled_freq_tuple[1] - enabled_freq_tuple[0]))
        t = config.Settings().load(configfile.name)

        for k in s.__dict__.keys():
            self.assertEqual(t.__dict__[k], s.__dict__[k])
            # print(f'Checking {t.__dict__[k]}  == {s.__dict__[k]}\n ')

        with open(configfile.name, 'r') as file_object:
            view = file_object.read()

        # print('tests passed here is what the data looked like \n1st line before, 2nd after \n')
        # print(s)
        # print(t)
        # print(f'\nThis is raw from config file \n{view}\n')
        #
        #
        # time.sleep(0.2)
