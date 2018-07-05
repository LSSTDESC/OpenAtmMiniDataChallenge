# OpenAtmMiniDataChallenge


The new version for MiniDataChallenge open to PCWG members

- author : Sylvie Dagoret-Campagne
- affiliation : LAL/IN2P3/CNRS/France
- creation date : July 5th 2018

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
						
-----------------------


git remote set-url origin git@github.com:LSSTDESC/OpenAtmMiniDataChallenge.git
