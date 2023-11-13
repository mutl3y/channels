import os
from unittest import TestCase
import settings

testFile = 'test_config.yaml'


def cleanup(filename):
    try:
        os.remove(filename)
    except WindowsError as e:
        if e.winerror != 2:
            print(f'issues deleting {filename}')
        pass


class Test(TestCase):
    def test_fpga_to_hz(self):
        self.assertEqual(settings.fpga_to_hz(200), 410850000)

    def test_hz_to_fpga(self):
        self.assertEqual(410850000, settings.fpga_to_hz(200))

    def test_settings_1(self):
        cleanup(testFile)
        s = settings.Settings(config_file=testFile)
        self.assertTrue(os.path.exists(testFile))
        cleanup(testFile)

    def test_settings_fpgaRange(self):
        cleanup(testFile)
        s = settings.Settings(config_file=testFile)

        s.write_default_config(fpga_range=(200, 210), enabled=True)
        self.assertEqual(len(s.enabled_frequencies()), 10)
        os.remove(testFile)
        cleanup(testFile)
