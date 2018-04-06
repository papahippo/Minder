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
    iterations = 2000
    packet_size = 42

    def get_flavours(self):
        return self.bit_rates

    def get_args(self, flavour):
        return ('-D', self.spiPort, '-s', flavour, '-I', self.iterations,
                '-o', 'results.bin', '-p', '\x80\x80\x80\x80',
                '-S', self.packet_size, '-B')
