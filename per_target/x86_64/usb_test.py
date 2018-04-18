#!/usr/bin/python3
# -*- coding: utf-8 -*-
import minder
import target


class UsbTest(minder.UsbTest, target.Target):
# can't get this working! ...
#     pre_args = ('sudo', '-S', 0,) + minder.UsbTest.pre_args
#    exec_file = 'echo'  # stub for initial testing
    usbDevice = '/dev/sda2'  # typically Ollivers lightning fast disk (spare partition)
    count =10        # this gets done quick enough for PC target!


if __name__ == "__main__":
    minder.main(UsbTest)
