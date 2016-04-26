from __future__ import division, print_function
import sys, os, datetime, time, re
from decimal import *
import pytest
import unittest
import wp_migrate.cfg as cfg
import wp_migrate.util as util
import wp_migrate.flio as flio
import wp_migrate.wp_migrate as wp_migrate



class TestProcInput():
    '''(flio.ProcInput) test class interface '''

    def setup(self):
        '''(flio.input.setup) setup for flio testing'''
        print('setup for ProcInput tests')
        self.filename = cfg.inflnm
        print('(io.setup) ',cfg.path, cfg.inflnm)
        self.x=flio.ProcInput(cfg.path,self.filename)
        assert isinstance(self.x.infl,object) == True
        self.rec_cnt=0

    def test_in_interface(self):
        '''(flio.interface) test class interface '''
        #assert self.x == True
        assert isinstance(self.x,object) == True

    def test_get_ifl_rec_str(self):
        '''(flio.get_ifl) test reading record and return str '''
        print('in test_get_ifl_rec')
        print(dir(self.x))
        assert isinstance(self.x.infl,object) == True
        _r = self.x.get_ifl_rec()
        self.rec_cnt += 1
        assert isinstance(_r,str)  == True

    def test_read_ifl_str(self):
        '''(flio.get_ifl) test reading entire file and return unformatted'''
        print('in test_get_ifl - str')
        assert isinstance(self.x.infl,object) == True
        _r = self.x.read_ifl()
        assert isinstance(_r,str) == True

    @unittest.skip('')
    def test_nothing(self):
        '''(flio.nothing) skip test'''
        raise SkipTest
        self.fail("shouldn't happen")


class TestProcOutput():
    '''(flio.ProcOutput) test class interface '''

    def setup(self):
        '''(flio.output.setup) setup for io output testing'''
        print('setup for ProcOutput tests')
        self.filename = 'TST'

        self.x=flio.ProcOutput(cfg.path,self.filename)
        assert isinstance(self.x.ofl,object) == True

    def teardown(self):
        '''(flio.output.teardown) clean up'''
        pass

    def test_out_interface(self):
        '''(flio.output.interface) test class interface '''
        assert isinstance(self.x,object) == True

    def test_write_ofl(self):
        '''(flio.write_ofl) test writing a record to output file'''
        self.x.write_ofl('this is a test line')
        assert True == True
