#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  crawler.py
#
#   This is the main controller for the neutron tunneling application
#   which will reformat the files from the nt experiments.
#
#  Copyright 2014 The Pineridge Group, LLC <cswaim@tpginc.net>
#  License: GPLv2 or later
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#


import sys, os, argparse, configparser, datetime, time, re
from decimal import *
import importlib
import atexit

# neutron-tunneling modules
import cfg, db, util, flio

parms=(object)

class AppProcess(object):
    ''' sample class
    '''

    #variables


    def __init__(self):
        ''' init class and define cursors '''
        atexit.register(self.exit_rtn)


    def config_parser_values(self,):
        '''initialize the cfg parser vmodule values'''
        global parms
        parser=util.get_parser()
        cfg.parms = parser.parse_args()
        util.confirm(cfg.parms,parser)

        #set rest of config values
        util.config_setup()

        #redirect stdout to writer class to allow console & file
        #t= tpgWriter(cfg.path+cfg.log_file,'w','b')
        #sys.stdout=t

    def db_setup(self,):
        '''init db & build table '''
        #global db
        print('Setting up database')
        cfg.db=db.ApplDb(cfg.path,cfg.dbnm)
        #cfg.db=db
        self.set_db()
        db.create_tbl(cfg.tblnm)
        #hack to establish utility access to the db instance
        util.set_db()

    def set_db(self,):
        '''set linkage to db instance'''
        global db
        db=cfg.db

    def app_functions(self):
        ''' function description '''

            #db.ins_upd_row(cfg.tblnm,_row)
            db.commit()
            _cnt=db.get_num_rows(cfg.tblnm)
        print('Message to log progress. function complete \n')


    def exit_rtn(self,):
        ''' clean up at exit'''
        print('(nt.exit) Processing of NT files complete')

        try:
            #close db
            db.close_cursor()
        except:
            pass

    def main(self,):
        ''' init cfg, load db, cleanup, write out csv, graphs '''
        #setup
        self.config_parser_values()
        util.config_runparms()
        self.db_setup()

        #read files and update db
        self.build_table()

        #get start/stop time
        util.calc_start_stop()





#end of class


def main():
    '''
    The main routine to get cmd line parms, initiate class and call
    main method(s)
    '''

    nt=AppProcess()
    nt.main()
    #print_data()

def print_data():
    '''debug info '''
    print('parms: ',cfg.parms)
    print('util path:',os.getcwd(),'*',cfg.parms.path,'*')

    print('filelist in nt', cfg.filelist,type(cfg.filelist),cfg.path)
    print('***')

    print('modules in nt', cfg.modulelist,'\n testno:',cfg.testno)
    print('***')


    print('cols list in nt', cfg.cols,type(cfg.filelist),cfg.testno)
    print('***')

    print('expected  in nt',cfg.expected_infiles)
    print('***')

    print('util: ', end=' ')
    util.whoamI()
    print('  ntio: ', end=' ')
    ntio.whoamI()
    print(' cfg: ', end=' ')
    cfg.whoamI()

    V02.main()


if __name__ == '__main__':
    main()




