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

        URL:

        If the site is installed in a subdirectory (ie, not in the root dir
        of the domain, then the URL will be different from the Domain.  If
        they are the same, the URL can be omitted, ie just press return.

        Full Path:

        Some of the internal paths require the full path to the site.  If a
        Linux environment, the path is in the form of /home/<userid>/<site-domain>

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
    print('                 Old URL: ',cfg.old_url)
    print('                 New URL: ',cfg.new_url)
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

def set_cfg_parms():
    ''' prompt for run parms '''

    get_sql_path()

    get_tbl_prefix()
    get_domains()
    get_urls()
    get_full_path()

    confirm(cfg.parms,cfg.parser)

def get_sql_path():
    ''' prompt for path and set file names '''
    print('\nThe sql path can be either relative path or an absolute path.  The relative path is relative to the data/ directory in this application.')
    print('For example:  xYz equates to data/data/xYz')
    print('              /user/home/username/xyz/ is the absolute sql path')
    while (True):
        _path = input('Enter the sql path:  ')
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
                    cfg.skip_atexit = util.print_help()
                    exit()
                else :
                    print("invalid entry....enter y or n")

    _flist=get_filelist(cfg.path)
    if not _flist:
        print('\n**No sql file found at the default directory {}  \nRerun and enter a correct path\n**Aborting Run**'.format(cfg.path))
        cfg.skip_atexit = True
        exit()
    else:
        cfg.inflnm = _flist[0]
        _nfnm = cfg.inflnm.split('.sql')
        cfg.outflnm = _nfnm[0]+cfg.new_fl_sfx+'.sql'

    print('   ')        #spacing

def get_tbl_prefix():
    ''' prompt for parms '''
    print('Enter the old and new table prefix:')
    print('(press enter for no prefix)')
    while (True):
        _op = input('Enter the old table prefix:  ')
        _np = input('Enter the new table prefix:  ')
        print('Changing Old Prefix: {}  ==> New Prefix: {} '.format(_op,_np))
        usr_resp= input("  Is this correct? (y/n/x to exit)   ")
        if (usr_resp =='y') :
            cfg.old_tbl_prefix = _op
            cfg.new_tbl_prefix = _np
            break
        elif (usr_resp == 'x'):
            cfg.skip_atexit = util.print_help()
            exit()


    print('   ')        #spacing

def get_domains():
    ''' prompt for old and new domains '''
    print('Enter the old and new domain names: www.domain.com')
    while (True):
        _od = input('Enter the old domain:  ')
        _nd = input('Enter the new domain:  ')
        print('Changing Old Domain: {}  ==> New Domain: {} '.format(_od,_nd))
        usr_resp= input("  Is this correct? (y/n/x to exit)   ")
        if (usr_resp =='y') :
            cfg.old_domain = _od
            cfg.new_domain = _nd
            break
        elif (usr_resp == 'x'):
            cfg.skip_atexit = util.print_help()
            exit()

    print('   ')        #spacing

def get_urls():
    ''' prompt for old and new url '''
    print('Enter the old and new url: www.domain.com/directory')
    print('  This will differ from domain if the site is installed')
    print('  in a subdirectory')
    while (True):
        _od = input('Enter the old url:  ')
        _nd = input('Enter the new url:  ')
        print('Changing Old URL: {}  ==> New URL: {} '.format(_od,_nd))
        usr_resp= input("  Is this correct? (y/n/x to exit)   ")
        if (usr_resp =='y') :
            cfg.old_url = _od
            cfg.new_url = _nd
            break
        elif (usr_resp == 'x'):
            cfg.skip_atexit = util.print_help()
            exit()

    print('   ')        #spacing

def get_full_path():
    ''' prompt for full path '''
    print('Enter the old and new full path:   /home/userid/site/')
    print('(press enter to skip)')
    while (True):
        _op = input('Enter the old full path:  ')
        _np = input('Enter the new full path:  ')

        print('Changing Old Path: {}  ==> New Path: {} '.format(_op,_np))
        usr_resp= input("  Is this correct? (y/n/x to exit)   ")
        if (usr_resp =='y') :
            cfg.old_full_path = _op
            cfg.new_full_path = _np
            break
        elif (usr_resp == 'x'):
            cfg.skip_atexit = util.print_help()
            exit()

    print('   ')        #spacing

