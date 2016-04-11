#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  wp-migrate.py
#
#   This is the main controller for the wp mirgration application
#   which will change the domain name in the sql files.
#
#  Copyright 2016 The Pineridge Group, LLC <cswaim@tpginc.net>
#  License: GPLv2 or later
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#

from __future__ import division, print_function
import sys, os, argparse, datetime, time, re
import phpserialize
import six
from collections import OrderedDict
from decimal import *
import importlib
import atexit

# neutron-tunneling modules
import cfg, util, flio

parms=(object)

class WPMigrate(object):
    ''' sample class
    '''

    #variables


    def __init__(self):
        ''' init class and define cursors '''
        atexit.register(self.exit_rtn)


    def config_parser_values(self,):
        ''' initialize the cfg parser (help text)
            prompt for run parameters
            set cfg values
        '''
        global parms
        parser=util.get_parser()
        cfg.parms = parser.parse_args()


        util.confirm(cfg.parms,parser)

        #set rest of config values
        util.config_setup()

    def get_path(self,):
        ''' prompt for parms '''
        while (True):
            usr_resp= input("  Is this correct? (y/n)  ")
            if (usr_resp =='y') :
                break
            elif (usr_resp == 'n'):
                parser.print_help()
                exit()
            else :
                print("invalid entry....enter y or n")

        print('   ')        #spacing

    def get_tbl_prefix(self,):
        ''' prompt for parms '''
        while (True):
            usr_resp= input("  Is this correct? (y/n)  ")
            if (usr_resp =='y') :
                break
            elif (usr_resp == 'n'):
                parser.print_help()
                exit()
            else :
                print("invalid entry....enter y or n")

        print('   ')        #spacing

    def get_domains(self,):
        ''' prompt for old and new domains '''
        while (True):
            usr_resp= input("  Is this correct? (y/n)  ")
            if (usr_resp =='y') :
                break
            elif (usr_resp == 'n'):
                parser.print_help()
                exit()
            else :
                print("invalid entry....enter y or n")

        print('   ')        #spacing

    def app_functions(self):
        ''' function description '''

        print('Message to log progress. function complete \n')


    def exit_rtn(self,):
        ''' clean up at exit'''
        print('(wpm.exit) Processing of wpm files complete')


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

    wpm=WPMigrate()
    wpm.main()
    #print_data()

def print_data():
    '''debug info '''
    print('parms: ',cfg.parms)
    print('util path:',os.getcwd(),'*',cfg.parms.path,'*')

    print('filelist in wpm', cfg.filelist,type(cfg.filelist),cfg.path)
    print('***')

    print('modules in wpm', cfg.modulelist,'\n testno:',cfg.testno)
    print('***')


    print('cols list in wpm', cfg.cols,type(cfg.filelist),cfg.testno)
    print('***')

    print('expected  in wpm',cfg.expected_infiles)
    print('***')

    print('util: ', end=' ')
    util.whoamI()
    print('  wpmio: ', end=' ')
    wpmio.whoamI()
    priwpm(' cfg: ', end=' ')
    cfg.whoamI()

    V02.main()


if __name__ == '__main__':
    main()




