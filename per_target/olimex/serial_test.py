#!/usr/bin/python3
# -*- coding: utf-8 -*-

import minder


class SerialTest(minder.SerialTest):
    ttyPort = '/dev/ttyS1'


if __name__ == "__main__":
    minder.main(SerialTest)

