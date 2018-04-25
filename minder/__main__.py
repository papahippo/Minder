import sys, os
from phileas import html5 as h


def main(*Classes):
    """
This is the main program of the 'minder' test and timing package.
It is executed when 'python -m minder' is entered from the command line
or (more usually and more usefully!) by test scripts. Since this file is imported
by __init__.py, such test scripts can access it simply by:
   import minder
   ...
   minder.main([class] ...)
    """

    script_name = sys.argv.pop(0)
    print("running %s" % script_name)
    calibrate, reticent, verbose = [sum([(a in alternatives) for a in sys.argv])
                                    for alternatives in
                                    (('-C', '--calibrate'),
                                    ('-R', '--reticent'),
                                    ('-V', '--verbose'),
                                     )]
    for Class in Classes:
        inst = Class(script_name=script_name,
                     calibrate=calibrate, reticent=reticent, verbose=verbose)
        inst.exercise()


if __name__ == '__main__':
    # we get here if command 'python3 -m minder ... ' is entered.
    # this does a dummy run with absolutely no test class and produce a skeletal
    # 'minder.__main__.html'. If noting else, it's a quick test of whether minder can be
    # imported!
    #
    main()
