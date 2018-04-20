import sys, os
from phileas import _html40 as h
from .style import Style


def main(*classes):
    """
This is the main program of the 'minder' test and timing package.
It is executed when 'python -m minder' is entered from the command line
or (more usually and more usefully!) by test scripts. Since this file is imported
by __init__.py, such test scripts can access it simply by:
   import minder
   ...
   minder.main([class] ...)
    """

    exec_name = sys.argv.pop(0)
    print("running %s" % exec_name)
    calibrate, reticent, verbose = [sum([(a in alternatives) for a in sys.argv])
                         for alternatives in
                            (('-C', '--calibrate'),
                             ('-R', '--reticent'),
                             ('-V', '--verbose'),
                             )]

    html_filename = (sys.argv and sys.argv[0] or
                     (os.path.splitext(exec_name)[0] + '.html'))
    with open(html_filename, 'w') as html_file:
        body = h.body | (h.p | "running %s" % exec_name)
        for class_ in classes:
            inst = class_(calibrate=calibrate, reticent=reticent, verbose=verbose)
            body |= inst.exercise()
        head = h.head | (h.style | Style())
        print(h.html | (head, body), file=html_file)


if __name__ == '__main__':
    main()
