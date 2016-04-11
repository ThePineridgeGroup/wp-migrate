import sys, os, datetime, time, re
from nose.tools import *
import nt.cfg as cfg
import nt.db as db
import nt.util as util
import nt.ntio as ntio

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

class TestUtil():
    
    def setup(self,):
        '''(util.setup) setup for each test'''
        self.db=db.ApplDb(cfg.path,cfg.dbnm)

    def test_get_filelist(_path=cfg.path):
        '''(util.get_filelist) get a list of files from directory'''
        fl=os.listdir(cfg.path)
        print 'fl:',fl
        assert_equal(util.fnd_file(fl, cfg.testno+'_PINNB.txt'),True)
        #assert_equal(util.fnd_file(fl, 'file1'),False)
        
    
