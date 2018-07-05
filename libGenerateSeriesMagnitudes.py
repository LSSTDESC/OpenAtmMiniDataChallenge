
# coding: utf-8

# # Generate series of Magnitudes from Cadence
# 
# Test My Telescope cloned from Telescope of Philippe Gris
# 
# - author : Sylvie Dagoret-Campagne
# - date   : Jul 5thth 2018
# - update : Jul 5th 2018
# 



import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np
import sys
import os
import pandas as pd



from astropy.io import fits


# to enlarge the sizes
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (10, 6),   #defines the default image size
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
plt.rcParams.update(params)



from lsst.sims.photUtils import SignalToNoise
from lsst.sims.photUtils import PhotometricParameters
from lsst.sims.photUtils import Bandpass,Sed

from MyTelescope import *
from MyThroughputs import *

#---------------------------------------------------------
# Definition of SED files
# - Picles in units erg/cm2/s/nm
sed_file="regenerated_sedgrid_pickle_uvi.fits"

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
idx_res=0

#---------------------------------------------------------
def GetSEDData(filename):
     hdu = fits.open(filename)
     theheader=hdu[0].header
     print(theheader)
     sidx_num=theheader['IDX_NUM']
     sidx_val=theheader['IDX_VAL']
     sidx_sed=theheader['IDX_SED']
     sidx_data=theheader['IDX_DATA']
     sidx_spec=theheader['IDX_SPEC']

     return hdu[0].data
#---------------------------------------------------------
def GetCadenceData(filename):     
    df=pd.read_csv(filename,index_col=False)
    return df
#-----------------------------------------------------------
def GetAtmosphericTransparencyData(filename):
    hdu = fits.open(filename)    
    hdu.info()
    theheader=hdu[0].header
    print(theheader)
    idx_num=theheader['ID_NUM']
    idx_night=theheader['ID_NIGHT']
    idx_date=theheader['ID_DATE']
    idx_date=theheader['ID_EXMJD']
    idx_am=theheader['ID_AM']
    idx_filt=theheader['ID_FILT']
    idx_vaod=theheader['ID_VAOD']
    idx_pwv=theheader['ID_PWV']
    idx_o3=theheader['ID_O3']
    idx_res=theheader['ID_RES']
    return hdu[0].data
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

    
if __name__ == "__main__":
    
   
    # 1) Get SED file
    sed_data=GetSEDData(sed_file)


    #2) Get Cadence file
    df=GetCadenceData(cadence_atm_program_file)    
    df.head()
    NBVISITS=len(df)
    print("Nb visits = {}".format(NBVISITS))


    #3) Atmospheric transparency data
    atmdata=GetAtmosphericTransparencyData(atmospheric_file)
    NBATM=atmdata.shape[0]-1

    PlotAtmosphericTransmissionData(atmdata)

    am=atmdata[1:,idx_am] # airmass distribution
    filt=atmdata[1:,idx_filt] # filter distribution
    vaod=atmdata[1:,idx_vaod] # aerosols distribution
    pwv=atmdata[1:,idx_pwv] # pwv distribution
    o3=atmdata[1:,idx_o3] # o3 distribution


     #4) Telescope
    tel=Telescope()
    tel.Plot_Throughputs()



    #5) Selection of Pickles

    sidx=1
    picklesname='Pickles {}'.format(sidx)
    picklesnum="{:06d}".format(sidx)
    output_file="magsim_pickles_{}.txt".format(picklesnum)


    wl_sed=sed_data[0,sidx_spec:]/10.
    flux_sed=sed_data[sidx+1,sidx_spec:]*10.


    PlotSED(wl_sed,flux_sed)


    # set the telescope to use this SED
    tel.Set_SED(wavel=wl_sed,newsed=flux_sed,name=picklename)


    # MAIN LOOP ON VISITS
    #======================



    all_mag_adu=[]
    all_mag_err=[]
    all_filt_num=[]
    all_am=[]
    for visit in np.arange(NBVISITS):
        idx=visit+1
    
        # from atmospheric simulation
        am=atmdata[idx,idx_am] 
        wl=atmdata[0,idx_res:]
        tr=atmdata[idx,idx_res:]
    
    
    
        #decode cadence
        data_series=df.iloc[visit]
        #print(data_series)
        filter_band=data_series["filter"]
        filternum=tel.filternum[filter_band]
        skybrightness=data_series["filtskybrightness"]
        transparency=1.-data_series["transparency"]
        FWHMgeom=data_series["finseeing"]
    

        tr_res=transparency*tr   # cloud effect
    
        #print("filter={}  skybrightness={}  FWHMGeom= {}   transparency= {}".format(filter_band,skybrightness,FWHMgeom,transparency))
    
        # force the telescope throughput with this new atmosphere
        tel.Set_Atmosphere(am,wl,tr_res)
        #tel.Plot_Throughputs()
    
        # calculate the magnitude and the error
        mag_adu=tel.CalcMyADUMagnitude_filter(filter_band)
        mag_err=tel.CalcMyABMagnitudesError_filter(filter_band,skybrightness,FWHMgeom)

        #print("filt={} : ADU = {}  +/- {}".format(filter_band,mag_adu,mag_err))
    
        all_mag_adu.append(mag_adu)
        all_mag_err.append(mag_err)
        all_filt_num.append(filternum)
        all_am.append(am)
    
    all_mag_adu=np.array(all_mag_adu)
    all_mag_err=np.array(all_mag_err)
    all_filt_num=np.array(all_filt_num)
    all_am=np.array(all_am)


    #save file
    np.savetxt(output_file,np.c_[all_am,all_filt_num,all_mag_adu,all_mag_err],header="airmass \t filter(1..6) \t instrum-mag (ADU) \t error-mag")

