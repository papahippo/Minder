"""
The presence of this __init__.py makes minder a python package. It includes a number
of imports so that all test classes can be imported concisely.
"""
from .base_test import BaseTest
from .ping_test import PingTest
from .serial_test import SerialTest
from .spi_test import SpiTest
from .ethernet_test import EthernetTest
from .usb_test import UsbTest
from .curaengine_test import CuraEngineTest
from .style import Style
from .__main__ import main
