#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cfg.py
#   this file contains all the shared variables for the application.
#
#  Copyright 2014 The Pineridge Group, LLC <cswaim@tpginc.net>
#  License: GPLv2 or later
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#

from __future__ import division, print_function
import sys, os, datetime, time, re
from decimal import *

version='1.1'      # version to monitor changes to the config.ini file layout
parms=''           # parms object from parser
rel_path='data/data/'
new_fl_sfx='new'
path=''            # path to data file directory w/ trailing '/'
inflnm=''
outflnm=''

#from wp-config.php  $table_prefix
old_tbl_prefix=''
new_tbl_prefix=''
#domain is www.domain.xxx
old_domain=''
new_domain=''
#url is the domain plus install subdirectory www.domain.xxx/directory
old_url=''
new_url=''
#full_path is /home/userid/site/directory
old_full_path=''
new_full_path=''

#errors
err=False
err_msgs=[]

#variables
skip_atexit = False
