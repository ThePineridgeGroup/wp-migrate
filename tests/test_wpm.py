''' System Test Module

This test will simulate a run with the test data and produce checks to
ensure the results of processing the data are valid.

Any change to the test file data in the init setup  (td_dict) will affect
the tests in this module.  Be sure to adjust the results appropiately.

'''

from __future__ import division, print_function
import sys, os, datetime, time, re
from nose.tools import *
from nose.plugins.skip import SkipTest
import wp_migrate.cfg as cfg
import wp_migrate.util as util
import wp_migrate.flio as ntio
import wp_migrate.wp_migrate as wp_migrate


def setup():
    '''(wpm.setup) setup for nt testing'''
    print("SETUP!")
    global wpm
    wm=wp_migrate.WPMigrate()
    util.config_runparms()
    util.config_setup()



def teardown():
    '''(wpm.teardown) tear down for nt testing'''
    print("TEAR DOWN!")


class TestWPM():

    def setup(self,):
        '''(wpm.setup) setup for each test'''

        pass

    def test_prompts(self,):
        '''(wpm.integrate) verify the integration routine'''
        print('(test_wpm.prompts)')

        #buffer responses to cmd  prompts
        ans_pipe = subprocess.Popen('xxx viewproject',shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, universal_newlines=True)
        _newline = os.linesep
        _responses = ['data/test/','','www.tpginc.net','www.test.net']
        ans_pipe.communicate(_newline.join(_responses))

        wmp.config_parser_values()

        assert_equal(cfg.path,_responses[0])

    @SkipTest
    def test_gen_graphs(self,):
        '''(wpm.gen_graphs) test the graphics'''
        #n.set_db()
        print('(test_wpm.gen_graphs)')

        print('table:',cfg.dbnm,cfg.tblnm)
        #print 'rows:',db.get_num_rows(cfg.tblnm)
        print('sel parms ',cfg.et_col,cfg.et_value)
        #print db.sel_col_rows(cfg.tblnm,'cvr')
        util.set_db()
        util.calc_start_stop()
        print('beg/end time',cfg.tbeg,cfg.tend)
        #assert()

        print('cwd:',os.getcwd())

        assert_equal(False,True)






