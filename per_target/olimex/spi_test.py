#!/usr/bin/python3
# -*- coding: utf-8 -*-

import minder
import target


class SpiTest(minder.SpiTest, target.Target):
    pass


if __name__ == "__main__":
    minder.main(SpiTest)
