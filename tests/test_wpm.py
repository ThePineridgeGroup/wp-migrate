''' System Test Module

This test will simulate a run with the test data and produce checks to
ensure the results of processing the data are valid.

Any change to the test file data in the init setup  (td_dict) will affect
the tests in this module.  Be sure to adjust the results appropiately.

'''

from __future__ import division, print_function
import sys, os, datetime, time, re
import pytest
import unittest
import wp_migrate.cfg as cfg
import wp_migrate.util as util
import wp_migrate.flio as flio
import wp_migrate.wp_migrate as wp_migrate

#@pytest.mark.usefixtures("setup_cfg")
def test_sample():
    print('(t_wpm)this is a sample.')
    print('newdom',cfg.new_domain)
    print ('tdata-rec3',cfg.tdata.trec3)
    assert cfg.new_domain == 'no domain'
    assert cfg.tdata.trec1 == 'test data'

#@pytest.mark.usefixtures("setup_cfg", "tdata")
class TestWPM():

    #pytest.fixture(autouse=True)


    def setup(self,):
        '''(wpm.setup) setup for each test'''

        self.wpm=wp_migrate.WPMigrate()

        #assert cfg.new_domain == cfg.old_domain

    @unittest.skip('')
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

    def test_edit_rec(self,):
        '''(wpm.test_edit_rec) parsing and editing of a record'''
        print('(test_wpm.pre_pst_proc)')
        print('oldpath',cfg.old_full_path)
        print('newpath',cfg.new_full_path)

        _r = self.wpm.edit_rec(cfg.tdata.trec1)
        print('b4:',repr(cfg.tdata.trec1))
        print('af:',repr(_r))
        print('sb:',repr(cfg.tdata.trec1_b))

        assert _r == cfg.tdata.trec1_b
        assert 0

#        print('test domain')
#        _trec1 = self.wpm.edit_rec(cfg.tdata.tec1)
#        assert cfg.tdata.trec1 == _trec1

#        print('test domain without serialization')
#        _trec3 = self.wpm.edit_rec(cfg.tdata.trec3)
#        assert cfg.tdata.trec3 == _trec3

#        print('test prefix')
#        _trec2 = self.wpm.edit_rec(cfg.tdata.trec2)
#        assert cfg.tdata.trec2 == _trec2

#        print('test full path')
#        _trec3 = self.wpm.edit_rec(cfg.tdata.trec3)
#        assert cfg.tdata.trec3 == _trec3

        assert False == True

    @unittest.skip('')
    def test_debug_parse_rtn(self,):
        '''test code to check the parsing routines'''
        print('(test_wpm.test_debug_parse_rtn)')
        _r = self.trec1_a.replace("""\', ""","~#~#")
        _r = _r.replace("~#~#'a","', 'a")
        _q = re.split(r"\\\'\, ",cfg.tdata.trec1)
        print('split-1',_q)
        _q = re.split(r"\\\'\, ",cfg.tdata.trec4_a)
        print('split-4a',_q)

        _x = re.findall(r'\"*(\\\'\, )*"',cfg.tdata.trec4_a)
        print('find',_x)

        _r = re.sub(r"\'\, ",r"~#~#",cfg.tdata.trec4_a)


    @unittest.skip('')
    def test_process_sql(self,):
        '''(wpm.test_process_sql) test the sql processing (syntax errors)'''
        print('(test_wpm.process)')
        self.wpm.process_sql_file()
        assert True == True



    @unittest.skip('')
    def test_sample_skip(self,):
        '''(wpm.sample_skip) test skip a test'''

        print('(test_wpm.sample_skip)')

        assert True == True






