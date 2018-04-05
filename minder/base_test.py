#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Minder is a simple(ish) test and evaluation framework ..
"""
import sys, os, subprocess
from collections import OrderedDict
from phileas import _html40 as h
# import phileas
# print(phileas.__path__)

dbg_print = (int(os.getenv('MINDER_DBG', 0)) and print) or (lambda *pp, **kw: None)


class BaseTest:
    exec_dir = ''  # default = find executables via path mechanism
    exec_file = ''  # stub for initial testing
    showOut = True
    times_over = 1
    count = 4
    _title = None

    def get_title(self):
        return self._title or self.__class__.__name__

    def get_flavours(self):
        return None

    def get_args(self, flavour):
        return '-c', '4', flavour

    def arrange_args_for_table(self, flavour):
        return 'width:40%', zip(('host', flavour),
                             ('count', self.count))

    def cmd(self, *pp):
        print(pp)
        answer = (('stdbuf', '-o0', self.exec_dir + self.exec_file,)
                  + tuple(map(str, pp)))
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
            style, args_nice = self.arrange_args_for_table(flavour)
            table = h.table(style=style)
            headers, values = args_nice
            table |= (h.tr() | [(h.th(style="background-color: f0c0c0;text-align:center;border: 1px solid #ddd; padding: 8px;") | header) for header in headers])
            table |= (h.tr() | [(h.td(style="background-color: f0f0f0;text-align:center;border: 1px solid #ddd; padding: 8px;color:blue") | value) for value in values])
            # print(table, file=self.html_out)
            # sys.exit(42)  # temporary!
            stats =list()
            self.accumulator[flavour] = (table, stats)

    def exercise(self):
        self.prepare()
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
                        h.th(style="border: 1px solid #ddd; padding: 8px;background-color: a0a0f0;") | 'seqno.',
                        [(h.th(style="border: 1px solid #ddd; padding: 8px;background-color: a0a0f0;") | header)
                         for header in result_headers]
                    ))
                table |= (h.tr | (
                    h.th(style="background-color: f0f0f0;text-align:center;border: 1px solid #ddd; padding: 8px;") | (1+time_over),
                    [(h.td(style="background-color: d0d0f0;text-align:center;border: 1px solid #ddd; padding: 8px;") |
                      ('-' if value is None else value)) for value in result_details]
                ))
        for flavour, (table, stats) in self.accumulator.items():
            self.summarize(flavour, stats)

        print(h.p | (
            h.h2 | self.get_title(), h.br,
            [(table, h.br*2) for table, stats in self.accumulator.values()]
        ), file=self.html_out)

    def main(self):
        print("running %s" % sys.argv.pop(0))
        if sys.argv:
            self.run(*sys.argv)
        else:
            with open('test.html', 'w') as self.html_out:
                self.exercise()


if __name__ == "__main__":
    test = BaseTest()
    test.main()

