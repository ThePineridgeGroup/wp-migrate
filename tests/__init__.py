import sys, os, datetime, time, re
from nose.tools import nottest
import nt.cfg as cfg
import nt.db as db
import nt.util as util
import nt.ntio as ntio
import nt.nt as nt


def setup():
    '''(int.setup) create the test files'''

    # set any variables
    cfg.xxx = ''


    print "\n --- SETUP! --- \n"
    cfg.path='tests/test-files/'

    #create cfg.parms object & set values
    class p_obj:
        def __init__(self,**kwargs):
            self.__dict__.update(kwargs)

    #create the test parm object
    cfg.parms=p_obj(path=cfg.path,td=0.0,fd=0.0,nv='n')


    # generate test files in folder cfg.path

    if os.path.exists(cfg.path):
        delete_test_files()
    os.mkdir(cfg.path)
    build_test_data(fl,f)




def teardown():
    '''(int.teardown) remove the test files'''
    print "TEAR DOWN!"
    return
    delete_test_files()

@nottest
def delete_test_files():
    '''(init.delete_test_files) delete test files and directory'''

#    for f in os.listdir(cfg.path):
#        try:
#            os.remove(cfg.path+f)
#        except OSError:
#            for fx in os.listdir(cfg.path+f):
#                os.remove(cfg.path+f+'/'+fx)
#            os.rmdir(cfg.path+f)
#    os.rmdir(cfg.path)

@nottest
def build_test_data(_fl,fnm):
    '''(init.build_test_data) Build the test data based on td_dict.

    iput is file object and filename
    '''
#    _fl.write('       10000\n')
#    _fl.write(fnm+'\n')
#    for v in td_dict[fnm]:
#        _fl.write(v+'\n')
    return
# test data
td_dict ={}
