import os
from unittest import TestCase
from data_class_storage import *
import tempfile
import pprint


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

    # def test_fpga_to_hz(self):
    #     self.assertEqual(hz_to_fpga(410850000), 200)
    #
    # def test_hz_to_fpga(self):
    #     self.assertEqual(410850000, fpga_to_hz(200))
    #
    # # def test_settings_1(self):
    # #     configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
    # #     self.addCleanup(cleanup, configfile)
    # #     s = config
    # #     s.save(configfile.name)
    # #
    # #     self.assertTrue(os.path.exists(configfile.name))

    def test_supplying_default_configuration(self):
        configfile = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', prefix='')
        self.addCleanup(cleanup, configfile)

        @dataclass
        class config(To_yaml):
            channel_types: list = field(default_factory=list)
            channels: list = field(default_factory=list)
            frequencies: list = field(default_factory=list)
            towers: list = field(default_factory=list)

            def __post_init__(self):
                self.channels: list = [{'center': 410850000, 'ch_type': 'BULK', 'name': 'test'}]
                self.frequencies: list = [{'enabled': True, 'fpga': fpga, 'hz': (6250 * int(fpga)) + 409600000} for fpga in
                                     range(200, 210)]

        enabled_freq_tuple = (200, 210)
        s = config()
        s.save(configfile.name)
        t = config().load(configfile.name)
        for k in s.__dict__.keys():
            self.assertEqual(t.__dict__[k], s.__dict__[k])
            print(f'Checking {k} \n{t.__dict__[k]}  \n{s.__dict__[k]}\n ')

            #
        #
        #
        # # self.assertTrue(len([i['hz'] for i in s.frequencies if i['enabled']]) == (
        # #         enabled_freq_tuple[1] - enabled_freq_tuple[0]))
        # t = config.To_yaml().load(configfile.name)
        #
        # for k in s.__dict__.keys():
        #     self.assertEqual(t.__dict__[k], s.__dict__[k])
        #     # print(f'Checking {t.__dict__[k]}  == {s.__dict__[k]}\n ')
        #
        # with open(configfile.name, 'r') as file_object:
        #     view = file_object.read()
        #
        # # print('tests passed here is what the data looked like \n1st line before, 2nd after \n')
        # # print(s)
        # # print(t)
        # print(f'\nThis is raw from config file \n{view}\n')
        #
        #
        # time.sleep(0.2)
