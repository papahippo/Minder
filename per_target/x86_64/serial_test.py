#!/usr/bin/python3
# -*- coding: utf-8 -*-
import minder
import target


class SerialTest(minder.SerialTest, target.Target):
    device_name_pattern = 'ttyUSB.+'
    ttyPort = '/dev/ttyUSB1'


if __name__ == "__main__":
    minder.main(SerialTest)
