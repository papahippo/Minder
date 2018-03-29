#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Try-out snippet of code for parsing ostensibly man-readable output
Currently this reads a captured log-file. Ultimately it will suck in the output
of a sub-process.
"""
import sys, os, re


class app_counts:
    pass


class kernel_counts:
    pass



def main():
    port = '/dev/ttyS1'
    with open('/home/lmyerscough/log/serialhammer1.log', 'r') as log:
        while True:
            line = log.readline().strip()
            result = re.match(r'%s\:\s*(\w+).*\:(.*)' % port, line)
            if not result:
                continue
            tag, rest = result.groups()
            category = {'count': app_counts, 'TIOCGICOUNT': kernel_counts,}.get(tag)
            print(tag, '...', rest)
            results = re.findall(r'\W*(\w+)\s*=\s*(\w+),?\s*', rest)
            if not results:
                print("parse error!")
                continue
            for name, value in results:
                category.setattr(name, value)


if __name__ == '__main__':
    main()
