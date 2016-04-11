import sqlite3
from .db_wrap import DbWrap
from decimal import *
 
def adapt_decimal(_d):
    return str(_d)
 
def convert_decimal(_s):
    return Decimal(_s)
 
# Register the adapter
sqlite3.register_adapter(Decimal, adapt_decimal)
 
# Register the converter - define type decimal to sqlite
sqlite3.register_converter("decimal", convert_decimal)

import datetime
class db_sqlite(DbWrap) :
        
    #class variables    
    _dbconn=''                   
    _cur=''
    _db=''

    
    '''
     * constructor
    '''
    def __init__(self,_path=None,_db='nt.sqlite',_type='dict'):
        ''' init class and define cursors 
            :memory:
        '''
        #establish connection
        self._dbconn = sqlite3.connect(_path+_db)
        
        #open the cursor for the db    
        self.get_cursor(_type)

    def __del__(self):
        pass
    
    
    def get_cursor(self,ctype='dict'):
        '''
        * get_cursor - unique for each db
        *
        * @returns instance of cursor
        '''
        #init cursor
        if ctype == 'dict':
            self._dbconn.row_factory = sqlite3.Row
             
        self._cur =self._dbconn.cursor() 
        
        return self._cur
    
    def exec_sql(self,_q):
        ''' execute db sql stmt '''
        try:
            self._cur.execute(_q)  
        except Exception as e:
            print("\n* * * * * ",datetime.datetime.now())
            print('  sql stmt:',(_q))
            print(e)
            print("* * * * *")
            raise Exception
            exit()
        return 
        
    def exec_query(self,_q):
        ''' return query result without cursor'''
        self.exec_sql(_q)
        try:
            _a=self._cur.fetchone()
            return _a  
        except:
            return False
            
    def exec_many(self,_q,t):
        ''' execute db many stmt '''
        try:
            self._cur.executemany(_q,t)  
        except Exception as e:
            print("\n* * * * * ",datetime.datetime.now())
            print (_q)
            print(e)
            print("* * * * *")
            raise Exception
            exit()
        return 
            
    def table_exists(self,_tbl):
        '''check if table exists'''
        _q="select tbl_name from sqlite_master where tbl_name like '{}'".format(_tbl,)
        self.exec_sql(_q)
        _a=self._cur.fetchone()
        if (_a) :
            return True
        else :
            return False
    
    def get_col_names(self,_tbl):
        ''' return column names for table'''
        _q="PRAGMA table_info ({})".format(_tbl)
        self.exec_sql(_q)
        _a=self._cur.fetchall()
        _cl=[]
        for k in _a:
            try:
                _cl.append(k[1])
            except:
                _cl.append(k['name'])
            
        if (_a) :
            return _cl
        else :
            return False
            
    
    def col_name_exists(self,_tbl,_col):
        ''' determine if column name exists for table '''
        _col_list=self.get_col_names(_tbl)
        
        if not _col_list:
            print("****")
            print("Invalid database/table passed  - {}".format(_tbl))
            print("****\n")
        
        if _col in _col_list:
            return True
        else :
            return False

    def get_next(self):
        ''' read the db if row found return row else return false  '''
        try:
            _a=self._cur.fetchone()
            return _a
        except:
            return False

    def get_all(self):
        '''read all the rows and return list else return false'''
        try:
            _a=self._cur.fetchall()
            return _a
        except:
            return False

    def clear_table(self,_tbl):
        '''delete rows in table'''
        _q="delete from {0} ".format(_tbl,)
        self.exec_sql(_q)

    def drop_table(self,_tbl):
        '''drop table'''
        _q="drop table {0} ".format(_tbl,)
        self.exec_sql(_q)
    
    def close_cursor(self):
        '''close the cursor'''
        self._cur.close()
        
    def commit(self):
        '''commit work'''
        #_q="commit"
        #self.exec_sql(_q)
        self._dbconn.commit()
    
    def rollback(self):
        ''' rollback work'''
        #_q="rollback"
        #self.exec_sql(_q)
        self._dbconn.rollback()
            
    def get_rowcount(self):
        ''' return number of rows effected by previous stmt '''
        try:
            _a=self._cur.rowcount
            return _a
        except:
            return False
            
    def get_num_rows(self,_tbl):
        """ return number of rows in table"""
        _q="SELECT count(*) as count FROM {0} ".format(_tbl,)
        self.exec_sql(_q)
        _a=self._cur.fetchone()
        if (_a) :
            try:
                return _a[0]
            except:
                return _a['count']
        else :
            return False
           
    
            


        
    

   


