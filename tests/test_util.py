from __future__ import division, print_function
import sys, os, datetime, time, re
#import pytest
import wp_migrate.cfg as cfg
import wp_migrate.util as util
import wp_migrate.flio as flio
import wp_migrate.wp_migrate as wp_migrate

def setup():
    print("SETUP!")

def teardown():
    print("TEAR DOWN!")

class TestUtil():
        @pytest.fixture(autouse=True)

    def setup(self,):
        '''(util.setup) setup for each test'''


    def test_get_filelist(_path=cfg.path):
        '''(util.get_filelist) get a list of files from directory'''
        fl=os.listdir(cfg.path)
        print('fl:',fl)
        print('cfg:',cfg.inflnm)
        assert cfg.outflnm == fl[0]



