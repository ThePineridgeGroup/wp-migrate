import sys, os, datetime, time, re
from nose.tools import *
from nose import SkipTest
import unittest
import nt.cfg as cfg
import nt.db as db
import nt.util as util
import nt.ntio as ntio


def setup():
    print "test db SETUP!"
    global db
    db=db.ApplDb(cfg.path,cfg.dbnm)

        #build common table for test
    db.create_tbl(cfg.tblnm)
    db.commit()
    cfg.db=db
    
    for filename in cfg.filelist:  #[0:3]:
        #self.filename = cfg.filelist[0]
        filename = filename
        colname = util.parse_col_from_file(filename)
        x=ntio.ProcInput(cfg.path,filename)
        _r = x.read_ifl()
        hdr_cnt = 0
        
        for row in _r:
            if row[0] == 'hdr':
                hdr_cnt +=1
            else:
                _rv=[colname,row[0],row[1]]
                db.ins_upd_row(cfg.tblnm,_rv)
        db.commit()
        print 'number ins for {:8s}:  {} : {}'.format(colname,len(_r)-hdr_cnt,db.get_num_rows(cfg.tblnm))
    assert_equal(405,db.get_num_rows(cfg.tblnm))

def teardown():
    print "TEAR DOWN!"
    
class TestApplDb():
    '''(db.Appldb) test class interface '''
    
    def setup(self):
        '''setup for db testing'''
        self.db=db
        #self.db=db.ApplDb(cfg.path,cfg.dbnm)
    
    def test_db_interface(self):
        '''(db.interface) test class interface '''
        print cfg.path,cfg.dbnm
        assert_true(isinstance(self.db,object))


    def test_ins_row(self):
        '''(db.ins_row) insert a row'''
        

        assert_true(isinstance(self.db,object))
        
    def test_ins_upd_row(self):
        '''(db.ins_upd_row) test insert/update of row'''
        itblnm='tinsupd'
        _data=[('v02',-7.24699900e-07,395545),
            ('v02',-7.24300000e-07,351258.9),
            ('v02',-7.23899900e-07,344330.8),
            ('v02',-7.23500000e-07,314207.1),
            ('v02',-7.23099900e-07,278609.8),
            ('cvr',-7.24300000e-07,9520.694),
            ('cvr',-7.23900000e-07,9380.003),
            ('cvr',-7.23500000e-07,10162.6),
            ('pvdot1',-7.24500000e-07,1.09114E+12),
            ('pvdot1',-7.24300000e-07,-1.72708E+12),
            ('pvdot1',-7.24100000e-07,1.09114E+12),
            ('pvdot1',-7.23900000e-07,1.09114E+12),
            ('pvdot1',-7.23700000e-07,-1.72708E+12),
            ('pvdot1',-7.23500000e-07,-1.72708E+12),
            ('pvdot1',-7.23300000e-07,1.09114E+12),
        ]
        _dmin=-7.247e-7
        _dmax=-7.231e-7
        _dnum_rows=9
        _v02_c=5
        _cvr_c=3
        _pvdot1_c=7

        
        self.db.create_tbl(itblnm)
        self.db.commit()
        
        assert_true(isinstance(self.db,object))
        
        print 'table {} exists: {}'.format(itblnm,self.db.table_exists(itblnm))
        assert_true(self.db.table_exists(itblnm))

        #load the data
        for d in _data:
            _rv=[d[0],d[1],d[2]]
            self.db.ins_upd_row(itblnm,_rv)
        self.db.commit()
            
        assert_equal(_dnum_rows,self.db.get_num_rows(itblnm))
        
        _q='SELECT count(*) as count FROM {tbl} where {col} not NULL'.format(tbl=itblnm,col='v02')
        assert_equal(_v02_c,self.db.exec_query(_q)['count'])
        
        _q='SELECT count(*) as count FROM {tbl} where {col} not NULL'.format(tbl=itblnm,col='cvr')
        assert_equal(_cvr_c,self.db.exec_query(_q)['count'])
        
        _q='SELECT count(*) as count FROM {tbl} where {col} not NULL'.format(tbl=itblnm,col='pvdot1')
        assert_equal(_pvdot1_c,self.db.exec_query(_q)['count'])


    @nottest
    def test_original_ins_upd_row():
        '''keep until new ins_upd code is working'''
        for filename in cfg.filelist:  #[0:3]:
            #self.filename = cfg.filelist[0]
            self.filename = filename
            self.colname = util.parse_col_from_file(self.filename)
            self.x=ntio.ProcInput(cfg.path,self.filename)
            _r = self.x.read_ifl()
            hdr_cnt = 0
            
            for row in _r:
                if row[0] == 'hdr':
                    hdr_cnt +=1
                else:
                    _rv=[self.colname,row[0],row[1]]
                    self.db.ins_upd_row(cfg.tblnm,_rv)
            self.db.commit()
            print 'number ins for {:8s}:  {} : {}'.format(self.colname,len(_r)-hdr_cnt,self.db.get_num_rows(cfg.tblnm))
        assert_equal(377,self.db.get_num_rows(cfg.tblnm))
        assert_true(isinstance(self.db,object))

    def test_sel_col_rows(self):
        '''(db.sel_col_rows) return all rows where column value not null'''
        
        _a = self.db.sel_col_rows(cfg.tblnm,'cvr')
        #_a = self.db.get_all()
        print _a
        
        assert_true(isinstance(_a,list))
