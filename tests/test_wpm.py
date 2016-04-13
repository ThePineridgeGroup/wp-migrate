''' System Test Module

This test will simulate a run with the test data and produce checks to
ensure the results of processing the data are valid.

Any change to the test file data in the init setup  (td_dict) will affect
the tests in this module.  Be sure to adjust the results appropiately.

'''

from __future__ import division, print_function
import sys, os, datetime, time, re
import pytest
#from nose2.tools import *
#from nose2.plugins.skip import SkipTest
import unittest
import wp_migrate.cfg as cfg
import wp_migrate.util as util
import wp_migrate.flio as flio
import wp_migrate.wp_migrate as wp_migrate


def setup():
    '''(wpm.setup) setup for  testing'''
    print("SETUP!")
    global wpm
    wpm=wp_migrate.WPMigrate()



def teardown():
    '''(wpm.teardown) tear down for  testing'''
    print("TEAR DOWN!")


class TestWPM():

    def setup(self,):
        '''(wpm.setup) setup for each test'''

        self.wpm=wp_migrate.WPMigrate()

        pass

    #@unittest.skip('')
    def test_prompts(self,):
        '''(wpm.test_prompts) verify the prompt routines'''
        print('(test_wpm.prompts)')

        #buffer responses to cmd  prompts
#        ans_pipe = subprocess.Popen('xxx viewproject',shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, universal_newlines=True)
#        _newline = os.linesep
#        _responses = ['data/test/','','www.tpginc.net','www.test.net']
#        ans_pipe.communicate(_newline.join(_responses))

#        wpm.config_parser_values()

#        assert cfg.path,_responses[0])

    def test_process_sql(self,):
        '''(wpm.test_process_sql) test the sql processing '''
        print('(test_wpm.process)')
        self.wpm.process_sql_file()
        assert False == True

    def test_edit_rec(self,):
        '''(wpm.test_process_sql) test the sql processing '''
        print('(test_wpm.edit_rec)')
        print('test domain')
        _trec1 = self.wpm.edit_rec(init.test_rec1)
        assert init.test_rec1 == _trec1

        print('test domain without serialization')
        _trec3 = self.wpm.edit_rec(test_rec3)
        assert test_rec3 == _trec3

        print('test prefix')
        _trec2 = self.wpm.edit_rec(test_rec2)
        assert test_rec2 == _trec2

        print('test full path')
        _trec3 = self.wpm.edit_rec(test_rec3)
        assert test_rec3 == _trec3

        assert False == True


    #@unittest.skip('')
    def test_sample_skip(self,):
        '''(wpm.sample_skip) test skip a test'''

        print('(test_wpm.sample_skip)')

        assert False == True






