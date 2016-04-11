import sys, os, datetime, time, re
from decimal import *
from nose.tools import *
from nose import SkipTest
import unittest
import nt.cfg as cfg
import nt.db as db
import nt.util as util
import nt.ntio as ntio

import __init__ as temp


def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"
    
class TestProcInput():
    '''(ntio.ProcInput) test class interface '''
    
    def setup(self):
        '''(ntio.input.setup) setup for ntio testing'''
        print 'setup for ProcInput tests'
        self.filename = cfg.filelist[0]
        print '(ntio.setup) exp:',cfg.expected_infiles,'\n filelist',cfg.filelist,'\n cols: ',cfg.cols,'\n modules: ',cfg.modulelist
        self.x=ntio.ProcInput(cfg.path,self.filename)
        assert_true(isinstance(self.x.infl,object))
        self.rec_cnt=0
    
    def test_in_interface(self):
        '''(ntio.interface) test class interface '''
        assert_true(self.x)
        assert_true(isinstance(self.x,object))

    def test_get_ifl_rec_str(self):
        '''(ntio.get_ifl) test reading record and return str '''
        print 'in test_get_ifl_rec'
        print dir(self.x)
        assert_true(isinstance(self.x.infl,object))
        _r = self.x.get_ifl_rec(fmt='str')
        self.rec_cnt += 1
        assert_true(isinstance(_r,str))
        
    def test_get_ifl_rec_list(self):
        '''(ntio.get_ifl) test reading record and return list'''
        for i in range(0,6):
            _r = self.x.get_ifl_rec()
            self.rec_cnt += 1
        _r = self.x.get_ifl_rec()
        self.rec_cnt += 1
        assert_true(isinstance(_r,list))
        _temp_name= re.split('_|\.',self.filename)
        _cnt=self.rec_cnt-3
        print 'td_key:',_temp_name,'  cnt:',_cnt
        print temp.td_dict[_temp_name[1]][_cnt]
        _irow=temp.td_dict[_temp_name[1]][_cnt].split(' ')
        print '_irow',_irow,_r[0]
        assert_equal(_r[0],Decimal(_irow[0]))
        
    def test_read_ifl_str(self):
        '''(ntio.get_ifl) test reading entire file and return unformatted'''
        print 'in test_get_ifl - str'
        assert_true(isinstance(self.x.infl,object))
        _r = self.x.read_ifl(fmt='str')
        print 'r:',_r
        assert_true(isinstance(_r,str))
    
    def test_read_ifl_list(self):
        '''(ntio.get_ifl) test reading entire file and return list'''
        print 'in test_get_ifl - list'
        assert_true(isinstance(self.x.infl,object))
        _r = self.x.read_ifl()
        print 'r:',_r
        assert_true(isinstance(_r,list))

    @SkipTest    
    def test_nothing(self):
        '''(ntio.nothing) skip test'''
        raise SkipTest
        self.fail("shouldn't happen")


class TestProcOutput():
    '''(ntio.ProcOutput) test class interface '''
    
    def setup(self):
        '''(ntio.output.setup) setup for io output testing'''
        print 'setup for ProcOutput tests'
        self.filename = 'TST'
        
        #test data for output from list
        self.outtbl={-1.086700e-006:-1.365825e+012,-1.086500e-006:-1.365825e+012,-1.086300e-006:4.176158e+012,-1.086100e-006:-1.365825e+012,-1.085900e-006:4.176158e+012,-1.085700e-006:-1.365825e+012,-1.085500e-006:4.176158e+012,-1.085300e-006:4.176158e+012,-1.085100e-006:9.718142e+012}

        self.x=ntio.ProcOutput(cfg.path,self.filename)
        assert_true(isinstance(self.x.ofl,object))
    
        
    def teardown(self):
        '''(ntio.output.teardown) clean up'''
        pass
    
    def test_out_interface(self):
        '''(ntio.output.interface) test class interface '''
        assert_true(self.x)

    def test_write_ofl(self):
        '''(ntio.write_ofl) test writing a record to output file'''
        self.x.write_ofl('this is a test line')
        assert_true(True)
        
    def test_write_ofl_list(self):
        '''(ntio.write_ofl_list) test writing a list to output file'''
        _list=[]
        for k,v in self.outtbl.iteritems():
            _list.append([k,v])
        self.x.write_ofl_list(_list)
        assert_true(True)


def test_file_list():
    '''(ntio.file_list) test if file in list'''
    fl=os.listdir(cfg.path)
    assert_equal(util.fnd_file(fl, cfg.testno+'_CVR.txt'),True)
    assert_equal(util.fnd_file(fl, 'file1'),False)

