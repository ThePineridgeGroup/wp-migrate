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
from six.moves import input
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
    skip_atexit = False

    def __init__(self):
        ''' init class and define cursors '''
        atexit.register(self.exit_rtn)


    def config_parser_values(self,):
        ''' initialize the cfg parser (help text)
            prompt for run parameters
            set cfg values
        '''
        global parms
        cfg.parser=util.get_parser()
        cfg.parms = cfg.parser.parse_args()

        self.get_path()
        cfg.inflnm = 'tpg_wp.sql'
        cfg.outflnm = 'tpg_wp-new.sql'

        self.get_tbl_prefix()
        self.get_domains()

        util.confirm(cfg.parms,cfg.parser)


    def get_path(self,):
        ''' prompt for path and set file names '''
        print('The path can be either relative path or an absolute path.  The relative path is relative to the data/ directory in this application.')
        print('For example:  xYz equates to data/data/xYz')
        print('              /user/home/username/xyz/ is the absolute path')
        while (True):
            _path = input('Enter the path:  ')
            if _path[:-1] not in ['/','\\']:
                _path += '/'
            if os.path.exists(cfg.rel_path+_path):
                _path = cfg.rel_path+_path
                cfg.path = _path
                break
            elif os.path.exists(_path):
                cfg.path = _path
                break
            else:
                while (True):
                    usr_resp= input("  The path was invalid. Retry? (y/n)  ")
                    if (usr_resp =='y') :
                        break
                    elif (usr_resp in ['n','x']):
                        self.skip_atexit = util.print_help()
                        exit()
                    else :
                        print("invalid entry....enter y or n")

        _flist=util.get_filelist(cfg.path)
        if not _flist:
            print('\n**No sql file found at the default directory {}  \nRerun and enter a correct path\n**Aborting Run**'.format(cfg.path))
            self.skip_atexit = True
            exit()
        else:
            cfg.inflnm = _flist[0]
            _nfnm = cfg.inflnm.split('.sql')
            cfg.outflnm = _nfnm[0]+cfg.new_fl_sfx+'.sql'

        print('   ')        #spacing

    def get_tbl_prefix(self,):
        ''' prompt for parms '''
        print('Enter the old and new table prefix:')
        print('(press enter for no prefix)')
        while (True):
            _op = input('Enter the old table prefix:  ')
            _np = input('Enter the new table prefix:  ')
            print('Old Prefix: {}  ==> New Prefix: {} '.format(_op,_np))
            usr_resp= input("  Is this correct? (y/n/x to exit)   ")
            if (usr_resp =='y') :
                cfg.old_tbl_prefix = _op
                cfg.new_tbl_prefix = _np
                break
            elif (usr_resp == 'x'):
                self.skip_atexit = util.print_help()
                exit()


        print('   ')        #spacing

    def get_domains(self,):
        ''' prompt for old and new domains '''
        print('Enter the old and new domain names: www.domain.com')
        while (True):
            _od = input('Enter the old domain:  ')
            _nd = input('Enter the new domain:  ')
            print('Old Domain: {}  ==> New Domain: {} '.format(_od,_nd))
            usr_resp= input("  Is this correct? (y/n/x to exit)   ")
            if (usr_resp =='y') :
                cfg.old_domain = _od
                cfg.new_domain = _nd
                break
            elif (usr_resp == 'x'):
                self.skip_atexit = util.print_help()
                exit()

        print('   ')        #spacing

    def process_sql_file(self,):
        ''' read the sql file, make changes, write new sql file '''

        self.outfl=flio.ProcOutput(cfg.path,cfg.outflnm)

        with open(cfg.path+cfg.inflnm,'r') as self.infl:
            for _rec in self.infl:
                #print(_rec)
                if re.search(cfg.old_domain,_rec) or re.search(cfg.old_tbl_prefix,_rec):
                    #print(_rec)
                    _rec = self.edit_rec(_rec)

                self.outfl.write_ofl(_rec,newline=False)

        self.outfl.close_ofl()

        print('Processing of sql file complete \n')


    def edit_rec(self,_r):
        ''' scan and edit each record if appropriate'''

        #import pdb; pdb.set_trace()
        _sep = "', '"

        #save the end char & split the rec into a list
        _end = _r[:-1]
        _rlist = _r.split(_sep)

        for _s in _rlist:
            #try unserialize, else just use it
            serialized=False
            try:
                _s = phpserialize.unserialize(_s,array_hook=OrderedDict)
                #serialized=True
                for _se in _s:
                    _se = self.replace_strings(_se)
                _s = phpserialize.serialize(_s)
            except:
                _s = self.replace_strings(_s)



        #put the pieces back together
        _t = _sep.join(_rlist)
        if _end == ',' and _t[-1] != ',':
            _t += ','
        return _t

    def replace_strings(self,_s):
        ''' replace the strings'''
         #search for a string that needs changing
        if re.search(cfg.old_domain,_s):
            print('before: {}'.format(_s))
            _s = _s.replace(cfg.old_domain,cfg.new_domain)
            print(' after: {}'.format(_s))

        if re.search(cfg.old_tbl_prefix,_s):
            _s = _s.replace(cfg.old_tbl_prefix,cfg.new_tbl_prefix)

        return _s


    def serialize_rec(self,_r):
        ''' unserialize the rec, change elements, serialize'''

        _s = phpserialize.unserialize(_r,array_hook=OrderedDict)

        #loop thru _s and change text
        # code to come

        _r = phpserialize.serialize(_s)

        return s


    def exit_rtn(self,):
        ''' clean up at exit'''
        # if help printed, skip this
        if self.skip_atexit:
            return
        #print('(wpm.exit) Processing of wpm files complete')


    def main(self,):
        ''' init cfg, load db, cleanup, write out csv, graphs '''
        #setup
        self.config_parser_values()
        self.process_sql_file()





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




