#!/usr/bin/python3
# -*- coding: utf-8 -*-

import minder
import target


class SpiTest(minder.SpiTest, target.Target):
    def get_flavours(self):
        return None  # no readily available SPI device on pc platform.


if __name__ == "__main__":
    test = SpiTest()
    test.main()
