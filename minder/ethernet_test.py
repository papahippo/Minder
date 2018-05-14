#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
from .base_test import BaseTest

class EthernetTest(BaseTest):
    exec_dir = ''  # default = find executables via path mechanism
    exec_file = 'iperf3'  # stub for initial testing
    times_over = 10
    count = 4
    _title = None
    iperf3_hosts = ('localhost',)
    def get_flavours(self):
        return self.iperf3_hosts

    def get_args(self, flavour):
        return '-c', flavour

    def arrange_args_for_table(self, flavour):
        return (
            ('server', flavour),
        )

    def run(self, *pp):
        """
'Iperf3' gives all we want to know in one call. We have to fudge things a bit to get
this all neatly included in the results table
        """
        if self.time_over:  # every time except the first...
            return 0, ''  # just pretend
        return BaseTest.run(self, *pp)

    def inspect(self, flavour, rc, output, stats):
        print(self.time_over, '???')
        if self.time_over == 0:  # the first time around ...
            self.all_stats = re.findall(r'\[.*\n', output)
            print (list(enumerate(self.all_stats)))
        my_line = self.all_stats[2 + self.time_over]
        print(self.time_over, '---', my_line)
        result = re.match(r'.*\]\s+(\S+\s+\S+)\s+(\S+\s+\S+)\s+(\S+\s+\S+)'
                         +r'\s+(\S+)\s+(\S+\s+\S+).*', my_line)

        interval, transfer, bandwidth, retr, cwnd = (result and result.groups()
                                                      or [None]*5)

        return ([],  # no cumulative stats need to be collected
                [('interval', interval),
                 ('transfer', transfer),
                 ('bandwidth', bandwidth),
                 ('retr', retr),
                 ('cwnd', cwnd)])

    def summarize(self, flavour, ez_stats):
        """
'summarize receives in ez_stats a list of accumulated values for each of the stats which
were returned by successive calls to 'inspect'. All unknown values (we indicated these by
returning None have been removed.
        """
        result = re.match(r'.*\]\s+(\S+\s+\S+)\s+(\S+\s+\S+)\s+(\S+\s+\S+)'
                         +r'\s+(\S+)\s+(\S+).*', self.all_stats[13])
        interval, transfer, bandwidth, retr, role = (result and result.groups()
                                                     or [None] * 5)
        return  [('interval', interval),
                 ('transfer', transfer),
                 ('bandwidth', bandwidth),
                 ('retr', retr),
                 ('role', role)]

