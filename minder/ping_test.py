#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
from .base_test import BaseTest

class PingTest(BaseTest):
    exec_dir = ''  # default = find executables via path mechanism
    exec_file = 'ping'  # stub for initial testing
    showOut = True
    times_over = 1
    count = 4
    _title = None

    def get_title(self):
        return self._title or self.__class__.__name__

    def get_flavours(self):
        return 'localhost', 'absenthost'

    def get_args(self, flavour):
        return '-c', 10, flavour

    def arrange_args_for_table(self, flavour):
        return 'width:40%', zip(('host', flavour), ('count', self.count))

    def inspect(self, flavour, rc, output, stats):
        result = re.search(r'(\d+) packets transmitted\D.(\d+)\sreceived\D+(\d+)\% packet loss,'
                           r'.*time\s+(\d+\S+)', # .*=\s+',
                           output)
        if result is not None:
            print(result.groups())
        return "width:100%", (('transmitted', 'received', '% packet loss', 'time'),
                              result and result.groups() or [None]*4)
        # to be finished to include stats from last line too!
if __name__ == "__main__":
    test = PingTest()
    test.main()
