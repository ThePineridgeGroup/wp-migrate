#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  wp_migrate.py
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
import atexit

# neutron-tunneling modules
import cfg, util, flio

parms=(object)

class WPMigrate(object):
    ''' sample class
    '''

    #variables
    #skip_atexit = False
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

        util.set_cfg_parms()


    def process_sql_file(self,):
        ''' read the sql file, make changes, write new sql file '''

        self.outfl=flio.ProcOutput(cfg.path,cfg.outflnm)

        with open(cfg.path+cfg.inflnm,'r') as self.infl:
            for _rec in self.infl:
                if self.scan_for_old_strings(_rec):
                    #_rec = self.pre_proc_rec(_rec)
                    _rec = self.edit_rec(_rec)
                    #_rec = self.pst_proc_rec(_rec)

                self.outfl.write_ofl(_rec,newline=False)

        self.outfl.close_ofl()

        print('Processing of sql file complete \n')


    def pre_proc_rec(self,_r):
        ''' edit each record so parsing works correctly '''
        return _r

    def pst_proc_rec(self,_r):
        ''' reverse changes applied in pre processing '''
        return _r

    def edit_rec(self,_r):
        ''' scan and edit each record if appropriate'''

        #import pdb; pdb.set_trace()
        _sep = "\\', "

        #save the end char & split the rec into a list
        _end = _r[:-1]

        #re.split parses the sql correctly, where str.split does
        # not handle escaped ' correctly
        self._rlist = re.split(r"\\\'\, ",_r)

        for i,_s in enumerate(self._rlist):
            #try unserialize, else just use it
            if self.scan_for_old_strings(_s):
                try:
                    add_quotes = False
                    if _s[1:3] == 'a:':
                        _s = _s.strip("'")
                        add_quotes = True
                    _s = phpserialize.unserialize(_s,array_hook=OrderedDict)
                    _s = self.iterate_data(_s)
                    _ss = phpserialize.serialize(_s)
                    #add back single quotes
                    if add_quotes:
                        self._rlist[i] = "'{}'".format(_ss)
                        add_quotes = False
                except Exception as e:
                    self._rlist[i] = self.replace_strings(_s)
                    if _s[0:2] == 'a:':
                        print('\n**serialization failed: {}\n{}'.format(self._rlist[0],self._rlist[i]))
                        print('**',e)
                        #print('***',a)
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
        if not cfg.old_url in ['',None]:
            if re.search(cfg.old_url,_txt):
                _r = True
        return _r
        if not cfg.old_full_path in ['',None]:
            if re.search(cfg.old_full_path,_txt):
                _r = True
        return _r

    def replace_strings(self,_s):
        ''' replace the strings
            ***NOTE:
            the URL must process before the Domain as the Domain is a
            subset of the url.  If the domain processes first, then the
            url will not match.
        '''
        #search for a string that needs changing
        if not cfg.old_url in ['',None]:
            if re.search(cfg.old_url,_s):
                _s = _s.replace(cfg.old_url,cfg.new_url)

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
        if cfg.skip_atexit:
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




