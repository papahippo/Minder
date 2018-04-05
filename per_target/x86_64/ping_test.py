#!/usr/bin/python3
# -*- coding: utf-8 -*-
import minder


class PingTest(minder.PingTest):
    pass


if __name__ == "__main__":
    test = PingTest()
    test.main()
