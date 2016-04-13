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
            self.open_ifl()

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

    def open_ifl(self,path=None,flname=None):
        ''' if path and flname passed, set variables
            open the file '''
        self.set_path_file(path,flname)
        print('ifile exists:',os.path.exists(self.path+self.flnm))
        if os.path.exists(self.path+self.flnm):
            self.infl=open(self.path+self.flnm)

    def get_ifl_rec(self,):
        ''' Read a single record and return it in selected format.
            fmt='str' or 'list' determines format of each line
        '''
        _r = self.infl.readline()

        return _r

    def read_ifl(self,):
        ''' Get the entire file.
            fmt='str' or 'list' determines format of each line
        '''
        _a = self.infl.read()
        return _a

    def reset_ifl(self,n=0):
        ''' Reset the file to specific position (char).'''
        self.infl.seek(n)


    def close_ifl(self,):
        ''' close the input file '''
        self.infl.close()
        return

#end of class

class ProcOutput(object):
    ''' all the output file processing   '''
    #constants'

    #variables
    path=None
    flnm=None

    def __init__(self,path=None ,flname=None):
        ''' init class and set the path and filename open file if file passed '''
        self.set_path_file(path,flname,True)
        if self.flnm != None:
            self.open_ofl()


    def set_path_file(self, path, flname, ovrwrite=False):
        ''' set the path & file name variables for class

            ovrwrite - allow path and filename to overwrite existing values
                otherwise just update if value = None
        '''

        if flname != None:
            flname=cfg.outflnm
        if ovrwrite==True:
            self.path=path
            self.flnm=flname
        else:
            if path!= None:
                self.path=path
            if flname != None:
                self.flnm = flname

    def open_ofl(self,path=None,flname=None):
        ''' if path and flname passed, set variables
            open the file '''
        self.set_path_file(path,flname)

        self.ofl=open(self.path+self.flnm,'w')

    def write_ofl(self,line,newline=True):
        '''write a single line file'''
        if newline:
            line+='\n'
        self.ofl.write(line)

    def close_ofl(self,):
        ''' close the file '''
        self.ofl.close()
        return

#end of class
