#!/usr/bin/python3
# -*- coding: utf-8 -*-
import minder
import target


class UsbTest(minder.UsbTest, target.Target):
    usbDevice = '/dev/sda2'  # typically Ollivers lightning fast disk (spare partition)
    count = 10


if __name__ == "__main__":
    minder.main(UsbTest)
