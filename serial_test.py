#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import base_test


class SerialTest(base_test.Test):
    exec_dir = '~/bin/'  # under review
    exec_file = 'linux-serial-test'
    showOut = True


if __name__ == "__main__":
    test = SerialTest()
    test.run(*sys.argv)
