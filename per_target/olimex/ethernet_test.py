#!/usr/bin/python3
# -*- coding: utf-8 -*-
import minder
import target


class EthernetTest(minder.EthernetTest, target.Target):
    iperf4_hosts = ('10.183.3.136',)


if __name__ == "__main__":
    minder.main(EthernetTest)
