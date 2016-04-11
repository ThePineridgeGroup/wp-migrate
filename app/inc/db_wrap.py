import time, datetime
class DbWrap(object):
    '''
    /**
     *
     * File Description:Data Base Class to allow easy and clean access to common commands for both Postgres & MySQL db
     * @author			The Pineridge Group, LLC (with thanks to ricocheting for code base)
     * @link			http://www.tpginc.net/
     * @version			3.2 
     * @lastmodified	2012-06-15
     * @copyright 		2012 The Pineridge Group, LLC
     *     *
     * @license 	http://opensource.org/licenses/gpl-license.php GNU Public License
     */

      
    /**  
     * Usage
     * <code>
     
     * </code>
     */
    '''


    #class variables
    _dbconn=''                   
    _cur=''
    _db=''

    '''
     * constructor
    '''
    def __init__(self,_host='',_db='',_user='',_pswd='',_type='dict',_cnm=''):
		#init datbase
        self._db=_db
        #get data base connection
        self.get_dbconn(_host,_db,_user,_pswd)
        
        #open the cursor for the db    
        self.get_cursor(_db,_type,_cnm)

    def __del__(self):
        pass
    
        
     #close the cursor
    def db_close_cursor(self):
        self._cur.close()
        
    '''
     * get_instance - create a new instance or get an existing instance
     *
     * singleton declaration
     * @returns instance of database link

    '''
    #return query result without cursor
    def db_exec_query(self,_q):
        self.db_exec(_q)
        try:
            _a=self._cur.fetchone()
            return _a  
        except:
            return False
            
    #execute db sql stmt
    def db_exec(self,_q):
        try:
            self._cur.execute(_q)  
        except Exception as e:
            print("\n* * * * * ",datetime.datetime.now())
            print (_q)
            print(e)
            print("* * * * *")
            raise Exception
            exit()
        return 
        
    #return number of rows effected by previous stmt   
    def db_get_rowcount(self):
        try:
            _a=self._cur.rowcount
            return _a
        except:
            return False
            
    #read the db if row found return row else return false    
    def db_get_next(self):
        try:
            _a=self._cur.fetchone()
            return _a
        except:
            return False
    
    #read all the rows and return list else return false    
    def db_get_all(self):
        try:
            _a=self._cur.fetchall()
            return _a
        except:
            return False

    #delete rows in table
    def clear_table(self,_tbl):
        #print "clearing table - please wait"
        _q="delete from {0} ".format(_tbl,)
        self.db_exec(_q)

    #drop table
    def drop_table(self,_tbl):
        #print "dropping table - please wait"
        _q="drop table {0} ".format(_tbl,)
        self.db_exec(_q)
    
    #commit
    def db_commit(self):
        _q="commit"
        self.db_exec(_q)
    
    #rollback
    def db_rollback(self):
        _q="rollback"
        self.db_exec(_q)
            
    #return number of rows in a table
    def get_num_rows(self,_tbl):
        """count rows in table"""
        _q="SELECT count(*) as count FROM {0} ".format(_tbl,)
        self.db_exec(_q)
        _a=self._cur.fetchone()
        if (_a) :
            try:
                return _a[0]
            except:
                return _a['count']
        else :
            return False
           
