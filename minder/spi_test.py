#!/usr/bin/python3
# -*- coding: utf-8 -*-
from .base_test import BaseTest

class SpiTest(BaseTest):
    exec_dir = ''  # under review
    exec_file = 'spidev_test'
    showOut = True
    times_over = 2
    bit_rates = (2500000, 300000, 5000000, 6000000, )
    spiPort = '/dev/spidev1.0'

    def get_flavours(self):
        return [('-D', self.spiPort, '-s', bit_rate, '-I', 2000, '-o', 'results.bin',
                 '-p', '\x80\x80\x80\x80', '-S', 42, '-B')
                for bit_rate in self.bit_rates]


if __name__ == "__main__":
    test = SpiTest()
    test.main()
