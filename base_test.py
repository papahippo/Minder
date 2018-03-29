#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Minder is a simple(ish) test framework ..
"""
import sys, os, subprocess

dbg_print = (int(os.getenv('MINDER_DBG', 0)) and print) or (lambda *pp, **kw: None)


class Test:
    exec_dir = ''  # default = find executables via path mechanism
    exec_file = 'ping' #'echo'  # stub for initial testing
    showOut = True

    def cmd(self, *pp):
        print(pp)
        answer = ('stdbuf', '-o0', self.exec_dir + self.exec_file,) + pp
        dbg_print("External.cmd answer = ", answer)
        return answer

    def process_output(self, output):
        pass  # stub

    def run(self, *args):
        cmd1 = self.cmd(*args)
        dbg_print (cmd1)
        process = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(process.stdout.readline, b''):
            output = line.strip().decode('utf8', errors='ignore')
            print(output)

        return output

if __name__ == "__main__":
    test = Test()
    test.run(*sys.argv[1:])
