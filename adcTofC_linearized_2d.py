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


c1 = TCanvas('c1', 'Plots', 1000, 500)
c1.SetFillColor(0)
c1.SetGrid()
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
		channel = (ih % 12 + 1)        
	    	
	
		_charge = array("d",charge[i_range][ih][:-1])
		_chargeErr = array("d",[0 for i in range(len(charge[i_range][ih][:-1]))])
		graphs[ih] = []	
		#print len(mean[1][14][1]),len(charge[1][14][:-1])
		for i_capID in range(4):		
		#	if ih ==14 and shuntMult==1.5 and i_capID==1 and i_range==0:
		#		print "the root of all trouble mean:",len(mean[0][14][1])
		#		print " the charge is :",len(_charge)
		#		gr = TGraphErrors(len(mean[i_range][ih][i_capID]),_charge,mean[i_range][ih][i_capID],_chargeErr,rms[i_range][ih][i_capID])
		#		gr.Draw('ap')
		#		c1.SaveAs("trial_1.pdf")
                	ADCvsfC=(TGraphErrors(len(mean[i_range][ih][i_capID]),_charge,mean[i_range][ih][i_capID],_chargeErr,rms[i_range][ih][i_capID]))
                	ADCvsfC.SetNameTitle("LinADCvsfC_%i_%i_range_%i_shunt_%.1f_capID_%i"%(ih, channel,i_range,float(shuntMult),i_capID),"LinADCvsfC_%i_%i_range_%i_shunt_%.1f_capID_%i"%(ih, channel,i_range,float(shuntMult),i_capID))
		#	print "LinADCvsfC_%i_%i_range_%i_shunt_%i_%i_capID_%i"%(ih, channel,i_range,int(shuntMult),int(shuntMult%1*10),i_capID)
			points = range(ADCvsfC.GetN())
			points.reverse()
			MinSaveValue = linADC(i_range*64 + 2)[0]
    			MaxSaveValue = linADC(i_range*64 + 61)[0]
			maxPointNumber = 999
    			minPointNumber = -1
		#	if shuntMult==1.5:
                 #                ADCvsfC.RemovePoint(points[0])
 			
		#	ADCvsfC.RemovePoint(points[len(points)-1])
			for p in points:
		#		if i_range==0:
		#		 	if (ADCvsfC.GetY()[p] < 1 or ADCvsfC.GetY()[p] >linADC(61)[0]):
		#				 ADCvsfC.RemovePoint(p)
		#		if i_range==1:
		#			if (ADCvsfC.GetY()[p] < linADC(64)[0] or ADCvsfC.GetY()[p] >linADC(122)[0]):
		#				 ADCvsfC.RemovePoint(p)
		#		if i_range==2:
		#			if (ADCvsfC.GetY()[p] < linADC(128)[0] or ADCvsfC.GetY()[p] >linADC(185)[0]):
		#				ADCvsfC.RemovePoint(p)
		#		if i_range==3:
		#			if (ADCvsfC.GetY()[p] < linADC(192)[0] or ADCvsfC.GetY()[p] >linADC(249)[0]):
		#				ADCvsfC.RemovePoint(p)
		#		if ADCvsfC.GetX()[p] < 0:
		#			 ADCvsfC.RemovePoint(p)
				if i_range==0 and shuntMult==1.5:
					ADCvsfC.RemovePoint(p)
        			if ADCvsfC.GetY()[p] > MaxSaveValue:
            				maxPointNumber = p
        			if ADCvsfC.GetY()[p] > MinSaveValue:
					minPointNumber = p
		#	if i_range==0 :
		#		for i in range(6):		
			ADCvsfC.RemovePoint(0)

    			#remove everything after the last point                                                                                   
    		 	if maxPointNumber < 999:
        			while (ADCvsfC.GetN() > maxPointNumber):
            				ADCvsfC.RemovePoint(maxPointNumber)


    			#remove the first N points, where N = minPointNumber                                                                      
		        if minPointNumber > -1:
        			for i in range(minPointNumber):
            				ADCvsfC.RemovePoint(0)
			
                	graphs[ih].append(ADCvsfC)
         
    return graphs

    
