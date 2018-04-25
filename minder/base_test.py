#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Minder is a simple(ish) test and evaluation framework ..
"""
import sys, os, subprocess, tempfile, datetime, re
from collections import OrderedDict
from phileas import html5 as h
from .style import Style

dbg_print = (int(os.getenv('MINDER_DBG', 0)) and print) or (lambda *pp, **kw: None)


class BaseTest:
    """
'BaseTest' is the primary class of the 'Minder' (timing) test script.
A number of other test classes inherit from it.
For the sake of example, BaseTest also works as a 'ping test'. N.B. This is not
as such part of our performance tests. (see EthernetTest in 'ethernet_test.py').
    """
    pre_args = ('stdbuf', '-o0')  # stuff these in front of command.
    exec_dir = ''  # default = find executables via path mechanism
    exec_file = 'ping'  # stub for initial testing
    times_over = 1
    count = 4
    calibrate = 0
    _title = None
    device_name_pattern = ''
    full_device_name = ''

    def __init__(self, script_name='(script name?)',
                 reticent=0, verbose=0, calibrate=None):
        """
        :param reticent: non-zero => hold back output until progam until test completed.
        :param verbose:  larger values => more progress info. (not yet fully implemented)
        """
        self.script_name = script_name
        self.calibrate = self.calibrate and calibrate
        self.reticent = reticent
        self.verbose = verbose
        self.temp_dir = tempfile.mkdtemp(prefix=self.__class__.__name__+'_')
        self.ongoing_html_file = open(self.temp_dir+'/'+"ongoing.html", 'w')
        self.accumulator = OrderedDict()
        self.full_device_name = self.find_device()
        if self.full_device_name:
            print('using device name "%s"' % self.full_device_name)
        self.prepare()

    def prepare(self):
        """
'prepare' is really just '__init__ continued'!
        """
        # TODO: name should include date and time - implemented 25apr18 to be validated!
        self.start_time = datetime.datetime.now()
        s_now = str(self.start_time)[:19].replace(' ', '_')
        if not s_now.startswith('20'):
            print("WARNING: date not set; perhaps you ought to do (e.g.) 'ntpdate' first?")
        self.html_filename = (sys.argv and sys.argv[0] or
                         (os.path.splitext(self.script_name)[0] + '_' + s_now + '.html'))
        for flavour in self.get_flavours():
            table = h.table()
            headers, values = zip(*self.arrange_args_for_table(flavour))
            table |= (h.tr() | [(h.th(Class='input') | header) for header in headers])
            table |= (h.tr() | [(h.td(Class='input') | value) for value in values])
            stats = list()
            self.accumulator[flavour] = (table, stats)
        self.html = h.html | (
            h.style | Style(),
            h.body | (
                h.p | (
                    h.h3 | self.get_title(), h.br,
                    h.h4 |  ("running %s" % self.script_name),
                    ("%s: test started." % self.start_time, h.br,
    # under review! ...                        "%s %s" % (datetime.datetime.now(),  self.status_string), h.br,
                            ),
                    [(table, h.br*2) for table, stats in self.accumulator.values()]
                )
            )
        )

    def find_device(self):
        """
'find_device' was introduced late in development to make 'minder' more resilient to
occasional innocuous changes in device names; e.g. '/dev/ttyUART0' becomes '/dev/ttyUART1'
when the physical device is unplugged and plugged back in.
It is calledby __init__.
It returns one of the following:
        - The first or only eligible device name.
        - An empty string if no device required
        - False if a device is required but no suitable device seems to be present.
        """
        if not self.device_name_pattern:
            return ''
        ok_names = [dev_name for dev_name in os.listdir('/dev')
                    if re.match(self.device_name_pattern, dev_name)]
        return ok_names and '/dev/' + ok_names[0]

    def get_title(self):
        return (self._title or self.__class__.__name__) + " on %s" % self.target_name

    def get_flavours(self):
        """
Several distinct combination of arguments are passed to each test program. One of
these arguments (e.g. the baud rate in the case of SerialTest is used as a key in our
test administration. The various values of this key ar referred to as 'flavours'.
'get_flavours' returns the appropriate flavours for a particular test class.
Exceptionally , if the test is not possible for the current
platform, an empty sequence is returned.
        """
        return ('localhost',)

    def get_args(self, flavour):
        """
Function 'get_args' returns the complete collection of arguments associated with a
particular flavour, as a (sometimes quite long) tuple.
        """
        return '-c', '4', flavour

    def arrange_args_for_table(self, flavour):
        """
Function 'arrange_args_for_table' returns essential information about a particular flavour,
as tuple of pairs (tuples of length 2).
        """
        return (('host', flavour),
                ('count', self.count))

    def cmd(self, *pp):
        """
'cmd' expands the supplied command arguments to include any 'up front' arguments
(e.g. 'stdbuf', '-o0' ... or  'nice' ... ...) and the name of the program to be run.
Arguments are 'stringified' here so once may pass e.g. counts as integers.
        """
        answer = list(map(str,
                     self.pre_args +
                     (self.exec_dir + self.exec_file,) +
                     pp))
        print("cmd to be executed = ", ' '.join(list(answer)))
        return answer

    def fixup(self, output, error):
        """
Function fixup is intended to 'juggle' output between stdout and stderr, in order to
conform to the notion that stdout should be held back and analysed in due course,
whereas stderr should be shown as is immediately. Owing to problems with buffer deadlock,
this mechanism has been ditched 'for now'.
        """
        return output, error

    def run(self, *args):
        """
Function 'run' runs the test program (e.g. ping, serial_test, spi_dev_test).
The combined stderr/stdout output is returned together with the return code.
        """
        cmd1 = self.cmd(*args)
        dbg_print(cmd1)

        process = subprocess.Popen(cmd1,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        output = ''
 #TODO: 'wait' here if reticent. implemented; not yet validated.
        if self.reticent:
            dbg_print ('Minder.run waiting before reading output')
            process.wait()
        for line_bytes in process.stdout:
            line_str = line_bytes.decode('utf8', errors='ignore')

            # display the output immediately. This is handy when getting the
            # test up and running but should maybe be subject to a command line argument.
            #
            print(line_str, end='')
            output += line_str
        # kind of broken 'for now'  ...
        # output, error = self.fixup(output, error)
        dbg_print('Minder.run waiting after reading output')
        rc = process.wait()
        return rc, output

    def inspect(self, flavour, rc, output, stats):
        """
'inspect' receives the output (stdout and stderr combined) of a run of the test program
(and the return code which it currently ignores!).
It is expected to return a tuple: <numeric data>, <table data>.
The returned <numeric data> must be a tuple. This will simply be appended to other data
relating to this flavour of this test. (All this data gets supplied to 'summarize' later.
The returned <table data> represents a sequence of pairs (tuples of length 2)
each containing a header text and a data value (not per se a string) to be displayed
in an HTML table.
        """
        result = re.search(r'(\d+) packets transmitted\D.(\d+)\sreceived\D+(\d+)\% packet loss,'
                           r'.*time\s+(\d+)(\S+)',  # .*=\s+',
                           output)
        transmitted, received, packet_loss, timing, units = (
                result and result.groups() or [None] * 5
        )
        # following rough and ready approach might need tightening if ever we use this for real!
        f_timing = float(timing)
        if units == 'ms':
            f_timing *= 0.001
        return (  # must return a couple (tuple of two items).
            (int(transmitted), f_timing, ),  # first item contains statistics for accumulation ...
            (('transmitted', transmitted),  # second item contains data for inclusion
             ('received', received),  # 'as is' in table.
             ('%% packet loss', packet_loss),
             ('time', timing+units),
             )
        )

    def summarize(self, flavour, ez_stats):
        """
Function 'summarize' is called when for each 'flavour' all (self.times_over) iterations
have been completed. It is supplied with the statistics that our 'inspect' function  returned on
all iterations. These have been 'zipped' in the python sense ('rows' and 'columns' reversed), and
Entries with the value 'None' have been removed.
It is expected to return a sequence of pairs (tuples of length 2)
each containing a header text and a data value (not per se a string) to be displayed
in the 'summary' row of an HTML table.
        """
        tx_counts, f_timings, = ez_stats
        avg_tx_rate = f_timings and ('%.2f' % (sum(tx_counts) / sum(f_timings))) or None
        return (('avg pkt/s', avg_tx_rate),
                )


    def exercise(self):
        """
Function exercise is really the principle entry point of the class and is called directly
from the top-level main function (see '__init__.py').
It performs a number of iterations of each flavour of this class's test program and manages
the resulting statistics.
        """
        if not self.get_flavours():
            print("'%s' is not runnable on this platform"
                  % self.get_title())
            return ''  # barely adequate?
        for time_over in range(-self.calibrate, self.times_over):
# introduced the following statement late in the day so that tests that do their own
# iteration making ours superfluous (e.g. iperf3) can be handled more simply.
            #
            self.time_over = time_over
            for flavour, (table, stats) in self.accumulator.items():
                rc, output = self.run(*self.get_args(flavour))
                if time_over < 0:  # i.e. if calibrating
                    print("presss Enter when calibration is finished:")
                    s_calibrated = sys.stdin.readline()  # how can we work this into the table?
                    continue
                numbers, results_for_table = self.inspect(flavour, rc, output, stats)
                result_headers, result_details = zip(*results_for_table)
                dbg_print("result headers, details: ", result_headers, result_details)
                stats.append(numbers)
                if time_over == 0:  # i.e first actual measuring run (not calibration)
                    table |= (h.tr() | (
                        h.th(Class='output') | 'seqno.',
                        [(h.th(Class='output') | header)
                         for header in result_headers]
                    ))
                table |= (h.tr | (
                    h.th(Class='output') | (1 + time_over),
                    [(h.td(Class='output') |
                      ('-' if value is None else value)) for value in result_details]
                ))
                self.stash_my_html('test in progress...')
        for flavour, (table, stats) in self.accumulator.items():
            ez_stats = [[stat_item for stat_item in stat_cat if stat_item is not None]
                        for stat_cat in zip(*stats)]
            headers, values = zip(*self.summarize(flavour, ez_stats))
            table |= (h.tr | (
                h.th(Class='output') | 'summary',
                [(h.th(Class='output') | header)
                 for header in headers]
            ))
            table |= (h.tr | (
                h.th(Class='output') | '-',
                [(h.td(Class='output') |
                  ('-' if value is None else value)) for value in values]
            ))
        return self.stash_my_html('test completed!')

    def stash_my_html(self, status_string):
        """
Function  'stash_my_html' is called after each inner iteration. it writes the 'story so far'
as an HTML table to a temporary file (whose name includes our class name). It is also called
once after writing teh summary information.

It returns the same html to its caller. This is ignored except on the final call, when it
is returned (to 'main' in "__main__.py") for inclusion in an html report including this
and possibly other tests.
TODO: Better to maintain a single (as complete as possible) document throughout the test.
        """
        with open(self.html_filename, 'w') as html_file:
            print(self.html, file=html_file)
