from __future__ import division, print_function
import sys, os, datetime, time, re
#from nose2.tools import nottest
#from nose2.tools import *
import pytest
import unittest

sys.path.append(os.getcwd())

#print('cur working dir',os.getcwd())
#print('pythonpath:',sys.path)
import wp_migrate.cfg as cfg
import wp_migrate.util as util
import wp_migrate.flio as flio
import wp_migrate.wp_migrate as wp_migrate
import test_data as td


#model object used when adding object & set values
class p_obj:
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)


class IniSetup():

    def __init__(self,):
        '''(int.init) create the test files'''
        self.setup()

    def setup(self,):
        '''(int.setup) create the test files'''

        # set any variables
        cfg.xxx = ''

        print( "\n --- SETUP! --- \n")
        cfg.path='tests/test-files/'
        cfg.old_tbl_prefix='wp_o205dv_'
        cfg.new_tbl_prefix='xx_'
        cfg.old_domain='www.tpginc.net'
        cfg.new_domain='www.testdomain.org'
        cfg.inflnm='test_sql.sql'
        cfg.outflnm='test_sql-new.sql'


        #create the test parm object
        cfg.parms=p_obj(path=cfg.path,td=0.0,fd=0.0,nv='n')


        #create the test data object
        cfg.tdata = p_obj(trec1=td.test_rec1,trec2=td.test_rec2,trec3=td.test_rec3,tsql=td.test_sql)

        # generate test files in folder cfg.path

        if os.path.exists(cfg.path):
            self.delete_test_files()

        #creat test file directory
        os.mkdir(cfg.path)

        # convert text into list
        cfg.newline = os.linesep

        self.build_test_data()


    @unittest.skip('')
    def delete_test_files(self,):
        '''(init.delete_test_files) delete test files and directory'''

        for f in os.listdir(cfg.path):
            try:
                os.remove(cfg.path+f)
            except OSError:
                for fx in os.listdir(cfg.path+f):
                    os.remove(cfg.path+f+'/'+fx)
                os.rmdir(cfg.path+f)
        os.rmdir(cfg.path)

    @unittest.skip('')
    def build_test_data(self,):
        '''(init.build_test_data) Build the test data from test_sql.

        input is file object and filename
        '''

         _sql_list= cfg.tdata.tsql.split(cfg.newline)
        #build test data file
        fl=open(cfg.path+cfg.inflnm,'w')

        for rec in _sql_list:
            fl.write(rec+'\n')
        fl.close()
        return

init = IniSetup()

##@pytest.fixture(scope='session')
#def init():
#    '''create the init class'''
#    global cfg
#    init = IniSetup()
#    return init

##@pytest.fixture(scope='session')
#def setup_cfg():
#    '''(conftest.setup_config) create the test files'''

#    print( "\n --- SETUP cfg! --- \n")
#    cfg.path='tests/test-files/'
#    cfg.old_tbl_prefix='wp_o205dv_'
#    cfg.new_tbl_prefix='xx_'
#    cfg.old_domain='www.tpginc.net'
#    cfg.new_domain='www.testdomain.org'
#    cfg.inflnm='test_sql.sql'
#    cfg.outflnm='test_sql-new.sql'

#    #create the test data object
#    cfg.tdata = p_obj(trec1=td.test_rec1,trec2=td.test_rec2,trec3=td.test_rec3,tsql=td.test_sql)
#    return cfg

#def set_up():
#    '''(int.setup) create the test files'''

#    # set any variables
#    cfg.xxx = ''


##    print("\n --- SETUP! --- \n")
##    cfg.path='tests/test-files/'
##    cfg.old_tbl_prefix='wp_o205dv_'
##    cfg.new_tbl_prefix='xx_'
##    cfg.old_domain='www.tpginc.net'
##    cfg.new_domain='www.testdomain.org'
##    cfg.inflnm='test_sql.sql'
##    cfg.outflnm='test_sql-new.sql'

#    #create cfg.parms object & set values
#    class p_obj:
#        def __init__(self,**kwargs):
#            self.__dict__.update(kwargs)

#    #create the test parm object
#    cfg.parms=p_obj(path=cfg.path,td=0.0,fd=0.0,nv='n')


#    # generate test files in folder cfg.path

#    if os.path.exists(cfg.path):
#        delete_test_files()

#    #creat test file directory
#    os.mkdir(cfg.path)

#    # convert text into list
#    _newline = os.linesep
#    _sql_list= test_sql.split(_newline)
#    #build test data file
#    fl=open(cfg.path+cfg.inflnm,'w')

#    for rec in _sql_list:
#        fl.write(rec+'\n')
#    fl.close()


#def tear_down():
#    '''(int.teardown) remove the test files'''
#    print( "TEAR DOWN!")
#    return
#    #delete_test_files()

##@unittest.skip('')
#def delete_test_files():
#    '''(init.delete_test_files) delete test files and directory'''

#    for f in os.listdir(cfg.path):
#        try:
#            os.remove(cfg.path+f)
#        except OSError:
#            for fx in os.listdir(cfg.path+f):
#                os.remove(cfg.path+f+'/'+fx)
#            os.rmdir(cfg.path+f)
#    os.rmdir(cfg.path)

##@unittest.skip('')
#def build_test_data(_fl,fnm):
#    '''(init.build_test_data) Build the test data from test_sql.

#    input is file object and filename
#    '''

#    _fl.write(fnm+'\n')
#    return


##@pytest.fixture(scope='session')
#def tdata():
#    '''(conftest.test_data) create the test data records'''

#    #create cfg.parms object & set values
#    class p_obj:
#        def __init__(self,**kwargs):
#            self.__dict__.update(kwargs)

#    #create the test parm object
#    data_rec = p_obj(trec1=td.test_rec1,trec2=td.test_rec2,trec3=td.test_rec3,tsql=td.test_sql)
#    return data_rec
