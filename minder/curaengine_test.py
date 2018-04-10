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
    times_over = 2
    model_dir = 'test_models'
    model_files = ('testModel.stl',
                 'TriangleForest.stl',
                 'robot_v2_support.stl',
                 'BigKnot.stl',
                 'Dragon.stl,'
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
        return zip(('Model', flavour),)

    def inspect(self, flavour, rc, output, stats):
        result = re.search(r'\dTotal time elapsed\s+([-+]?[\d]*\.?[\d]+)',
                           output)
        time_elapsed, = result and result.groups() or None,
        return "width:100%", (('time elapsed',),
                              (time_elapsed,)
                              )
