import sys, os
from phileas import _html40 as h

from .base_test import BaseTest
from .serial_test import SerialTest
from .spi_test import SpiTest
from .ping_test import PingTest
from .style import Style


def main(*classes):
    exec_name = sys.argv.pop(0)
    print("running %s" % exec_name)
    html_filename = (sys.argv and sys.argv[0] or
                     (os.path.splitext(exec_name)[0] + '.html'))
    with open(html_filename, 'w') as html_file:
        body = h.body | (h.p | "running %s" % exec_name)
        for class_ in classes:
            inst = class_()
            body |= inst.exercise()
        head = h.head | (h.style | Style())
        print(h.html | (head, body), file=html_file)

if __name__ == "__main__":
    from .target import Target
    main(BaseTest)

