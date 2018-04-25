#!/usr/bin/python3
# -*- coding: utf-8 -*-
import minder
import target


class SerialTest(minder.SerialTest, target.Target):
#TODO: overrule run times with shorter values for quick test. done; to be validated.
    device_name_pattern = 'ttyUSB.+'
    tx_secs = 2
    rx_secs = 3


if __name__ == "__main__":
    minder.main(SerialTest)
