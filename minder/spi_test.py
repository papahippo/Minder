#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
minder/spi_test.py contains the generic code for 'minding' the actual test program
'spi_dev_test'.
"""
from .base_test import BaseTest
import re

class SpiTest(BaseTest):
    """
Class 'SpiTest' is based on 'BaseTest'. Only functions which relate to program
'spi_dev_test' and its output are subclassed. Most of the intelligence and
"housekeeping" is inherited straight from the base class.
A lot of stuff is defined at class level; this is done to facilitate
tweaking of parameters (e.g. 'full_device_name') in derived classes for specific targets.
    """
    exec_dir = ''  # under review
    exec_file = 'spidev_test'
    showOut = True
    times_over = 2
    kbit_rates = (2500, 3000, 5000, 6000, )
    device_name_pattern = 'spi.+'
    iterations_dict = {}  # gets filled in later
    packet_size = 256
    # 'dividend' represents a hack to make sure we test long enough to get
    #  at least one rate report from spi_dev_test!
    dividend = 60000

    def get_flavours(self):
        """
This 'get_flavours' is a little more complicated than that of other [Device]Test classes because we
fudge the arguments to make the would-be quicker tests run unnaturally longer.
        """
        for flavour in self.kbit_rates:
            self.iterations_dict[flavour] = int((self.dividend*self.packet_size)/flavour)
        return self.kbit_rates

    def get_args(self, flavour):
        """
The arguments returned by this 'getargs' implementation rely on minor local changes to
'spi_dev_test' with respect to the standard version in the kernel tree.
In particular, these changes make it possible to specify a fixed pattern at the start of
of a long repeated packet. This makes it easier to check the frame timing on a scope.
TODO: make these changes official or at least easily findable!

        """
        return ('-D', self.full_device_name, '-s', flavour*1000,
                '-I', self.iterations_dict[flavour],
                '-o', 'results.bin', '-p', '@@@@',
                '-S', self.packet_size, '-B')

    def arrange_args_for_table(self, flavour):
        return (
            ('SPI port', self.full_device_name),
            ('Kbits/second', flavour),
            ('packet size', self.packet_size),
            ('iterations', self.iterations_dict[flavour]),
        )

    def inspect(self, flavour, rc, output, stats):
        result = re.search(r'max speed\:\s+(\d+)\sHz.*\n' +
                           r'.*rate\:\s*tx\s*(\S+)kbps\,\s+rx\s*(\S+)kbps',
                           output)
        max_speed, tx_kbps, rx_kbps = result and result.groups() or [None]*3

        # We return everything as strings, even the stats info.
        #
        return ((rx_kbps, tx_kbps,),  # this couple for accumulation towards summary
                #
                (('rx kbps', rx_kbps),  # this threesome for immediate inclusion in table
                 ('tx kbps', tx_kbps),
                 ('max speed Hz', max_speed),
                 ))

    def summarize(self, flavour, ez_stats):
        """
'ez_stats' is a couple of lists: a list of receiving speeds and a list of transmission speeds.
Entries with the None value have been removed (hence the name (ez => easy). But they are
strings not floats so it's not all plain sailing!
        """
        f_rx_kbps, f_tx_kbps = [list(map(float, stat_list)) for stat_list in ez_stats]
        return [
            (name, (f and '%.2f' % (sum(f) / len(f)) or None))
            for name, f in (('avg rx rate', f_rx_kbps),
                                 ('avg tx rate', f_tx_kbps))
        ]
