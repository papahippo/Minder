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

    def get_flavours(self):
        #return [('-p', self.ttyPort, '-o', 30, '-i', 35, '-b', bit_rate)
        return [('-p', self.ttyPort, '-o', 3, '-i', 4, '-b', bit_rate)
                for bit_rate in self.bit_rates]


if __name__ == "__main__":
    test = SerialTest()
    test.main()
