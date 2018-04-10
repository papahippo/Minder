#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
from .base_test import BaseTest

class SerialTest(BaseTest):
    exec_dir = ''  # under review
    exec_file = 'linux-serial-test'
    showOut = True
    times_over = 2
    bit_rates = (115200, 250000) # , 500000, 1500000)
    ttyPort = '/dev/ttyUSB0'
    tx_secs = 3  # 30
    rx_secs = 5  # 35

    def get_flavours(self):
        return self.bit_rates

    def get_args(self, flavour):
        return ('-p', self.ttyPort, '-o', self.tx_secs, '-i', self.rx_secs,
                '-b', flavour)

    def arrange_args_for_table(self, flavour):
        return (
            ('ttyPort', self.ttyPort),
            ('bit ("baud") rate', flavour),
            ('transmit seconds', self.tx_secs),
            ('receive seconds', self.rx_secs),
        )

    def inspect(self, flavour, rc, output, stats):
        result = re.search(r'session\:\s*rx=(\d+)\D+tx=(\d+)\D+rx\s*err=(\d+)',
                           output)
        received, transmitted, rx_errors = result and result.groups() or [None]*3

        return (42,), (('received', received),
                       ('transmitted', transmitted),
                       ('rx errors', rx_errors),
                       )

    def summarize(self, flavour, stats):
        print(flavour, stats)
        dummy_avg = sum([stat[0] for stat in stats]) / len(stats)
        print ("=============", dummy_avg)
        return (('dummy_avg',), dummy_avg,) # not yet tabulated!
