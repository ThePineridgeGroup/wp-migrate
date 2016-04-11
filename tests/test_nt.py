''' System Test Module

This test will simulate a run with the test data and produce checks to
ensure the results of processing the data are valid.

Any change to the test file data in the init setup  (td_dict) will affect
the tests in this module.  Be sure to adjust the results appropiately.

'''
import sys, os, datetime, time, re
from nose.tools import *
from nose.plugins.skip import SkipTest
import nt.cfg as cfg
import nt.db as db
import nt.util as util
import nt.ntio as ntio
import nt.nt as nt
import importlib


def setup():
    '''(nt.setup) setup for nt testing'''
    print "SETUP!"
    global n
    n=nt.NTProcess()
    util.config_runparms()
    util.config_setup()

    #set the db connector, if cfg tests have not been run, then cfg.db
    # will not exist 
    global db
    #db=cfg.db
    db=db.ApplDb(cfg.path,cfg.dbnm)


def teardown():
    '''(nt.teardown) tear down for nt testing'''
    print "TEAR DOWN!"
    

class TestNT():
    
    def setup(self,):
        '''(nt.setup) setup for each test'''

        pass
        
    def test_integrate_y(self,):        
        '''(nt.integrate) verify the integration routine'''
        print '(test_nt.integrate_y)'
        
        _src=[[2,10],[4,20],[5,30],[7,20],[9,10],[11,20],[12,30],[14,10]]
        _i=[0,2,1,2,2]       #dif between src[:][0] items
        _ans=[[2,0],[4,40],[5,70],[7,110],[9,130],[11,170],[12,200],[14,220]]

        _modpkg='nt'
        _module='plot_default'
        try:
            g = importlib.import_module('.'+_module,_modpkg)
            print '  Found  {} & running'.format(_module) 
        except ImportError:
            print '  {} not found'.format(_module)
        v=g.Plot()
        _a=v.integrate_y(_src)
        assert_equal(_ans,_a)

    @SkipTest
    def test_gen_graphs(self,):
        '''(nt.gen_graphs) test the graphics'''
        #n.set_db()
        print '(test_nt.gen_graphs)'
        
        print 'table:',cfg.dbnm,cfg.tblnm
        #print 'rows:',db.get_num_rows(cfg.tblnm)
        print 'sel parms ',cfg.et_col,cfg.et_value
        #print db.sel_col_rows(cfg.tblnm,'cvr')
        util.set_db()
        util.calc_start_stop()
        print 'beg/end time',cfg.tbeg,cfg.tend
        #assert()
        
        
        print 'cwd:',os.getcwd()
        _modpkg='nt'

        for _mod in cfg.modulelist:    #.iteritems():
            m = 'plot_'+_mod
            print '    Looking for {:.<15s}.....'.format(m),
            #if _mod == 'V02':
            #    g = importlib.import_module('.'+m,_modpkg)
            try:
                g = importlib.import_module('.'+m,_modpkg)
                print '  Found  {} & running'.format(m) 
                g.main(_mod)
            except ImportError:
                print '  {} not found'.format(m)
            except:
                raise
                assert()
        
        assert_equal(False,True)
        
        
    
        
    

