#!/usr/bin/python3
# -*- coding: utf-8 -*-

import minder
import target

class SerialTest(minder.SerialTest, target.Target):
    device_name_pattern = 'ttymxc0'  # this seems to correspond to UART1 ... i.e. it works!


if __name__ == "__main__":
    minder.main(SerialTest)

