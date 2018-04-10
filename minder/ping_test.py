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

    def get_flavours(self):
        return 'localhost', 'absenthost'

    def get_args(self, flavour):
        return '-c', 10, flavour

    def arrange_args_for_table(self, flavour):
        return (
            ('host', flavour),
            ('count', self.count)
        )

    def inspect(self, flavour, rc, output, stats):
        result = re.search(r'(\d+) packets transmitted\D.(\d+)\sreceived\D+(\d+)\% packet loss,'
                           r'.*time\s+(\d+\S+)', # .*=\s+',
                           output)
        transmitted, received, packet_loss, timing = (
                result and result.groups() or [None] * 4
        )
        return (42,),  (('transmitted', transmitted),
                        ('received', received),
                        ('%% packet loss', packet_loss),
                        ('time', timing),
        )
        # to be finished to include stats from last line too!
