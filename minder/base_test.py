#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Minder is a simple(ish) test framework ..
"""
import sys, os, subprocess

dbg_print = (int(os.getenv('MINDER_DBG', 0)) and print) or (lambda *pp, **kw: None)


class BaseTest:
    exec_dir = ''  # default = find executables via path mechanism
    exec_file = 'ping' #'echo'  # stub for initial testing
    showOut = True
    times_over = 1

    def get_flavours(self):
        return ( 'localhost', 'absenthost')

    def get_args(self, flavour):
        return ('-c', '4', flavour)

    def cmd(self, *pp):
        print(pp)
        answer = (('stdbuf', '-o0', self.exec_dir + self.exec_file,)
            + tuple(map(str, pp)))
        dbg_print("External.cmd answer = ", answer)
        return answer

    def fixup(self, output, error):
        return output, error

    def process_output(self, output):
        pass  # stub


    def run(self, *args):
        cmd1 = self.cmd(*args)
        dbg_print (cmd1)
        process = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = (pipe.read().decode('utf8', errors='ignore')
                         for pipe in (process.stdout, process.stdout))

        print ("stdout: \n", output)
        print ("stderr: \n", error)
        output, error = self.fixup(output, error)
        return output

    def inspect(self, flavour, output):
        print("sorry, I - %s - don't (yet) do analysis!" % self)
        return False

    def summarize(self):
        print("sorry, I - %s - don't (yet) do summarizing!" % self)
        return False

    def prepare(self):
        pass

    def exercise(self):
        self.prepare()
        flavours = self.get_flavours()
        if not flavours:
            print("'%s' is not implemented or maybe just not enabled for this platform"
                  % self.__class__.__name__)
            return
        self.rows = []
        for time_over in range(self.times_over):
            row = []
            for flavour in flavours:
                output = self.run(*self.get_args(flavour))
                column = self.inspect(flavour, output)
                row.append(column)
            self.rows.append(row)
        self.summarize()

    def main(self):
        print("running %s" % sys.argv.pop(0))
        if sys.argv:
            self.run(*sys.argv)
        else:
            self.exercise()


if __name__ == "__main__":
    test = BaseTest()
    test.main()

