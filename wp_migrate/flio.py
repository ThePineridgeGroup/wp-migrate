#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  flio.py
#
#  Copyright 2014 The Pineridge Group, LLC <cswaim@tpginc.net>
#  License: GPLv2 or later
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#

from __future__ import division, print_function
import sys, os, datetime, time, re
import string
from decimal import *
#application modules
import cfg, util


def whoamI():
    print('in module {} {}'.format(sys.argv[0],__name__))

class ProcInput(object):
    ''' all the input file processing   '''

    #variables
    path=None
    flnm=None

    def __init__(self,path=None ,flname=None):
        ''' init class and set the path and filename open file if file passed '''

        self.set_path_file(path,flname,True)
        if self.path != None and self.flnm != None:
            self.open_ifile()

    def set_path_file(self,path,flname,ovrwrite=False):
        ''' set the path & file name variables for class '''
        if ovrwrite==True:
            self.path=path
            self.flnm=flname
        else:
            if path!= None:
                self.path=path
            if flname != None:
                self.flnm = flname

    def open_ifile(self,path=None,flname=None):
        ''' if path and flname passed, set variables
            open the file '''
        self.set_path_file(path,flname)
        if os.path.exists(self.path+self.flnm):
            self.infl=open(self.path+self.flnm)

    def get_ifl_rec(self,fmt='list'):
        ''' Read a single record and return it in selected format.

            fmt='str' or 'list' determines format of each line
        '''
        _r = self.infl.readline()
        if fmt == 'list':
            _r = self.parse_input_line(_r)

        return _r

    def read_ifl(self,fmt='list'):
        ''' Get the entire file.

            fmt='str' or 'list' determines format of each line
        '''
        _a = self.infl.read()
        if fmt == 'list':
            _xx = re.split('\n',_a)
            _t = []
            for _x in _xx:
                _b = self.parse_input_line(_x)
                _t.append(_b)
            _a = _t
        return _a

    def reset_ifl(self,n=0):
        ''' Reset the file to specific position (char).'''
        self.infl.seek(n)

    def parse_input_line(self,_ln):
        '''parse the line and return a list (time,value)'''
        _ln = _ln.strip(' \t\n\r')
        _tv = re.split('\s+',_ln)
        if len(_tv) < 2:
            _tv.insert(0,'hdr')

        if _tv[0] != 'hdr':
            #_tv[0]= Decimal(str(_tv[0]),cfg.context).quantize(cfg.dquant)
            _tv[0]= util.fmt_time(_tv[0])
        return _tv

    def close_ofl(self,):
        ''' close the input file '''
        self.infl.close()
        return

#end of class

class ProcOutput(object):
    ''' all the output file processing   '''
    #constants
    fl_pfx='RAW_'

    #variables
    path=None
    flnm=None

    def __init__(self,path=None ,flname=None,pfx=None):
        ''' init class and set the path and filename open file if file passed '''
        self.set_path_file(path,flname,pfx,True)
        if self.flnm != None:
            self.open_ofl()

    def set_path_file(self, path, flname, pfx, ovrwrite=False):
        ''' set the path & file name variables for class

            ovrwrite - allow path and filename to overwrite existing values
                otherwise just update if value = None
        '''
        if pfx !=None:
            self.fl_pfx = pfx

        if flname != None:
            self.fnm=util.parse_col_from_file(flname).upper()
            flname=self.fl_pfx+cfg.testno+'_'+self.fnm+'.csv'
        if ovrwrite==True:
            self.path=path
            self.flnm=flname
        else:
            if path!= None:
                self.path=path
            if flname != None:
                self.flnm = flname

    def open_ofl(self,path=None,flname=None,pfx=None):
        ''' if path and flname passed, set variables
            open the file '''
        self.set_path_file(path,flname,pfx)

        self.ofl=open(self.path+self.flnm,'w')


    def write_ofl(self,line,newline=True):
        '''write a single line file'''
        if newline:
            line+='\n'
        self.ofl.write(line)

    def write_ofl_list(self,_list,newline=True):
        '''write a single line file'''
        if newline:
            new_line = '\n'
        else:
            new_line = ''
        self.write_ofl(self.fnm)
        for i in _list:
            _line= '{:17.15f},{:f}{}'.format(i[0],i[1],new_line)
            self.ofl.write(_line)

    def close_ofl(self,):
        ''' close the file '''
        self.ofl.close()
        return

#end of class
