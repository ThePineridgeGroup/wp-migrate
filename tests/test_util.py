from __future__ import division, print_function
import sys, os, datetime, time, re
from nose.tools import *
import wp_migrate.cfg as cfg
import wp_migrate.util as util
import wp_migrate.flio as ntio
import wp_migrate.wp_migrate as wp_migrate

def setup():
    print("SETUP!")

def teardown():
    print("TEAR DOWN!")

class TestUtil():

    def setup(self,):
        '''(util.setup) setup for each test'''
        self.db=db.ApplDb(cfg.path,cfg.dbnm)

    def test_get_filelist(_path=cfg.path):
        '''(util.get_filelist) get a list of files from directory'''
        fl=os.listdir(cfg.path)
        print('fl:',fl)
        assert_equal(util.fnd_file(fl, cfg.testno+'_PINNB.txt'),True)
        #assert_equal(util.fnd_file(fl, 'file1'),False)


