# OpenAtmMiniDataChallenge


The new version for MiniDataChallenge open to PCWG members

- author : Sylvie Dagoret-Campagne
- affiliation : LAL/IN2P3/CNRS/France
- creation date : July 5th 2018
- update : July 13

## Purpose
From Series of SED (pickles), from Cadence data (MINION 1016), generate Instrumental magnitudes with errors.  

## Note:
LSST\_SIM is used to calculate Instrumental and AB Magnitudes, and their errors,in addition to 

- Zero point
- Dark Sky

The cadence parameters extraction and atmospheric simulation had been done before.

## notebooks
###***TestMyTelescope.ipynb***
Debug the calculation of flux and magnitudes and errors 
###***TestGenerateSeriesMagnitudes.ipynb***
First example with a full cadence
###***ViewRegeneratedSED.ipynb***
View simulated SED
###***CheckRegeneratedSED.ipynb***
Check the magnitude and color distributions of regenerated sample 

## Code
This code define two python classes to access to LSST throughputs.
These two classes has been originally developped by P.Gris as a toolbox (private use).
I have modified these classes for my simulation purpose.
### ***MyTelescope.py***		
Telescope class		
### ***MyThroughputs.py***
Throughput class

## ipython console

run libGenerateSeriesMagnitudes -n 3

## shell

python libGenerateSeriesMagnitudes -n 3


## Production of a large dataset

- ***GenerateManyPicklesMagnitudes.py***

to run it do

  python GenerateManyPicklesMagnitudes.py -f 1 -l 1000

Generate dataset of magnitudes and errors from first sed number 1 to last sed number 1000

## Compute AB magnitudes
- ***libGenerateABMagnitudes.py

python libGenerateABMagnitudes.py -n 2125
	
    
or


    
-----------------------

implemented for python3
git remote set-url origin git@github.com:LSSTDESC/OpenAtmMiniDataChallenge.git
