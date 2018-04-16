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
    # 'dividend' represents a hack to make sure we test long enough to get
    #  at least one rate report from spi_dev_test!
    dividend = 60000

    def get_flavours(self):
        """
This is little more complicated
        """
        for flavour in self.kbit_rates:
            self.iterations_dict[flavour] = int((60000*self.packet_size)/flavour)
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
                           r'.*rate\:\s*tx\s*(\S+)kbps\,\s+rx\s*(\S+)kbps',
                           output)
        max_speed, tx_kbps, rx_kbps = result and result.groups() or [None]*3
        return ((rx_kbps, tx_kbps,),  # this couple for accumulation towards summary
                #
                (('rx kbps', rx_kbps),  # this threesome for immediate inclusion in table
                 ('tx kbps', tx_kbps),
                 ('max speed Hz', max_speed),
                 ))

    def summarize(self, flavour, ez_stats):
        f_rx_kbps, f_tx_kbps = [list(map(float, stat_list)) for stat_list in ez_stats]
        return [
            (name, (f and '%.2f' % (sum(f) / len(f)) or None))
            for name, f in (('avg rx rate', f_rx_kbps),
                                 ('avg tx rate', f_tx_kbps))
        ]
