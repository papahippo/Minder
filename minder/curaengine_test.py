#!/usr/bin/python3
# -*- coding: utf-8 -*-
from .base_test import BaseTest
import re, os
import tempfile
class CuraEngineTest(BaseTest):
    exec_dir = 'bin/'  # under review
    exec_file = 'CuraEngine'
    pre_args = ('nice', '-n-15')
    showOut = True
    times_over = 3
    model_dir = 'test_models'
    model_files = ('testModel.stl',
                   'robot_v2_support.stl',
                   'Dragon.stl',
                   'BigKnot.stl',
                   'TriangleForest.stl',
                   )

    def prepare(self):
        BaseTest.prepare(self)
        self.temp_dir = tempfile.mkdtemp(prefix='curaengine_test_')

    def get_flavours(self):
        return self.model_files

    def get_args(self, flavour):
        output_gcode = os.path.join(self.temp_dir,
                                    "EnginePerfTest-{model}.gcode".format(
                                        model=flavour
                                    )
                                    )
        return ('slice', '-v',
                '-j', 'definitions/fdmprinter.def.json',
                '-l', 'test_models/'+flavour,
                '-o', output_gcode,
                )

    def arrange_args_for_table(self, flavour):
        return ('Model', flavour),

    def inspect(self, flavour, rc, output, stats):
        result = re.search(r'\nTotal time elapsed\s+([-+]?[\d]*\.?[\d]+)',
                           output)
        time_elapsed = result and eval(result.groups()[0]) or None

        # simplistic for now...
        return time_elapsed, (('time elapsed', time_elapsed),)

    def summarize(self, flavour, stats):
        avg_elapsed_time = sum(stats) / len(stats)
        print ("=============", avg_elapsed_time)
        return ('avg. elapsed time', "%.2f" % avg_elapsed_time),
