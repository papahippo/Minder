#!/usr/bin/python3
# -*- coding: utf-8 -*-
from .base_test import BaseTest
import re

class SpiTest(BaseTest):
    exec_dir = ''  # under review
    exec_file = 'spidev_test'
    showOut = True
    times_over = 2
    kbit_rates = (2500, 3000, 5000, 6000, )
    spiPort = '/dev/spidev1.0'
    iterations_dict = {}  # gets filled in later
    packet_size = 256

    def get_flavours(self):
        """
This is little more complicated
        """
        for flavour in self.kbit_rates:
            self.iterations_dict[flavour] = int((30000*self.packet_size)/flavour)
        return self.kbit_rates

    def get_args(self, flavour):
        return ('-D', self.spiPort, '-s', flavour*1000, '-I', self.iterations_dict[flavour],
                '-o', 'results.bin', '-p', '\x80\x80\x80\x80',
                '-S', self.packet_size, '-B')

    def arrange_args_for_table(self, flavour):
        return (
            ('SPI port', self.spiPort),
            ('Kbits/second', flavour),
            ('packet size', self.packet_size),
            ('iterations', self.iterations_dict[flavour]),
        )

    def inspect(self, flavour, rc, output, stats):
        result = re.search(r'max speed\:\s+(\d+)\sHz.*\n' +
                           r'.*rate\:\s*tx\s*(.+)kbps\,\s+rx\s*(.+)kbps',
                           output)
        max_speed, tx_kbps, rx_kbps = result and result.groups() or [None]*3
        return (42,), (('rx kbps', rx_kbps),
                       ('tx kbps', tx_kbps),
                       ('max speed Hz', max_speed),
                       )
