#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Minder is a simple(ish) test and evaluation framework ..
"""
import sys, os, subprocess
from collections import OrderedDict
from phileas import html40_ as h

dbg_print = (int(os.getenv('MINDER_DBG', 0)) and print) or (lambda *pp, **kw: None)


class BaseTest:
    pre_args = ('stdbuf', '-o0')
    exec_dir = ''  # default = find executables via path mechanism
    exec_file = ''  # stub for initial testing
    showOut = True
    times_over = 1
    count = 4
    _title = None

    def get_title(self):
        return (self._title or self.__class__.__name__) + " on %s" % self.target_name

    def get_flavours(self):
        return None

    def get_args(self, flavour):
        return '-c', '4', flavour

    def arrange_args_for_table(self, flavour):
        return (('host', flavour),
                ('count', self.count))

    def cmd(self, *pp):
        print(pp)
        answer = map(str,
                     self.pre_args +
                     (self.exec_dir + self.exec_file,) +
                     pp)
        dbg_print("External.cmd answer = ", answer)
        return answer

    def fixup(self, output, error):
        return output, error

    def process_output(self, rc, output):  # obsolescent?
        pass  # stub

    def run(self, *args):
        cmd1 = self.cmd(*args)
        dbg_print(cmd1)
        if 0:  # this requires python 3.5 so is not (yet?) appropriate!
            process = subprocess.run(cmd1,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
            output, error = (stream.decode('utf8', errors='ignore')
                             for stream in (process.stdout,
                                            process.stderr))
        else:  # this is also ok under python 3.4!
            process = subprocess.Popen(cmd1,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.STDOUT)
            output = ''
            for line_bytes in process.stdout:
                line_str = line_bytes.decode('utf8', errors='ignore')
                print(line_str, end='')
                output += line_str
        # kind of broken 'for now'  ...
        # output, error = self.fixup(output, error)
        return process.returncode, output

    def inspect(self, flavour, rc, output, stats):
        print("sorry, I - %s - don't (yet) do analysis!" % self)
        return None

    def summarize(self, flavour, stats):
        return ("None",), ("-",)

    def prepare(self):
        self.accumulator = OrderedDict()
        for flavour in self.get_flavours():
            table = h.table()
            headers, values = zip(*self.arrange_args_for_table(flavour))
            table |= (h.tr() | [(h.th(Class='input') | header) for header in headers])
            table |= (h.tr() | [(h.td(Class='input') | value) for value in values])
            stats = list()
            self.accumulator[flavour] = (table, stats)

    def exercise(self):
        flavours = self.get_flavours()
        if not flavours:
            print("'%s' is not runnable on this platform"
                  % self.get_title())
            return
        self.prepare()
        for time_over in range(self.times_over):
            for flavour, (table, stats) in self.accumulator.items():
                rc, output = self.run(*self.get_args(flavour))
                numbers, results_for_table = self.inspect(flavour, rc, output, stats)
                result_headers, result_details = zip(*results_for_table)
                print("result headers, details: ", result_headers, result_details)
                stats.append(numbers)
                if time_over is 0:
                    table |= (h.tr() | (
                        h.th(Class='output') | 'seqno.',
                        [(h.th(Class='output') | header)
                         for header in result_headers]
                    ))
                table |= (h.tr | (
                    h.th(Class='output') | (1+time_over),
                    [(h.td(Class='output') |
                      ('-' if value is None else value)) for value in result_details]
                ))
        for flavour, (table, stats) in self.accumulator.items():
            headers, values = self.summarize(flavour, stats)


        return h.p | (
            h.h2 | self.get_title(), h.br,
            [(table, h.br*2) for table, stats in self.accumulator.values()]
        )
