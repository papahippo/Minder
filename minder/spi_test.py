#!/usr/bin/python3
# -*- coding: utf-8 -*-
from .base_test import BaseTest


class SpiTest(BaseTest):
    exec_dir = ''  # under review
    exec_file = 'spidev_test'
    showOut = True
    times_over = 2
    kbit_rates = (2500, 3000, 5000, 6000, )
    spiPort = '/dev/spidev1.0'
    iterations = 2000
    packet_size = 256

    def get_flavours(self):
        return self.kbit_rates

    def get_args(self, flavour):
        return ('-D', self.spiPort, '-s', flavour*1000, '-I', int((50000*self.packet_size)/flavour),
                '-o', 'results.bin', '-p', '\x80\x80\x80\x80',
                '-S', self.packet_size, '-B')
