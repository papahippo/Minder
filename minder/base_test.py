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
        return zip(('host', flavour),
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
        process = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        rc = process.wait()
        output, error = (pipe.read().decode('utf8', errors='ignore')
                         for pipe in (process.stdout, process.stdout))

        print(*["%s=<<%s>>\n" % (name, data) for name, data in
              (('stdout', output),
               ('stderr', error))])
        output, error = self.fixup(output, error)
        return rc, output

    def inspect(self, flavour, rc, output, stats):
        print("sorry, I - %s - don't (yet) do analysis!" % self)
        return None

    def summarize(self, flavour, stats):
        return False

    def prepare(self):
        self.accumulator = OrderedDict()
        for flavour in self.get_flavours():
            args_nice = self.arrange_args_for_table(flavour)
            table = h.table()
            headers, values = args_nice
            table |= (h.tr() | [(h.th(Class='input') | header) for header in headers])
            table |= (h.tr() | [(h.td(Class='input') | value) for value in values])
            # print(table, file=self.html_out)
            # sys.exit(42)  # temporary!
            stats =list()
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
                style, (result_headers, result_details) = self.inspect(flavour, rc, output, stats)
                print("result headers, details: ", result_headers, result_details)
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
            self.summarize(flavour, stats)

        return h.p | (
            h.h2 | self.get_title(), h.br,
            [(table, h.br*2) for table, stats in self.accumulator.values()]
        )
