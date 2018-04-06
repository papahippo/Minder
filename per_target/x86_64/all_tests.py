#!/usr/bin/python3
# -*- coding: utf-8 -*-

import minder
from serial_test import SerialTest
from spi_test import SpiTest
from ping_test import PingTest


if __name__ == "__main__":
    minder.main(SerialTest, SpiTest, PingTest)

