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


class TestWPM():

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

    def test_scan_for_old_string(self,):
        '''(wpm.test_scan_for_old_string) return true if old string found'''
        print('(test_wpm.edit_rec)')
        print('oldpath',cfg.old_full_path)
        print('oldurl',cfg.old_url)
        print('olddomain',cfg.old_domain)
        print('rec',cfg.tdata.trec1)
        _a = self.wpm.scan_for_old_strings(cfg.tdata.trec1)
        assert _a == True

    def test_replace_strings(self,):
        '''(wpm.test_replace_strings) replace rec strings'''
        print('(test_wpm.replace_strings)')
        print('oldpath',cfg.old_full_path)
        print('newpath',cfg.new_full_path)

        _r = self.wpm.replace_strings(cfg.tdata.trec1)
        print('b4:',repr(cfg.tdata.trec1))
        print('af:',repr(_r))
        print('sb:',repr(cfg.tdata.trec1_b))

        assert _r == cfg.tdata.trec1_b


    def test_edit_rec(self,):
        '''(wpm.test_edit_rec) parsing and editing of a record'''
        print('(test_wpm.edit_rec)')
        print('oldpath',cfg.old_full_path)
        print('newpath',cfg.new_full_path)

        _r = self.wpm.edit_rec(cfg.tdata.trec1)
        print('b4:',repr(cfg.tdata.trec1))
        print('af:',repr(_r))
        print('sb:',repr(cfg.tdata.trec1_b))

        assert _r == cfg.tdata.trec1_b



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







