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

import sys, os, datetime, time, re
from decimal import *
import inspect

#set precision for decimal time
context = Context(prec = 14)
dquant=Decimal('10')**-10
tround=Decimal('-10')**-13
    
version='1.1'      # version to monitor changes to the config.ini file layout
parms=''           # parms object from parser
path=''            # path to data file directory w/ trailing '/'

dbnm=''            # db name
tblnm=''           #  table name

display_on_console=True    #show plots on console
