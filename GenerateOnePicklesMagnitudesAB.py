import numpy as np
import sys

import contextlib
import os

import sys,getopt

import libGenerateABMagnitudes.py


if __name__ == "__main__":
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"f:l:h",['f=',"l=",'help'])
    except getopt.GetoptError:
        print(' Exception bad getopt with :: '+sys.argv[0]+ ' -f <first-number> -l <last-number>')
        sys.exit(2)
        

    str_fnum=""
    fnum=0

    str_lnum=""
    lnum=0
    
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(sys.argv[0]+ ' -f <first-number> -l <last-number>')
            sys.exit(2)
        elif opt in ('-f', '--fnum'):
            str_fnum = arg
            fnum=int(str_fnum)
        elif opt in ('-l', '--lnum'):
            str_lnum = arg
            lnum=int(str_lnum)
        else:
            print(sys.argv[0]+ ' -f <first-number> -l <last-number>')
            sys.exit(2)
 
    IDX_START=fnum
    IDX_STOP=lnum
    
    print("IDX_START={} , IDX_STOP={} ".format(IDX_START,IDX_STOP))
    


    with contextlib.redirect_stdout(None):
        for idx in np.arange(IDX_START,IDX_STOP+1):
            #%run libGenerateABMagnitudes -n $idx
            libGenerateABMagnitudes.entry(idx)