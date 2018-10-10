
# coding: utf-8

# # Generate series of Magnitudes from Cadence
# 
# Test My Telescope cloned from Telescope of Philippe Gris
# 
# - author : Sylvie Dagoret-Campagne
# - date   : October 10th 2018
# - update : October 10th 2018
# 
# The goal is to provide the AB magnitude of a star


#import matplotlib.pyplot as plt
#import matplotlib.colors as colors
#import matplotlib.cm as cmx
import numpy as np
import os,sys
import pandas as pd

import sys,getopt

from astropy.io import fits



# libradtran
#-------------
PATH_LIBRADTRAN='./libradtran'
sys.path.append(PATH_LIBRADTRAN)
import libsimulateTranspLSSTScattAbsAer3 as rt

# lsstsims
#----------
from lsst.sims.photUtils import SignalToNoise
from lsst.sims.photUtils import PhotometricParameters
from lsst.sims.photUtils import Bandpass,Sed

from MyTelescope import *
from MyThroughputs import *


# LSST
#-----

all_filternum = {'u':1, 'g':2, 'r':3, 'i':4, 'z':5, 'y':6}
all_filtercolors = {'u':'b', 'g':'g', 'r':'r', 'i':'y', 'z':'grey', 'y':'k'}
all_filtername= ['u','g','r','i','z','y']
all_filtercmap=["Blues","Greens","Reds","Oranges","Greys","Purples"]

LSST_SkyBrightness=np.array([22.03,21.68,21.02,19.7,17.83,17.21])
LSST_GeomSeeing=np.array([1.1,1.02,0.95,0.92,0.88,0.94])

#---------------------------------------------------------
# Definition of SED files
# - Picles in units erg/cm2/s/nm
sed_file="regenerated_sedgrid_pickle_uvk.fits"

sidx_num=0
sidx_val=0
sidx_sed=0
sidx_data=0
sidx_spec=0

# cadence extraction
cadence_atm_program_file='cadence_field1000.csv'

# atmospheric transparency file
atmospheric_file='cadence_field1000_atm_sim_{}.fits'.format(1)
idx_num=0
idx_night=0
idx_date=0
idx_date=0
idx_am=0
idx_filt=0
idx_vaod=0
idx_pwv=0
idx_o3=0
idx_cld=0
idx_res=0
#---------------------------------------------------------
output_dir="/sps/lsst/data/PCWG_MiniDataChallenge/pickles_uvk/2018-09-10"
#---------------------------------------------------------
def GetSEDData(filename):
     hdu = fits.open(filename)
     #hdu.info()
     theheader=hdu[0].header
     #print(theheader)
     sidx_num=theheader['IDX_NUM']
     sidx_val=theheader['IDX_VAL']
     sidx_sed=theheader['IDX_SED']
     sidx_data=theheader['IDX_DATA']
     sidx_spec=theheader['IDX_SPEC']

     return hdu[0].data,sidx_num,sidx_val,sidx_sed,sidx_data,sidx_spec
#---------------------------------------------------------
def GetCadenceData(filename):     
    df=pd.read_csv(filename,index_col=False)
    return df
#-----------------------------------------------------------
def GetAtmosphericTransparencyData(filename):
    hdu = fits.open(filename)    
    #hdu.info()
    theheader=hdu[0].header
    #print(theheader)
    idx_num=theheader['ID_NUM']
    idx_night=theheader['ID_NIGHT']
    idx_date=theheader['ID_DATE']
    idx_date=theheader['ID_EXMJD']
    idx_am=theheader['ID_AM']
    idx_filt=theheader['ID_FILT']
    idx_vaod=theheader['ID_VAOD']
    idx_pwv=theheader['ID_PWV']
    idx_o3=theheader['ID_O3']
    idx_cld=theheader['ID_CLD']
    idx_res=theheader['ID_RES']
    
    
    return hdu[0].data,idx_num,idx_night,idx_date,idx_am,idx_filt,idx_vaod,idx_pwv,idx_o3,idx_cld,idx_res
#-------------------------------------------------------------
def PlotAtmosphericTransmissionData(data):
    NBATM=data.shape[0]-1
    plt.figure(figsize=(5,4))
    for count in np.arange(NBATM):
        plt.plot(data[0,idx_res:],data[count+1,idx_res:])
    plt.grid(True)
    plt.title("Atmospheric transmission")
    plt.xlabel("$\lambda$ (nm)")
    plt.show()
#-----------------------------------------------------------
def PlotSED(wl,flux):
    
    plt.figure(figsize=(5,4))
    plt.plot(wl,flux,'b-')
    plt.grid(True)
    plt.title(picklesname)
    plt.show()
#----------------------------------------------------------


def entry(arg1):
    """
    """
    
    num=int(arg1)
    
    # do whatever the script does
    print("main arg1={}, num={} ".format(arg1,num))

    # 1) Get SED file
    sed_data,sidx_num,sidx_val,sidx_sed,sidx_data,sidx_spec=GetSEDData(sed_file)
    NBSED=sed_data.shape[0]-1

    # 2) Atmosphere simulation
    am=1.2
    pressure = 782.5
    pwv=4
    aer=0
    ozone=350.
    wl0=500.
   
    path,thefile=rt.ProcessSimulationaer(am,pwv,ozone,wl0,aer)
    #path,thefile=ProcessSimulation(am,pwv,ozone)
    rtdata = np.loadtxt(os.path.join(path,thefile))
    wl=rtdata[:,0]
    tr=rtdata[:,1]

     #4) Telescope
    tel=Telescope()
    #tel.Plot_Throughputs()



    #5) Selection of Pickles

        
    sidx=1
    if num>=1 and num<NBSED:
        sidx=num
    else:
        print("the number of SED must be such 1 < n < {}".format(NBSED))
        sys.exit(2)
    
    picklesname='Pickles {}'.format(sidx)
    picklesnum="{:06d}".format(sidx)
    
    output_file1="magabsim_pickles_{}.txt".format(picklesnum)
    output_file2="info_magabsim_pickles_{}.txt".format(picklesnum)
    
    print("output files = {}, {}".format(output_file1,output_file2))

    output_file1=os.path.join(output_dir,output_file1)
    output_file2=os.path.join(output_dir,output_file2)
    
    #print("sidx_spec={}".format(sidx_spec))
    wl_sed=sed_data[0,sidx_spec:]/10.
    flux_sed=sed_data[sidx,sidx_spec:]*10.
   

    #PlotSED(wl_sed,flux_sed)


    # set the telescope to use this SED
    tel.Set_SED(wavel=wl_sed,newsed=flux_sed,name=picklesname)

    all_magab_infilter = []
    all_magerr_infilter = []
    
    # Loop on filters
    for filter_band in all_filtername:
        
        filternum=all_filternum[filter_band]-1
        skybrightness=LSST_SkyBrightness[filternum]
        FWHMgeom=LSST_GeomSeeing[filternum]
    
    
        # force the telescope throughput with this new atmosphere
        tel.Set_Atmosphere(am,wl,tr)
        #tel.Plot_Throughputs()
    
        # calculate the magnitude and the error
        mag_ab=tel.CalcMyABMagnitude_filter(filter_band)
        mag_err=tel.CalcMyABMagnitudesError_filter(filter_band,skybrightness,FWHMgeom)
        
 
        all_magab_infilter.append(mag_ab)
        all_magerr_infilter.append(mag_err)
 
    #save files
    #fmt1='%1.4f %d %8.5f %8.5f' 
    #np.savetxt(output_file1,np.c_[all_am,all_filt_num,all_mag_adu,all_mag_err],header="airmass \t filter(1..6) \t instrum-mag (ADU) \t error-mag",fmt=fmt1)
    #print("output file = {} saved ".format(output_file1))
    #array_for_output2=np.c_[all_am,all_filt_num,all_vaod,all_o3,all_pwv,all_clouds,all_mag_adu,all_mag_err]
    #header2="airmass \t filter(1..6) \t vaod \t o3 \t pwv \t clouds \t instrum-mag (ADU) \t error-mag"
    #fmt2='%1.4f %d %6.3f %6.3f %6.3f %6.3f %8.5f %8.5f'     
    #np.savetxt(output_file2,array_for_output2,header=header2,fmt=fmt2)
    #print("output file = {} saved ".format(output_file2))
    
   
    print("sed = {:d} , am = {:4.3f} , mag :: u={:6.3f} g={:6.3f} r={:6.3f} i={:6.3f} z={:6.3f} y={:6.3f} ".format(sidx,am,all_magab_infilter[0],all_magab_infilter[1], all_magab_infilter[2], all_magab_infilter[3], all_magab_infilter[4],all_magab_infilter[5])) 
#-----------------------------------------------------------------------------------------------    
    
    
#----------------------------------------------------------------------------------------------------    
# python libGenerateABMagnitudes.py -n 1
#----------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"n:h",['n=','help'])
    except getopt.GetoptError:
        print(' Exception bad getopt with :: '+sys.argv[0]+ ' -n <pickles-number>')
        sys.exit(2)
        

    snum=""
    num=0
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(sys.argv[0]+ ' -n <pickles-number>')
            sys.exit(2)
        elif opt in ('-n', '--num'):
            snum = arg
            num=int(snum)
        else:
            print(sys.argv[0]+ ' -n <pickles-number>')
            sys.exit(2)
 
    print("snum={} , num={} ".format(snum,num))
    
    

    # 1) Get SED file
    sed_data,sidx_num,sidx_val,sidx_sed,sidx_data,sidx_spec=GetSEDData(sed_file)
    NBSED=sed_data.shape[0]-1

    # 2) Atmosphere simulation
    am=1.2
    pressure = 782.5
    pwv=4
    aer=0
    ozone=350.
    wl0=500.
   
    path,thefile=rt.ProcessSimulationaer(am,pwv,ozone,wl0,aer)
    #path,thefile=ProcessSimulation(am,pwv,ozone)
    rtdata = np.loadtxt(os.path.join(path,thefile))
    wl=rtdata[:,0]
    tr=rtdata[:,1]
 
   

    #4) Telescope
    tel=Telescope()
    #tel.Plot_Throughputs()



    #5) Selection of Pickles       
    sidx=1
    if num>=1 and num<NBSED:
        sidx=num
    else:
        print("the number of SED must be such 1 < n < {}".format(NBSED))
        sys.exit(2)
    
    picklesname='Pickles {}'.format(sidx)
    picklesnum="{:06d}".format(sidx)
    
  
    wl_sed=sed_data[0,sidx_spec:]/10.
    flux_sed=sed_data[sidx,sidx_spec:]*10.
    #PlotSED(wl_sed,flux_sed)


    # set the telescope to use this SED
    tel.Set_SED(wavel=wl_sed,newsed=flux_sed,name=picklesname)


    # do the calculation
    all_magab_infilter = []
    all_magerr_infilter = []
    
    # Loop on filters
    for filter_band in all_filtername:
        
        filternum=all_filternum[filter_band]-1
        skybrightness=LSST_SkyBrightness[filternum]
        FWHMgeom=LSST_GeomSeeing[filternum]
    
    
        # force the telescope throughput with this new atmosphere
        tel.Set_Atmosphere(am,wl,tr)
        #tel.Plot_Throughputs()
    
        # calculate the magnitude and the error
        mag_ab=tel.CalcMyABMagnitude_filter(filter_band)
        mag_err=tel.CalcMyABMagnitudesError_filter(filter_band,skybrightness,FWHMgeom)
        
 
        all_magab_infilter.append(mag_ab)
        all_magerr_infilter.append(mag_err)
 

    

    print("sed = {:d} , am = {:4.3f} , mag :: u={:6.3f} g={:6.3f} r={:6.3f} i={:6.3f} z={:6.3f} y={:6.3f} ".format(sidx,am,all_magab_infilter[0],all_magab_infilter[1], all_magab_infilter[2], all_magab_infilter[3], all_magab_infilter[4],all_magab_infilter[5])) 
    
    
   
    
    
