from unittest import TestCase
from _channels import *


class TestChannel(TestCase):
    def test_keys(self):
        c = Channel('test', 1, 'BULK UP')
        self.assertEqual(c.keys(), ['name', 'center', 'channel_type'])

    def test_values(self):
        c = Channel('test', 1, 'BULK UP')
        self.assertTupleEqual(c.values(), ('test', 1, 'BULK UP'))
        self.assertListEqual(list(c.values()), ['test', 1, 'BULK UP'])

    def test_fpga(self):
        c = Channel('test', 1, 'BULK UP')
        self.assertEqual(c.fpga(), 6250 * 1 + 409600000)
