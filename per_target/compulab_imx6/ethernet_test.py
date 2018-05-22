#!/usr/bin/python3
# -*- coding: utf-8 -*-
import minder
import target


class EthernetTest(minder.EthernetTest, target.Target):
    iperf3_hosts = ('192.168.1.42',)


if __name__ == "__main__":
    minder.main(EthernetTest)
