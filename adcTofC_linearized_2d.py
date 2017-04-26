# Import tools
from ROOT import *
from math import sqrt
import sys
import re
from array import array 
import os
import string
import sqlite3 as lite
import csv
from linearADC import *
from read_histo_2d import *

gROOT.SetBatch(kTRUE)
nominalMapping = { 1 : 4,
                   2 : 4,
                   3 : 4,
                   4 : 4,
                   5 : 1,
                   6 : 2,
                   7 : 4,
                   8 : 4,
                   }



def makeADCvsfCgraphSepCapID(values,mean, rms, charge,histo_list = range(0,96), linkMap = {}, injectionCardMap = {},qieRange=0,shuntMult=1):

   

    print 'Making TGraphs from histos'
    
    #print mean
    graphs = {}
    i_range=qieRange
    if shuntMult == 1:
            qierange = range(4)
    else :
            qierange = range(2)
    if i_range > 0 or shuntMult>1:
        highCurrent = True
    else:
        highCurrent = False
    lsbList = values[histo_list[0]].keys()
    lsbList.sort()
    for ih in histo_list:
           # for i_lsb in lsbList:
		channel = (ih % 12 + 1)        
	    	
	
		_charge = array("d",charge[i_range][ih][:-1])
		_chargeErr = array("d",[0 for i in range(len(charge[i_range][ih][:-1]))])
		graphs[ih] = []	
		for i_capID in range(4):		
                	ADCvsfC=(TGraphErrors(len(mean[i_range][ih][i_capID]),_charge,mean[i_range][ih][i_capID],_chargeErr,rms[i_range][ih][i_capID]))
                	ADCvsfC.SetNameTitle("LinADCvsfC_%i_%i_range_%i_shunt_%i_%i_capID_%i"%(ih, channel,i_range,int(shuntMult),int(shuntMult%1*10),i_capID),"LinADCvsfC_%i_%i_range_%i_shunt_%i_%i_capID_%i"%(ih, channel,i_range,int(shuntMult),int(shuntMult%1*10),i_capID))
			for p in range(ADCvsfC.GetN()):
				 if i_range==0:
				 	if ADCvsfC.GetY()[p] < 1 or ADCvsfC.GetY()[p] >linADC(62)[0]:
						 ADCvsfC.RemovePoint(p)
				 if i_range==1:
					if ADCvsfC.GetY()[p] < linADC(64)[0] or ADCvsfC.GetY()[p] >linADC(126)[0]:
						 ADCvsfC.RemovePoint(p)
				 if i_range==2:
					if ADCvsfC.GetY()[p] < linADC(128)[0] or ADCvsfC.GetY()[p] >linADC(190)[0]:
						ADCvsfC.RemovePoint(p)
				 if i_range==3:
					if ADCvsfC.GetY()[p] < linADC(192)[0] or ADCvsfC.GetY()[p] >linADC(254)[0]:
						ADCvsfC.RemovePoint(p)
				 if ADCvsfC.GetX()[p] < 0:
					 ADCvsfC.RemovePoint(p)
			if i_range==0:ADCvsfC.RemovePoint(0) 
                	graphs[ih].append(ADCvsfC)
         
    return graphs

    
