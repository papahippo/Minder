#!/usr/bin/python3
# -*- coding: utf-8 -*-

import minder
import target

# n.b. to get usable spi device on toradex,  you need to patch the device tree;
# see: https://www.toradex.com/community/questions/13661/imx7d-spidev.htm

class SpiTest(minder.SpiTest, target.Target):
    device_name_pattern = 'spidev.+'    # typically /dev/spidev2.0


if __name__ == "__main__":
    minder.main(SpiTest)
