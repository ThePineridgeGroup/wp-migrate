import MySQLdb as dbc     #db class - generic
import _mysql_exceptions as db_exc
from .db_wrap import db_wrap
class analysis_db (db_wrap) :
    
    
    '''
    * get_dbconn - unique for each db
    *
    * @returns instance of database connector
    '''
    def get_dbconn(self,_host,_db,_user,_pswd):
        try:
            self._dbconn = dbc.connect(host=_host,db=_db,user=_user,passwd=_pswd)
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
    def get_cursor(self,_db,type='dict',_cnm=''):
        #_cnm used for server side cursor
        #init cursor
        if ( type == 'dict' ):
            try:
                #self._cur =self._dbconn.cursor(dbc.cursors.DictCursor) 
                if _cnm=='':
                    self._cur =self._dbconn.cursor(dbc.cursors.DictCursor)       
                else:
                    self._cur =self._dbconn.cursor(dbc.cursors.SSDictCursor)        
            except db_exc.OperationalError as e:
                print('error on cursor definition')
        elif ( type == 'tuple' ):
            try:
                if _cnm=='':
                    self._cur =self._dbconn.cursor(dbc.cursors.Cursor)
                else:
                    self._cur =self._dbconn.cursor(dbc.cursors.SSCursor) 
            except db_exc.OperationalError as e:
                print('error on cursor definition')
        else:
            print("Invalid cursor type passed to get_cursor")
            exit()
        
        return self._cur
        
    #check if table exists
    def table_exists(self,_tbl):
        _q="show tables like '%s'" % (_tbl,)
        self.db_exec(_q)
        _a=self._cur.fetchone()
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
        _q="""CREATE TABLE IF NOT EXISTS `{0}` (
                  `id` bigint(20) NOT NULL AUTO_INCREMENT,
                  `sysid` char(2) NOT NULL,
                  `freq` decimal(16,7) NOT NULL,
                  `ss` enum('b','e') NOT NULL DEFAULT 'b' COMMENT 'start/stop',
                  `sec` int(11) NOT NULL,
                  `nsec` int(9) NOT NULL,
                  `time` decimal(22,9) NOT NULL,
                  `datetime` char(40) NOT NULL,
                  `amplitude` varchar(500) NOT NULL,
                  `avg_amp` decimal(16,7) NOT NULL DEFAULT '0.0000000',
                  `ovfl_time` decimal(22,9) NOT NULL DEFAULT '0.0000000' COMMENT 'time since last overflow',
                  `ovfl_cnt` bigint(20) NOT NULL DEFAULT '0' COMMENT 'total number of overflows',
                  `ep` enum('y','n') NOT NULL DEFAULT 'n' COMMENT 'event processing',
                  PRIMARY KEY (`id`),
                  UNIQUE KEY `datax2` (`sysid`,`freq`,`sec`,`nsec`,`ss`),
                  UNIQUE KEY `datax` (`sysid`,`ss`,`time`,`freq`),
                  KEY `datax_time` (`sysid`,`time`)
                ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0""".format(_tbl,)
        self.db_exec(_q)
    def create_match_table(self,_tbl='matches'):
        _q="""CREATE TABLE IF NOT EXISTS `{0}` (
                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                `freq` decimal(16,7) NOT NULL,
                `dt_tm` datetime DEFAULT NULL,
                `beg_time` decimal(22,9) NOT NULL,
                `a1` int(1) DEFAULT '0',
                `a1_row_cnt` bigint(20) DEFAULT '0',
                `a2` int(1) DEFAULT '0',
                `a2_row_cnt` bigint(20) DEFAULT '0',
                `a3` int(1) DEFAULT '0',
                `a3_row_cnt` bigint(20) DEFAULT '0',
                `a4` int(1) DEFAULT '0',
                `a4_row_cnt` bigint(20) DEFAULT '0',
                `extracted` enum('y','n') NOT NULL DEFAULT 'n',
                PRIMARY KEY (`id`),
                UNIQUE KEY `matchx` (`beg_time`,`freq`),
                UNIQUE KEY `matchx_a1` (`beg_time`,`freq`,`a1`),
                UNIQUE KEY `matchx_a2` (`beg_time`,`freq`,`a2`),
                UNIQUE KEY `matchx_a3` (`beg_time`,`freq`,`a3`),
                UNIQUE KEY `matchx_a4` (`beg_time`,`freq`,`a4`)
                ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0 """.format(_tbl)
        self.db_exec(_q)
    def create_multifreq_table(self,_tbl='multifreq') :
        _q="""CREATE TABLE IF NOT EXISTS {0} ( 
                `id` bigint(20) NOT NULL AUTO_INCREMENT, 
                `sysid` char(2) NOT NULL,
                `dt_tm` datetime DEFAULT NULL,
                `beg_time` decimal(22,9) NOT NULL,
                `adj` enum('y','n') NOT NULL DEFAULT 'n',
                `row_cnt` smallint(6) NOT NULL DEFAULT '0',
                `extracted` enum('y','n') NOT NULL DEFAULT 'n',
                PRIMARY KEY (`id`),
                UNIQUE KEY `mf_timex` (`sysid`,`beg_time`)
                ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0""".format(_tbl)
        self.db_exec(_q)
    def create_signals_table(self,_tbl='signals'):
        _q="""CREATE TABLE IF NOT EXISTS `{0}` (
                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                `sysid` char(2) NOT NULL,
                `dt_tm` datetime DEFAULT NULL,
                `freq` decimal(16,7) NOT NULL,
                `beg_time` decimal(22,9) NOT NULL DEFAULT '0',
                `end_time` decimal(22,9) NOT NULL DEFAULT '0',
                `duration` decimal(15,9) NOT NULL DEFAULT '0',
                `avg_amp` decimal(16,7) NOT NULL DEFAULT '0',
                `dt_nearest` decimal(15,9) NOT NULL DEFAULT '0'COMMENT 'time to nearest next signal',
                `dt_cluster` decimal(22,9) NOT NULL DEFAULT '0'COMMENT 'duration of a group of signals',
                `multifreq_cnt` int(6) NOT NULL DEFAULT '0' COMMENT 'multifreq cnt at exact time',
                `multifreq_tvar` int(6) NOT NULL DEFAULT '0' COMMENT 'multifreq cnt within freq dist',
                `f_mean` decimal(16,7) NOT NULL DEFAULT '0' COMMENT 'freq weighted mean',
                `f_width` decimal(16,7) NOT NULL DEFAULT '0' COMMENT 'freq std deviation',
                `local` boolean NOT NULL DEFAULT False,
                `ovfl_time` decimal(22,9) NOT NULL DEFAULT '0' COMMENT 'time since last overflow',
                `ovfl_cnt` bigint(20) NOT NULL DEFAULT '0' COMMENT 'total number of overflows',
                `mp` enum('y','n') NOT NULL DEFAULT 'n' COMMENT 'match processing',
                `amplitude` varchar(500) NOT NULL DEFAULT ' ',
                PRIMARY KEY (`id`),
                UNIQUE KEY `eventx` (`sysid`,`freq`,`beg_time`, `id`),
                KEY `eventx_time` (`sysid`,`beg_time`)
            ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0""".format(_tbl)
        self.db_exec(_q)
        
    def create_stationcoord_table(self,_tbl='stationcoord'):
        _q="""CREATE TABLE IF NOT EXISTS `{0}` ( 
                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                `sysid` char(2) NOT NULL COMMENT 'observation station id', 
                `sec` int(11) NOT NULL, 
                `dt_tm` datetime NOT NULL COMMENT 'UTC value of sec', 
                `latitude` double NOT NULL COMMENT 'decimal degree', 
                `longitude` double NOT NULL COMMENT 'decimal degree',
                `altitude` double NOT NULL COMMENT 'meters', 
                PRIMARY KEY (`id`), 
                UNIQUE KEY `last_loc` (`sysid`,`sec`) 
            ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0""".format(_tbl)
        self.db_exec(_q)
        
    def create_stations_table(self,_tbl='stations'):
        _q="""CREATE TABLE IF NOT EXISTS `{0}` (
                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                `sysid` varchar(64) NOT NULL,
                `vpn_ip` varchar(64) DEFAULT NULL,
                `vpn_name` varchar(64) DEFAULT NULL,
                PRIMARY KEY (`id`),
                UNIQUE KEY station_id (`sysid`)
            )ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0""".format(_tbl)
        self.db_exec(_q)
        
    def create_station_status_table(self,_tbl='station_status'):
        _q="""CREATE TABLE IF NOT EXISTS `{0}` (
                `id` bigint(20) NOT NULL AUTO_INCREMENT,
                `dt_tm` datetime NOT NULL,
                `sysid` varchar(64) NOT NULL,
                `cpu_temp` decimal(5,2) NOT NULL DEFAULT '0.00',
                `mb_temp` decimal(5,2) NOT NULL DEFAULT '0.00',
                `max_core_temp` decimal(5,2) NOT NULL DEFAULT '0.00',
                `sensors_info` text,
                `comm_status` int(1) DEFAULT NULL,
                PRIMARY KEY (`id`),
                UNIQUE KEY `dt_sys` (`dt_tm`,`sysid`)
            )ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0""".format(_tbl)
        self.db_exec(_q)
        
    def create_signal_clusters_table(self,_tbl='signal_clusters'):
        _q="""CREATE TABLE IF NOT EXISTS `{0}` (
          `id` bigint(20) NOT NULL AUTO_INCREMENT,
          `sysid` char(2) NOT NULL,
          `beg_time` decimal(20,9) NOT NULL,
          `end_time` decimal(20,9) NOT NULL DEFAULT '0.0000000',
          `duration` decimal(20,9) NOT NULL DEFAULT '0.0000000',
          `mf_cnt` int(11) NOT NULL DEFAULT '0' COMMENT 'cnt of multi-freq events in cluster',
          `freq_cnt` int(11) NOT NULL DEFAULT '0' COMMENT 'non-adjacent frequencies in cluster',
          `avg_cluster_time` decimal(20,9) NOT NULL DEFAULT '0.000000000' COMMENT 'avg cluster time',
          `local` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'local signal, > x secs',
          `primord` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'primord like signal',
          `min_freq` decimal(16,7) not NULL DEFAULT '0' COMMENT 'Min Freq',
          `max_freq` decimal(16,7) not NULL DEFAULT '0' COMMENT 'Max Freq',
          `min_avg_amp` decimal(16,7) not NULL DEFAULT '0' COMMENT 'Min Avg_Amp',
          `max_avg_amp` decimal(16,7) not NULL DEFAULT '0' COMMENT 'Max Avg_Amp',
          PRIMARY KEY (`id`),
          UNIQUE KEY `cluster_sid_bt` (`sysid`,`beg_time`),
          KEY `cluster_sid_et` (`sysid`,`end_time`),
          KEY `cluster_sid_primord` (`sysid`,`primord`)
        ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0""".format(_tbl)
        self.db_exec(_q)
    
    #------------------------------------------------------
    #table maintence
    #
    def check_colum_maint(self,_db,_tbl,_chg):
        ''' check to see if table has been modified for new columns'''
        _rtn=False
        
        #test by function
        if _chg == 'ww':
            #test for changes for weighted width
            if not self.col_name_exists(_db,_tbl,'f_mean'):
                self.add_ww_columns(_tbl)
                #print 'adding for',_tbl
                _rtn=True
        return _rtn
        
    def add_ww_columns(self,_tbl):
        '''add new fields weighted width calc'''
        _q='''
            ALTER TABLE {tbl} 
            ADD `multifreq_tvar` int( 6 ) NOT NULL DEFAULT '0.0' COMMENT 'multifreq cnt within freq dist' AFTER `multifreq_cnt` ,
            ADD `f_mean` DECIMAL( 19,7 ) NOT NULL DEFAULT '0.0' COMMENT 'freq weighted mean' AFTER `multifreq_tvar` ,
            ADD `f_width` DECIMAL( 19,7 ) NOT NULL DEFAULT '0.0' COMMENT 'freq std deviation' AFTER `f_mean`  ;
            '''.format(tbl=_tbl)

        self.db_exec(_q)

   


