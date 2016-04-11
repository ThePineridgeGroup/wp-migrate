from lib.db_sqlite import db_sqlite
from decimal import *
# neutron-tunneling modules
import cfg, util, flio

class ApplDb(db_sqlite):
    ''' application db routines '''    
    
        
    def create_tbl(self,_tblname):
        '''create table and build columns from csv modules list '''
        if self.table_exists(_tblname):
            print('table {} found, droping it\n'.format(_tblname))
            _a=self.drop_table(_tblname)
        
        # build create line
        _ln='time decimal, keyword text,'
        cfg.cols=['kw_cnt',]
        _ln+=' real, '.join(cfg.cols)+' real'
        
        # Create table
        q='CREATE TABLE {} ({})'.format(_tblname,_ln)
        self.exec_sql(q)
        q='CREATE UNIQUE INDEX {} on {} (time ASC) '.format(_tblname+'idx',_tblname)
        self.exec_sql(q)


        
    def ins_rows(self,_tblname,_rows):
        '''Insert rows to table
        
        _tblname - name of table which rows are inserted
        _rows - a list of column, time, value, one or more rows can be
                inserted at once
        '''
        
        q="insert into {_tbl} (time,{_col}) VALUES ({_time},{_val})".format(_tbl=_tblname,_col=_rows[0],_val=_rows[2],_time=_rows[1])
        _a=self.exec_sql(q)
        #print '(db.ins) row inserted'
        
    def ins_upd_row(self,_tblname,row):
        '''Insert  or update row in table
    
        _tblname - name of table which rows are inserted
        _row - a list of column, time, value, one row only
        '''

        if type(row[1]) != Decimal:
            row[1] = util.fmt_time(row[1])
        
        # update a row of data
        q="update or ignore {_tbl} set {_col}={_val} where time = {_time}".format(_tbl=_tblname,_col=row[0],_time=row[1],_val=row[2])
        _a=self.exec_sql(q)
        
        if self.get_rowcount() == 0:
            if row[0] in cfg.time_adj_signals:
                #tadj=util.fmt_time(row[1])
                tadj=util.fmt_time(row[1]-cfg.time_adj)
                q="update or ignore {_tbl} set {_col}={_val} where time = {_time}".format(_tbl=_tblname,_col=row[0],_time=tadj,_val=row[2])
                #print q
                _a=self.exec_sql(q)
                if self.get_rowcount() == 0:
                    self.ins_rows(_tblname,row)
            else:
                self.ins_rows(_tblname,row)
            
    def purge_rows(self,_tblname):
        ''' Delete the rows before and after the time of interest.
        
            the deletion criteria is:
        '''
        print('(db.purge_rows)')
        pass
        
    def sel_col_rows(self,_tblname,_col,_begt=-999.0,_endt=999.0):
        ''' Select the non null values for for a column rtn list '''
        
        q="select time, {col} from {tbl} where {col} not NULL and time between {bt} and {et}".format(tbl=_tblname,col=_col,bt=_begt,et=_endt)
        #print 'db.sel_col_rows) ',q
        _a=self.exec_sql(q)
        _a=self.get_all()
        
        _rsp=[]
        for _r in _a:
            _rsp.append([Decimal(str(_r[0]),cfg.context),_r[1]])
        return _rsp
        
    def get_start_time(self,_tblname,_col,_val):
        ''' Select the values for for a column rtn list '''
        
        q="select time, {col} from {tbl} where {col} > {val}".format(tbl=_tblname,col=_col,val=_val)
        #print q
        _a=self.db_exec_query(q)

        return [Decimal(str(_a[0]),cfg.context),_a[1]]
    
    def sel_baseline_rows(self,_tblname,_col,_begt=-999.0):
        ''' Select the rows before start time to calc baseline, rtn list '''
        
        q="select time,{col} from {tbl} where {col} not NULL and time < {bt}".format(tbl=_tblname,col=_col,bt=_begt)
        #print 'db.sel_col_rows) ',q
        _a=self.exec_sql(q)
        _a=self.get_all()
        
        _rsp=[]
        for _r in _a:
            _rsp.append([Decimal(str(_r[0]),cfg.context),_r[1]])
        return _rsp

