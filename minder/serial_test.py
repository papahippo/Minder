#!/usr/bin/python3
# -*- coding: utf-8 -*-
from .base_test import BaseTest

class SerialTest(BaseTest):
    exec_dir = ''  # under review
    exec_file = 'linux-serial-test'
    showOut = True
    times_over = 2
    bit_rates = (115200, 250000, 500000, 1500000)
    ttyPort = '/dev/ttyUSB0'
    tx_secs = 3  # 30
    rx_secs = 5  # 35
    def get_flavours(self):
        return self.bit_rates

    def get_args(self, flavour):
        return ('-p', self.ttyPort, '-o', self.tx_secs, '-i', self.rx_secs,
                '-b', flavour)


if __name__ == "__main__":
    test = SerialTest()
    test.main()
