import sys, os
from phileas import html4 as h
import datetime
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
    # TODO: name should include date and time - implemented 25apr18 to be validated!
    s_now = str(datetime.datetime.now()).replace(' ', '_')
    if not s_now.startswith('20'):
        print("WARNING: date not set; perhaps you ought to do (e.g.) 'ntpdate' first?")
    html_filename = (sys.argv and sys.argv[0] or
                     (os.path.splitext(exec_name)[0] + '_' + s_now[:19] + '.html'))
    with open(html_filename, 'w') as html_file:
        body = h.body | (h.p | "running %s" % exec_name)
        for class_ in classes:
            inst = class_(calibrate=calibrate, reticent=reticent, verbose=verbose)
            body |= inst.exercise()
        head = h.head | (h.style | Style())
        print(h.html | (head, body), file=html_file)


if __name__ == '__main__':
    # we get here if command 'python3 -m minder ... ' is entered.
    # this does a dummy run with absolutely no test class and produce a skeletal
    # 'minder.__main__.html'. If noting else, it's a quick test of whether minder can be
    # imported!
    #
    main()
