#!/usr/bin/python3
# -*- coding: utf-8 -*-

import minder
from serial_test import SerialTest
from spi_test import SpiTest
from ethernet_test import EthernetTest


if __name__ == "__main__":
    minder.main(SerialTest, SpiTest, EthernetTest)

