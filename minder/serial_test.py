#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
from .base_test import BaseTest

class SerialTest(BaseTest):
    """
'SerialTest' is implemented around  the 'Minder' test framework.
    """
    exec_dir = ''  # usually rely on the path mechanism to find the test executable.
    # the following program is available from:
    #  https://github.com/cbrake/linux-serial-test.git
    exec_file = 'linux-serial-test'
    showOut = True  # obsolete?
    times_over = 5
    bit_rates = (115200, 250000, 500000, 1500000)
    # default ttyPort sometimes ok on PC, but invariably overruled on SOM target.
    ttyPort = '/dev/ttyUSB0'
    tx_secs = 30
    rx_secs = 35

    def prepare(self):
        BaseTest.prepare(self)
        self.prev_kernel_stats = (0, 0, 0, 0,)

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
        # user level stats expected to be present on all platforms:
        result = re.search(r'session\:\s*rx=(\d+)\D+tx=(\d+)\D+rx\s*err=(\d+)',
                           output)
        received, transmitted, rx_errors = result and map(int, result.groups()) or [None]*3
        tx_rate = result and float(transmitted / self.tx_secs) or None
        s_tx_rate = result and '%.2f' % tx_rate or None

        # kernel level stats expected to be present on target but not (yet?) on pc:
        result = re.search(r'TIOCGICOUNT\:.*frame\s*=\s*(\d+).*overrun\s*=\s*(\d+)' +
                           r'.*parity\s*=\s*(\d+).*brk\s*=\s*(\d+).*buf_overrun\s*=\s*(\d+)',
                           output)
        # The kernel's stats are all cumulative; but we really want to see just the
        # 'deltas' for this run (see also 'prepare' above:

        if result:
            new_cumulatives = list(map(int, result.groups()))
            actual = [
                new_cumulatives[i] - self.prev_kernel_stats[i] for i in range(4)]
            self.prev_kernel_stats = new_cumulatives

        else:
            actual = [None]*4

        framing_errors, overrun_errors, parity_errors, buf_overruns = actual
        return (tx_rate,), (('received', received),
                            ('transmitted', transmitted),
                            ('rx err', rx_errors),
                            ('tx rate', s_tx_rate),
                            ('framing err', framing_errors),
                            ('overrun err', overrun_errors),
                            ('parity err', parity_errors),
                            ('buf overruns', buf_overruns),
                            )

    def summarize(self, flavour, ez_stats):
        tx_rates,  = ez_stats
        avg_tx_rate = tx_rates and '%.2f' % (sum(tx_rates) / len(tx_rates)) or None
        return (('avg tx rate', avg_tx_rate),
                )
