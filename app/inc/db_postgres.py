import psycopg2 as dbc              #db class
import psycopg2.extensions as db_ext
import psycopg2.extras as db_extra
from .db_wrap import db_wrap
class analysis_db (db_wrap) :
    
    '''
    * get_dbconn - unique for each db
    *
    * @returns instance of database connector
    '''
    def get_dbconn(self,_host,_db,_user,_pswd):
        try:
            self._dbconn = dbc.connect(host=_host,database=_db,user=_user,password=_pswd)
        except Exception as e:
            print('***')
            print('  error on connect ',_host,_db,_user,_pswd)
            print('***')
            raise Exception(e)
            exit()
        return
    
    '''
    * get_cursor - unique for each db
    *
    * @returns instance of cursor
    '''
    def get_cursor(self,_db,_type='dict',_cnm=''):
        #init cursor
        if  _type == 'dict' :
            try:
                if _cnm:
                   self._cur =self._dbconn.cursor(_cnm,cursor_factory=db_extra.RealDictCursor)
                else:
                    self._cur =self._dbconn.cursor(cursor_factory=db_extra.RealDictCursor)                     
            except Exception as e:
                print('*** error on cursor definition (dict)')
                raise Exception(e)
                exit()
        elif  _type == 'tuple' :
            try:
                if _cnm:
                   self._cur =self._dbconn.cursor(_cnm)  
                else:
                    self._cur =self._dbconn.cursor()       
            except Exception as e:
                print('*** error on cursor definition (tuple)')
                raise Exception(e)
                exit()
        else:
            print("Invalid cursor type passed to get_cursor")
            exit()
        
        return self._cur
    
    def create_types(self):
        if not self.type_exists("start_stop"):
            _q=""" create type "start_stop" as ENUM('b','e') """
            self.db_exec(_q)
        if not self.type_exists("y_n"):
            _q=""" create type "y_n" as ENUM('y','n') """
            self.db_exec(_q)
    
    #check if table exits
    def table_exists(self,_tbl):
        _q="select exists(select * from pg_tables where tablename = '{0}')".format(_tbl)
        self.db_exec(_q)
        #_a=bool(self._cur.fetchone()[0])
        _a=self._cur.fetchone()
        
        #if result is real dict or tuple
        try:
            _a=bool(_a[0])
        except:
            _a=bool(_a['?column?'])

        if (_a) :
            return True
        else :
            return False
    
    #check if data type exits
    def type_exists(self,_data):
        _q="select exists(select * from pg_type where typname = '{0}')".format(_data)
        self.db_exec(_q)
        _a=self._cur.fetchone()
        #if result is real dict or tuple
        try:
            _a=bool(_a[0])
        except:
            _a=bool(_a['?column?'])
            
        if (_a) :
            return True
        else :
            return False
            
    #return column names for table
    def get_col_names(self,_db,_tbl):
        _q="select column_name from information_schema.columns where table_schema = '%s' and table_name = '%s'" % (_db,_tbl)
        self.db_exec(_q)
        _a=self._cur.fetchall()
        _cl=[]
        for k in _a:
            try:
                _cl.append(k[0])
            except:
                _cl.append(k['column_name'])
            
        if (_a) :
            return _cl
        else :
            return False
        
    #determine if column name exists for table
    def col_name_exists(self,_db,_tbl,_col):
        _col_list=self.get_col_names(_db,_tbl)
        
        if not _col_list:
            print("****")
            print("Invalid database/table passed ",_db,' - ',_tbl)
            print("****\n")
        
        if _col in _col_list:
            return True
        else :
            return False
    
    def create_data_table(self,_tbl='data'):
        self.create_types()
        _q="""CREATE TABLE IF NOT EXISTS "{0}" (
                  "id" serial NOT NULL,
                  "sysid" char(2) NOT NULL,
                  "freq" decimal(16,7) NOT NULL,
                  "ss" start_stop NOT NULL DEFAULT 'b',
                  "sec" bigint NOT NULL,
                  "nsec" integer NOT NULL,
                  "time" decimal(22,9) NOT NULL,
                  "datetime" char(40) NOT NULL,
                  "amplitude" varchar(500) NOT NULL,
                  "avg_amp" decimal(16,7) NOT NULL DEFAULT '0.0000000',
                  "ovfl_time" decimal(22,9) NOT NULL DEFAULT '0.0000000',
                  "ovfl_cnt" bigint NOT NULL DEFAULT '0' ,
                  "ep" y_n NOT NULL DEFAULT 'n' ,
                  PRIMARY KEY ("id"),
                  UNIQUE  ("sysid","freq","sec","nsec","ss"),
                  UNIQUE ("sysid","ss","time","freq")
                )""".format(_tbl)
        self.db_exec(_q)
        _q="create index {0}_time on {0} (sysid,time)".format(_tbl)
        self.db_exec(_q)
    def create_match_table(self,_tbl='matches'):
        self.create_types()
        _q="""CREATE TABLE IF NOT EXISTS "{0}" (
                "id" serial NOT NULL,
                "freq" decimal(16,7) NOT NULL,
                "dt_tm" timestamp with time zone DEFAULT NULL,
                "sec" bigint NOT NULL,
                "nsec" integer NOT NULL,
                "beg_time" decimal(22,9) NOT NULL,
                "datetime" char(40) NOT NULL,
                "a1" smallint DEFAULT '0',
                "a1_row_cnt" integer DEFAULT '0',
                "a2" smallint DEFAULT '0',
                "a2_row_cnt" integer DEFAULT '0',
                "a3" smallint DEFAULT '0',
                "a3_row_cnt" integer DEFAULT '0',
                "a4" smallint DEFAULT '0',
                "a4_row_cnt" integer DEFAULT '0',
                "extracted" y_n NOT NULL DEFAULT 'n',
                PRIMARY KEY ("id"),
                UNIQUE ("beg_time","freq")
                )""".format(_tbl) 
        self.db_exec(_q)
        
    def create_multifreq_table(self,_tbl='multifreq') :
        self.create_types()
        _q="""CREATE TABLE IF NOT EXISTS {0} ( 
                "id"serial NOT NULL, 
                "sysid" char(2) NOT NULL,
                "dt_tm" timestamp with time zone DEFAULT NULL,
                "sec" bigint NOT NULL,
                "nsec" integer NOT NULL,
                "beg_time" decimal(22,9) NOT NULL,
                "adj" y_n NOT NULL DEFAULT 'n',
                "row_cnt" smallint NOT NULL DEFAULT '0',
                "extracted" y_n NOT NULL DEFAULT 'n',
                PRIMARY KEY ("id"),
                UNIQUE ("sysid","beg_time")
                ) """.format(_tbl)
        self.db_exec(_q)
        
    def create_signals_table(self,_tbl='signals'):
        self.create_types()
        _q="""CREATE TABLE IF NOT EXISTS "{0}" (
                "id" serial NOT NULL,
                "sysid" char(2) NOT NULL,
                "dt_tm" timestamp with time zone DEFAULT NULL,
                "freq" decimal(16,7) NOT NULL,
                "beg_time" decimal(22,9) NOT NULL DEFAULT '0.0000000',
                "end_time" decimal(22,9) NOT NULL DEFAULT '0.0000000',
                "duration" decimal(22,9) NOT NULL DEFAULT '0.0000000',
                "avg_amp" decimal(16,7) NOT NULL DEFAULT '0.0000000',
                "dt_nearest" decimal(15,9) NOT NULL DEFAULT '0',
                "dt_cluster" decimal(22,9) NOT NULL DEFAULT '0',
                "multifreq_cnt" integer NOT NULL DEFAULT '0',
                "multifreq_tvar" integer(6) NOT NULL DEFAULT '0',
                "f_mean" decimal(16,7) NOT NULL DEFAULT '0',
                "f_width" decimal(16,7) NOT NULL DEFAULT '0',
                "local" boolean NOT NULL DEFAULT False,
                "ovfl_time" decimal(22,9) NOT NULL DEFAULT '0.0000000' ,
                "ovfl_cnt" bigint NOT NULL DEFAULT '0' ,
                "mp" y_n NOT NULL DEFAULT 'n' ,
                "amplitude" varchar(500) NOT NULL DEFAULT ' ',
                PRIMARY KEY ("id"),
                UNIQUE ("sysid","freq","beg_time", "id")
                ) """.format(_tbl)
        self.db_exec(_q)
        _q="""create index {0}x_time on {0}("sysid","beg_time")""".format(_tbl)
        self.db_exec(_q)
        
    def create_stationcoord_table(self,_tbl='stationcoord'):
        _q="""CREATE TABLE IF NOT EXISTS "{0}" ( 
                "id" serial NOT NULL,
                "sysid" char(2) NOT NULL , 
                "dt_tm" timestamp with time zone NOT NULL, 
                "latitude" double precision NOT NULL , 
                "longitude" double precision NOT NULL ,
                "altitude" double precision NOT NULL , 
                PRIMARY KEY ("id"), 
                UNIQUE  ("sysid","time") 
            ) """.format(_tbl)
        self.db_exec(_q)
        
    def create_stations_table(self,_tbl='stations'):
        _q="""CREATE TABLE IF NOT EXISTS "{0}" (
                "id" serial NOT NULL PRIMARY KEY,
                "sysid" varchar(64) NOT NULL UNIQUE,
                PRIMARY KEY ("id"),
                UNIQUE ("sysid")
            )""".format(_tbl)
        self.db_exec(_q)

