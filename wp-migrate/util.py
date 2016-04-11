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

import sys, os, datetime, time, re
import argparse, configparser
import importlib
import json,copy
from collections import OrderedDict
from decimal import *
import numpy as np
# neutron-tunneling modules
import cfg, db, flio

def set_db():
    '''set db to the instance '''
    global db
    db = cfg.db

def config_setup():
    '''set the values in cfg after parser has set path 
       cfg.xxxx=cfg.parms.xxxx
    '''
    # set current path
    cfg.path=cfg.parms.path+'/'

    #set db and tablename from run parms
    cfg.sitename='apptest'
    cfg.dbnm=cfg.sitename+'.sqlite'
    cfg.tblnm=cfg.sitename
    
    # see if display on console flag is set
    if cfg.parms.display == 'n':
        cfg.display_on_console = False
    else:
        cfg.display_on_console = True   


def config_runparms():
    '''get the runparms from config file and load in cfg '''
    print("Get the run parms")
    co = ConfigOptions()
    cfg.run_parms = co.get_sectparms('RunParms')
    
    #build cfg fields from run parms
    
    #cfg.xxxxx= cfg.run_parms["xxxxx"]
  

    print('Run parms complete.\n')

def prt_cfg_runparms():
    '''print the run parms from the cfg module'''
    print('CFG Run Parms        ')
    print('          xxxxx: {} '.format(cfg.xxxxx))
    print('')

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
                if _f[-4:] == '.txt':
                    _filelist.append(_f)
            break            #exit after level 1 directory
    else:
        _filelist=False
    if _filelist:
        _filelist.sort()
    return _filelist


def fnd_file(tbl, fn):
    if fn in tbl:
        return True
    else:
        return False

def get_parser():
    """ get the command line args
        @return object of parser args
    """
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='nt',
    epilog='''
    Description
        Describe application here

        Other comments
    
    Other Parms:

        No other parms
        
        Usage:   python nt.py path/to/dir
        output file is path/to/file-xx.csv   (note insert of -xx in name)
    '''
    )
    
    parser.add_argument('path', metavar='path to the experiment data', nargs='?', help='path name must be the absolute path or relative path to the desired folder. ')
    parser.add_argument('-td', metavar='time_delta', nargs='?', default='0.00002048', help='time delta')
    parser.add_argument('-fd',metavar="freq_delta",nargs='?',default='0.0492125984260099',help="frequency delta")
    parser.add_argument("-nv","--noverify",action="store_const",dest="verify",const='n',default='y',help="-nv will not prompt for verification")
    parser.add_argument("-nd","--nodisplay",action="store_const",dest="display",const='n',default='y',help="-nd will supress the display of the graphs on console")
        
    #parser.add_argument('sectname', metavar='Section Name', nargs='?', help='the section in the ini file which contains the parms', default='xxxxx')


    #parser.add_argument("-v","--verbose",action="store_true",dest="verbose",help="-v will run in verbose mode, showing all output from match routine")
    
    return parser
    
def confirm(parms,parser):
    ''' display the parameters for this run and ask for verification '''
    
    print('\n=============PARMS for False Positive Analysis==============')
    print('        Running for test: ',parms.path)
    print('')
    print('===================================================\n')
    if (parms.verify == 'y') :
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



class ConfigOptions(object):
    '''
    /**
     *
     * File Description: This class provides a single access metthod to 
     *    acquire parms.  A call to the method returns an array of 
     *    runparms.  If the run parm file does not exist, a file is 
     *    created from the defaults in the config file.  If the file
     *    is found, then the options are set from the parm file.
     *
     * If a version is set, the cfg version is compared to parm version and
     *    the file is rewritten if the version changes.
     *    
     *
     * @author          The Pineridge Group, LLC 
     * @link            http://www.tpginc.net/
     * @lastmodified    2012-06-15
     * @copyright       2012 The Pineridge Group, LLC
     *     *
     * @license     http://opensource.org/licenses/gpl-license.php GNU Public License
     */

      
    /**  
     * Usage
     * <code>
     * co = util.ConfigOptions()
     * sect_array = co.get_sectparms('RunParms')
     * </code>
     *
     *

     */
    '''
    
    #class variables
    _cp=''                                  #config parser object
    cwd=''                                  #curr working dir
    configfl='config.ini'                   #config file

    def __init__(self,_cfgfl=''):
        ''' Constructor - load file or create if not found
        '''

        if _cfgfl:
            self.configfl=_cfgfl
    
        # create config parser object
        self._cp =configparser.SafeConfigParser()
        #path to current working directory
        self.cwd = cfg.path
        
        if os.path.exists(self.cwd+self.configfl):
            self._cp.read(self.cwd+self.configfl)
        else:
            with open(self.cwd+self.configfl,'w') as cfl:
                cfl.write("# config file - values here will override cfg module values \n")
                cfl.write("[RunParms] \n")
                cfl.write("version={} \n".format(cfg.version))
                

            cfl.close()
            # read the model
            self._cp.read(self.cwd+self.configfl)

        
    def __del__(self):
        pass
    
    def verify_parmfile(self,_path,_flnm):
        ''' Verify parm file exists. 
        '''
        if not os.path.exists(_path+_flnm):
            print('***')
            print('  sys parm file "{0}" not found on path {1}'.format(_flnm, _path))
            print('  path:',_path+_flnm)
            print('***')
            exit(1)

    def get_sectparms(self,sect='RunParms'):
        '''
        * get_sectparms - return an array of the section options from the 
        * run options ini file
        *
        * @returns array of section options

        '''

        # return dict
        try:
            sectparms = dict(self._cp.items(sect))
        except:
            print('***')
            print('  run parm section "{0}" not found '.format(sect))
            print('***')
            exit(1)


        if 'version' not in sectparms or sectparms['version'] != cfg.version:
            print('***')
            print('  The version of config.ini is not the same as the config.py module')
            print('  Save any changes made in the config.ini and then delete the file')
            print('  this will force rebuilding of the file in the correct format')
            print('  Re-apply any custom changes')
            print('***')
            exit(1)

        return sectparms
