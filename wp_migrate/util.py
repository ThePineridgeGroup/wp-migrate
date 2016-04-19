#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  util.py
''' Utility funtctions for application. '''
#
#  Copyright 2014 The Pineridge Group, LLC <cswaim@tpginc.net>
#  License: GPLv2 or later
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#

from __future__ import division, print_function
import sys, os, datetime, time, re
import argparse
import six
from six.moves import configparser
from six.moves import input
import json,copy
from collections import OrderedDict
from decimal import *
# application modules
import cfg, flio


def fmt_time(_t):
    '''format the time to consistant Decimal '''
    _d = Decimal(_t).quantize(cfg.dquant)
    return _d

def get_filelist(path=''):
    ''' take a path or file name and return a list of files.

        if a path, the list will contain all files in path dir
        if a file name, only the single file is in the list

        return the list if path exists
        return False if path does not exist
    '''
    _filelist=[]
    if os.path.exists(path):
        for (_dirpath, _dirnames, _filenames) in os.walk(path):
            for _f in _filenames:
                if _f[-4:] == '.sql':
                    _filelist.append(_f)
            break            #exit after level 1 directory
    else:
        _filelist=False
    if _filelist:
        _filelist.sort()
    return _filelist


def get_parser():
    """ get the command line args
        @return object of parser args
    """
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='WP Migrate',
    epilog='''
    Description
        WP Migrate is a tool to process the WordPress sql and change
        the table name prefix, if applicable, and domain name.

        A prompt for the following parameters will be shown:

        Path:

        The path is relative to the application root directory or an
        absolute path.  The ending / must be entered.

        Table Prefix:

        The table name prefix is optional and if not used, then is
        skipped.  The prefix is established in the wp-config.php file
        in the php value $table_prefix.

        Domain:

        Domain name references are stored in two forms: text and serialized
        text.  The application will scan for the domain name and
        determine if the string is in standard text or serialized text.

        Other comments

        This application should run under Python 2.7 or Python 3.3.
        See the requirements.txt file for Python module dependencies.

    Parms:

        No parameters are passed at startup. The application will prompt
        for the parameters.

        Usage:   python wp-migrate.py

        Output file:  path/to/file-new.sql
    '''
    )

    #parser.add_argument('path', metavar='path to the experiment data', nargs='?', help='path name must be the absolute path or relative path to the desired folder. ')
    #parser.add_argument('-td', metavar='time_delta', nargs='?', default='0.00002048', help='time delta')
    #parser.add_argument('-fd',metavar="freq_delta",nargs='?',default='0.0492125984260099',help="frequency delta")
    #parser.add_argument("-nv","--noverify",action="store_const",dest="verify",const='n',default='y',help="-nv will not prompt for verification")
    #parser.add_argument("-nd","--nodisplay",action="store_const",dest="display",const='n',default='y',help="-nd will supress the display of the graphs on console")

    #parser.add_argument('sectname', metavar='Section Name', nargs='?', help='the section in the ini file which contains the parms', default='xxxxx')

    #parser.add_argument("-v","--verbose",action="store_true",dest="verbose",help="-v will run in verbose mode, showing all output from match routine")

    return parser

def confirm(parms,parser):
    ''' display the parameters for this run and ask for verification '''

    print('\n============= PARMS for WP Migration ==============')
    print('        Path to sql file: ',cfg.path)
    print('                sql file: ',cfg.inflnm)
    print('            new sql file: ',cfg.outflnm)
    print('')
    print('        Old table prefix: ',cfg.old_tbl_prefix)
    print('        New table prefix: ',cfg.new_tbl_prefix)
    print('')
    print('              Old Domain: ',cfg.old_domain)
    print('              New Domain: ',cfg.new_domain)
    print('')
    print('')
    print('           Old Full Path: ',cfg.old_full_path)
    print('           New FUll Path: ',cfg.new_full_path)
    print('=====================================================\n')

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

def print_help():
    ''' print the help from the parser '''
    cfg.parser.print_help()
    return True


