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
    rlist=[]
    ser_err_cnt=0

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

        self.get_tbl_prefix()
        self.get_domains()
        self.get_full_path()

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

    def get_full_path(self,):
        ''' prompt for full path '''
        print('Enter the old and new full path:   /home/userid/site/')
        print('(press enter to skip)')
        while (True):
            _op = input('Enter the old full path:  ')
            _np = input('Enter the new full path:  ')

            print('Old Path: {}  ==> New Path: {} '.format(_op,_np))
            usr_resp= input("  Is this correct? (y/n/x to exit)   ")
            if (usr_resp =='y') :
                cfg.old_full_path = _op
                cfg.new_full_path = _np
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
                if self.scan_for_old_strings(_rec):
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
        self._rlist = _r.split(_sep)


        for i,_s in enumerate(self._rlist):
            #try unserialize, else just use it
            if self.scan_for_old_strings(_s):
                try:
                    _s = phpserialize.unserialize(_s,array_hook=OrderedDict)
                    #serialized=True
                    _s = self.iterate_data(_s)
                    self._rlist[i] = phpserialize.serialize(_s)
                except:
                    self._rlist[i] = self.replace_strings(_s)
                    if _s[0:2] == 'a:':
                        print('\n**serialization failed: {}\n{}'.format(self._rlist[0],self._rlist[i]))
                        self.ser_err_cnt += 1

        #put the pieces back together
        _t = _sep.join(self._rlist)
        if _end == ',' and _t[-1] != ',':
            _t += ','
        return _t

    def iterate_data(self,_s):
        ''' parse the data and determine if it contains nested arrays
            recursive call to process nested arrays
        '''
        for _sk, _sv in six.iteritems(_s):
            if isinstance(_sv, six.string_types):
                _s[_sk] = self.replace_strings(_sv)
            else:
                self.iterate_data

        return _s

    def scan_for_old_strings(self,_txt):
        ''' scan for text that needs to be changed and return true if so'''
        #if re.search(cfg.old_domain,_txt) or re.search(cfg.old_tbl_prefix,_txt):
        _r = False
        if not cfg.old_domain in ['',None]:
            if re.search(cfg.old_domain,_txt):
                _r = True
        if not cfg.old_tbl_prefix in ['',None]:
            if re.search(cfg.old_tbl_prefix,_txt):
                _r = True
        if not cfg.old_full_path in ['',None]:
            if re.search(cfg.old_full_path,_txt):
                _r = True
        return _r

    def replace_strings(self,_s):
        ''' replace the strings'''
        #search for a string that needs changing

        if not cfg.old_domain in ['',None]:
            if re.search(cfg.old_domain,_s):
                _s = _s.replace(cfg.old_domain,cfg.new_domain)

        if not cfg.old_tbl_prefix in ['',None]:
            if re.search(cfg.old_tbl_prefix,_s):
                _s = _s.replace(cfg.old_tbl_prefix,cfg.new_tbl_prefix)

        if not cfg.old_full_path in ['',None]:
            if re.search(cfg.old_full_path,_s):
                _s = _s.replace(cfg.old_full_path,cfg.new_full_path)

        return _s


    def exit_rtn(self,):
        ''' clean up at exit'''
        # if help printed, skip this
        if self.skip_atexit:
            return
        print('(wpm.exit) Processing of wpm files complete')
        print('** {} serializations failed '.format(self.ser_err_cnt))


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


if __name__ == '__main__':
    main()




