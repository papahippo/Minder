#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
minder/spi_test.py contains the generic code for 'minding' the actual test program
'spi_dev_test'.
"""
from .base_test import BaseTest
import re

class UsbTest(BaseTest):
    """
Class 'UsbTest' is based on 'BaseTest'. Only functions which relate to program
'dd' and its output are subclassed. Most of the intelligence and
"housekeeping" is inherited straight from the base class.
A lot of stuff is defined at class level; this is done to facilitate
tweaking of parameters (e.g. 'spiPort') in derived classes for specific targets.
    """
    exec_dir = ''  # => no explicit path needed; linux can find this command!
    exec_file = 'dd'
    times_over = 5
    kbit_rates = (2500, 3000, 5000, 6000, )
    usbDevice = '/dev/sda2'  # typically Olliver's lightning fast disk (spare partition)
    count =10
    s_block_size = '16M'
    directions = {
        'input':  {'source' : usbDevice , 'destination' : '/dev/zero'},
        'output': {'source' : '/dev/zero' , 'destination' : usbDevice},
    }

    def get_flavours(self):
        return self.directions.keys()

    def get_args(self, flavour):
        df = self.directions[flavour]
        return ('if=' + df['source'], 'of=' + df['destination'], # 'conv=fdatasync',
                'bs=' + self.s_block_size, 'count=%d' % self.count)

    def arrange_args_for_table(self, flavour):
        return (
            ('direction', flavour),
            ('device', self.usbDevice),
            ('count', self.count),
            ('packet size', self.s_block_size),
        )

    def inspect(self, flavour, rc, output, stats):
        result = re.search(r'(\d+).+copied,\s+(\S+)\s+s,\s+' +
                           r'(\S+\s+\S+)',
                           output)
        byte_count, time_taken, transfer_rate = result and result.groups() or [None]*3

        # We return everything as strings, even the stats info.
        #
        return ((byte_count, time_taken,),  # this couple for accumulation towards summary
                #
                (('byte count', byte_count),  # this threesome for immediate inclusion in table
                 ('time taken', time_taken),
                 ('transfer rate', transfer_rate),
                 ))

    def summarize(self, flavour, ez_stats):
        """
'ez_stats' is a couple of lists: a list of receiving speeds and a list of transmission speeds.
Entries with the None value have been removed (hence the name ez => easy). But they are
strings not floats or ints so it's not all plain sailing!
        """
        print('summarize', flavour)
        s_byte_counts, s_times_taken = ez_stats
        total_byte_count = sum(map(int, s_byte_counts))
        total_time_taken = sum(map(float, s_times_taken))
        avg_MB_per_sec = (total_time_taken and "%.2f MB/sec" % (
                total_byte_count / (1000*1000*total_time_taken))
                             or None)
        return (
            ('total byte count', total_byte_count),
            ('total seconds taken', "%.5f" % total_time_taken),
            ('average rate', avg_MB_per_sec),
        )
