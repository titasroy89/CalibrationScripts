from datetime import date, datetime
from time import sleep
import os
from optparse import OptionParser
import subprocess
import sys
from numpy import std
from ROOT import *
import re
from array import array
from getPedestals import *

#script to control DAC
from DAC import *

#from scans import *
# from adcTofC import *
from fitGraphs_linearized_2d import *
from adcTofC_linearized_2d import *
#from fitGraphs_linearized_2d import *

from GraphParamDist_2d import *

from FitUncertaintyPlots import *

slotDict = {1:[18,19,20,21,23,24,25,26],
            }

shunt_Val ={1:0,
            1.5:1,
            2:2,
            3:4,
            4:8,
            5:16,
            6:18,
            7:20,
            8:24,
            9:26,
            10:28,
            11:30,
            11.5:31}        
shuntMultList = shunt_Val.keys()
shuntMultList.sort()
Barcode_UID ={hex(0xead4b070):600028,
	      hex(0xeabb9870):600549,
	      hex(0xeab47170):600639,
	      hex(0xead65570):600709,
	      hex(0xeacc8d70):600458,
	      hex(0xea93f270):600425,
	      hex(0xeacd8870):600426,
	      hex(0xea9db770):600429,
	      hex(0xeabb1f70):600489,
	      hex(0xeaaeaa70):600033,
	      hex(0xeabfc070):600078,
	      hex(0xeaa7ef70):600095,
	      hex(0xeabcff70):600106,
	      hex(0xead3d470):600463,
	      hex(0xea9e6d70):600501,
	      hex(0xeaa72770):600670}
	     # hex(0xead5c870):600064,
	     # hex(0xead60170):600658}  
BarcodeList = Barcode_UID.keys()
BarcodeList.sort()


import sqlite3 as lite
mg = TMultiGraph()

from read_histo_2d import read_histo_2d

gROOT.SetBatch(kTRUE)

orbitDelay = 30
GTXreset = 1
CDRreset = 0

### Which slot number contains which injection card {slot:card}
### slots are numbered 1 to 8 (slot 10 contains the DAC, slot 9 has an extra injection card)
### The purpose of this dictionary is to allow for swapping out a nonfunctional card
injectionCardSlotMapping = {1:1,
                            2:2,
                            3:3,
                            4:4,
                            5:5,
                            6:6,
                            7:7,
                            8:8,
                            }

fakesimpleCardMap = {1  : 1 , 2  : 2 , 3  : 3 , 4  : 4 , 5  : 5 , 6  : 6 , 7  : 7 , 8  : 8 , 9  : 9 , 10 : 10, 11 : 11, 12 : 12, 13 : 13, 14 : 14, 15 : 15, 16 : 16, 17 : 17, 18 : 18, 19 : 19, 20 : 20, 21 : 21, 22 : 22, 23 : 23, 24 : 24, 25 : 25, 26 : 26, 27 : 27, 28 : 28, 29 : 29, 30 : 30, 31 : 31, 32 : 32,
                             }


def getValuesFromFile(outputDir):
        """
        Gets data from the cardData text file from the previous run
        Gets things like the injection mapping, QIE ranges used, etc.
        """

        dataFile = open(outputDir+"/cardData.txt",'r')
        for line in dataFile:

                if 'DAC' in line and 'Used' in line:
                        dacNumber = line.split()[1]
                if 'linkMap' in line:
                        linkMap = eval(line.split('linkMap')[-1])
                if 'injectionCardMap' in line:
                        injectionCardMap = eval(line.split('injectionCardMap')[-1])
        return linkMap, injectionCardMap 
                

def ShuntScan(shuntMult=1, outputDirectory = '', linkMap={},injectionCardMap={}):
         files = os.listdir(outputDirectory)
	 final_file = ''
	 for f in files:
	 	if 'QIECalibration_' in f:
			final_file = outputDirectory+f
	 if final_file=='':
		print 'Unable to find data file in directory %s'%outputDirectory
		print 'Exiting'
		sys.exit()
         #final_file = outputDirectory+'QIECalibration_1.root'

	 linkMap, injectionCardMap = getValuesFromFile(outputDirectory)

         linkMap, injectionCardMap = getValuesFromFile(outputDirectory)
         val, mean, rms, charge= read_histo_2d(file_in=final_file,shuntMult=shuntMult,linkMap=linkMap, injectionCardMap=injectionCardMap)
	 
         return val, mean, rms, charge

def QIECalibrationScan(options):

        ts = None



        outputDirectory = options.Directory + '/'
        rootfile = options.filename
        final_file = outputDirectory+rootfile
        
        print "the root file is %s"%rootfile
        print "Reading from directory %s"%outputDirectory
        print "final file is %s"%final_file



        linkMap, injectionCardMap = getValuesFromFile(outputDirectory)
	#print linkMap[0]['slot']

        simpleCardMap = fakesimpleCardMap

        histoList = []
        for link in linkMap:
		histoList += [link*6,link*6+1,link*6+2,link*6+3,link*6+4,link*6+5]
        print '-'*30
        print 'Histograms List'
        print '-'*30
        print histoList

    




        outputParamFile = open(outputDirectory+"calibrationParams.txt",'w')
        outputParamFile.write('(qieID, barcode, qieNum, capID, qieRange,shuntMult,Gsel,slope,offset,uncertainty)\n')

        uID_list = []
        for link in linkMap:
                uID = linkMap[link]['unique_ID'].replace(' ','_')
				
		#print linkMap[link]['unique_ID'].split()[1]
                if not uID in uID_list:
                        uID_list.append(uID)
		

        #sys.exit()


        qieParams={}
        cursor = {}
        for uID in uID_list:
                 outputGraphFile = TFile("%s/fitResults_%s.root"%(outputDirectory, uID),"recreate")
                 outputGraphFile.mkdir("adcVsCharge")
                 outputGraphFile.mkdir("LinadcVsCharge")
                 outputGraphFile.mkdir("fitLines")
                 outputGraphFile.mkdir("Shunted_adcVsCharge")
                 outputGraphFile.mkdir("Shunted_LinadcVsCharge")
                 outputGraphFile.mkdir("Shunted_fitLines")
                 outputGraphFile.mkdir("SummaryPlots")
                 outputGraphFile.Close()
 
                 qieParams[uID] = lite.connect(outputDirectory+"qieCalibrationParameters_%s.db"%(uID))
                 cursor[uID] = qieParams[uID].cursor()
                 cursor[uID].execute("drop table if exists qieshuntparams")
 
                 cursor[uID].execute("create table if not exists qieshuntparams(id STRING, barcode STRING, qie INT, capID INT, range INT, shunt INT, Gsel INT, slope REAL, offset REAL, uncertainty REAL)")




        ### Graph parameters
        outputParamFile_shunt = open(outputDirectory+"calibrationParams_shunt.txt",'w')
        outputParamFile_shunt.write('(qieID, barcode,qieNum, capID, qieRange, shuntMult, Gsel,slope, offset, uncertainty)\n') 
        
        if options.RunShunt:
                print " Shunt Scans begin"
        if options.shuntList == '-1':
            shuntMult_list = shunt_Val.keys()
        else:
            shuntMult_list = eval(options.shuntList)

        if type(shuntMult_list)==type(int()):
                shuntMult_list = [shuntMult_list]
        shuntMult_list.sort()


	pedestalVals = {}


	pedestal_graphs_shunt ={}
        for shuntMult in shuntMult_list:
                output={}
                shuntOutputDirectory = outputDirectory #+ "Data_%s_%s/"%(rangeMode, shuntMode)
                vals, mean, rms, charge = ShuntScan(shuntMult=shuntMult, outputDirectory=outputDirectory, linkMap=linkMap,injectionCardMap=injectionCardMap)
		
		pedestal_graphs_shunt[shuntMult] = makeADCvsfCgraphSepCapID(vals[0],mean, rms, charge, histoList,linkMap=linkMap,injectionCardMap=injectionCardMap,qieRange=0,shuntMult=shuntMult)

	dirStructure = outputDirectory.split('/')
	for value in dirStructure:
		if '2016' in value:
			date = value
		if 'Run' in value:
			run = value
	_filePeds = TFile("%s/PedestalPlots/pedestalMeasurement_%s_%s.root"%(outputDirectory,date, run),"recreate")
	_filePeds.Close()
	print "Now Get Pedestals"

	pedestalVals = getPedestals(pedestal_graphs_shunt,shuntMult_list,histoList,outputDirectory, date, run)

#	for ih in histoList:
		#print pedestal_graphs_shunt[1.0][ih]
		#print pedestalVals[ih]
	high_slope=[]
	shuntFactors={}
        for shuntMult in shuntMult_list:
		shuntFactors[shuntMult]={}
                graphs_shunt ={}
                output={}
                print "Now on shuntMult %.1f"%shuntMult
                shuntOutputDirectory = outputDirectory #+ "Data_%s_%s/"%(rangeMode, shuntMode)
                vals, mean, rms, charge = ShuntScan(shuntMult=shuntMult, outputDirectory=outputDirectory)
                print "this is:",outputDirectory
                if shuntMult == 1:
			qieRange= range(4)
                else:
			qieRange=range(2)

                for i_range in qieRange:
			histoList =  vals[i_range].keys()
			histoList.sort()
			graphs_shunt[i_range] = makeADCvsfCgraphSepCapID(vals[i_range],mean, rms, charge, histoList,linkMap=linkMap,injectionCardMap=injectionCardMap,qieRange=i_range,shuntMult=shuntMult)
		shunts_method1 = [array('d') for i in range(12)]
                for ih in histoList:
			
			linkNum = int(ih/6)
			qieID = linkMap[linkNum]['unique_ID']
			
			#print qieID
			uID_barcode = linkMap[linkNum]['unique_ID'].split()[1]
			#print uID_barcode
			shuntFactors[shuntMult]
			if uID_barcode not in BarcodeList:
				barcode = 600000
				for i in range(12):
					for r in range(12):
						shunts_method1[i].append(float(shuntMult))
			else:
				barcode = Barcode_UID[uID_barcode] 
				
				f1 = open("/Users/titasroy/cmshcal11_github/Method1_shuntfactors_%s.txt"%(uID_barcode)).readlines()
                                for line in f1:
                                        for i in range(12):
                                		shunts_method1[i].append(float(line.split()[i]))
			
				print len(shunts_method1)
				print len(shunts_method1[0])
			#sys.exit()

			#print "Barcode is:",barcode
			qieNum =ih%12 + 1
			graphList_shunt=[]

			if 0 in graphs_shunt:
				graphList_shunt.append(graphs_shunt[0][ih])
			else:
				graphList_shunt.append(None)
			if 1 in graphs_shunt:
				graphList_shunt.append(graphs_shunt[1][ih])
			else:   
				graphList_shunt.append(None)
			if 2 in graphs_shunt:
				graphList_shunt.append(graphs_shunt[2][ih])
			else:
				graphList_shunt.append(None)
			if 3 in graphs_shunt:
				graphList_shunt.append(graphs_shunt[3][ih])
			else:
				graphList_shunt.append(None)
			if shuntMult ==1 :
				params_shunt, high_ranges =  doFit_combined(graphList = graphList_shunt, saveGraph = options.saveGraphs, qieNumber = qieNum, qieUniqueID = qieID.replace(' ', '_'), useCalibrationMode = False, outputDir = outputDirectory, shuntMult=shuntMult, pedestalVals = pedestalVals[ih])
			else:
				params_shunt, high_vals =  doFit_combined(graphList = graphList_shunt, saveGraph = options.saveGraphs, qieNumber = qieNum, qieUniqueID = qieID.replace(' ', '_'), useCalibrationMode = False, outputDir = outputDirectory, shuntMult=shuntMult, pedestalVals = pedestalVals[ih])
			high_slopes=high_ranges
			uID = qieID.replace(' ', '_')
				
			#for i_range in graphs_shunt:
			for i_range in range(4):
				for i_capID in range(4):
					if (shuntMult==1 and( i_range==0 or i_range==1 or i_range==2 or i_range==3)) or i_range==0 or i_range==1:
						print shuntMult, i_range
						values_shunt = (qieID, barcode, qieNum, i_capID, i_range, shuntMult,shunt_Val[shuntMult], (params_shunt[i_range][i_capID][0]),(params_shunt[i_range][i_capID][1]),(params_shunt[i_range][i_capID][2]))
						cursor[uID].execute("insert into qieshuntparams values (?,?,?, ?, ?, ?, ?, ?, ?, ?)",values_shunt)
					elif (shuntMult ==1.5 or shuntMult==2 or shuntMult==3 or shuntMult==4 or shuntMult==5 or shuntMult==6 or shuntMult==7 or shuntMult==8 or shuntMult==9 or shuntMult==10 or shuntMult==11) and (i_range==2 or i_range==3):
						print shuntMult, i_range, qieNum, int(shuntMult)-1
						print shunts_method1[int(shuntMult)-1][int(qieNum-1)]
						values_shunt = (qieID, barcode, qieNum, i_capID, i_range, shuntMult,shunt_Val[shuntMult], (high_slopes[i_capID][0])/shunts_method1[int(shuntMult)-1][qieNum-1],(high_slopes[i_capID][1])/shunts_method1[int(shuntMult)-1][qieNum-1],(high_slopes[i_capID][2])/shunts_method1[int(shuntMult)-1][qieNum-1])
						cursor[uID].execute("insert into qieshuntparams values (?,?,?, ?, ?, ?, ?, ?, ?,?)",values_shunt)
					if shuntMult==11.5 and (i_range==2 or i_range==3):
						print shuntMult, i_range
						values_shunt = (qieID, barcode, qieNum, i_capID, i_range, shuntMult,shunt_Val[shuntMult], (high_slopes[i_capID][0])/shunts_method1[11][qieNum-1],(high_slopes[i_capID][1])/shunts_method1[11][qieNum-1],(high_slopes[i_capID][2])/shunts_method1[11][qieNum-1])
                                                cursor[uID].execute("insert into qieshuntparams values (?,?,?, ?, ?, ?, ?, ?, ?,?)",values_shunt)

					# print values_shunt
					outputParamFile_shunt.write(str(values_shunt)+'\n')
         
        outputParamFile_shunt.close()

        for uID in uID_list:
                cursor[uID].close()
                qieParams[uID].commit()
                qieParams[uID].close()

        for uID in uID_list:
                graphParamDist(outputDirectory+"qieCalibrationParameters_%s.db"%uID)

		problemCards = []
                outputFileName = "%s/fitResults_%s.root"%(outputDirectory, uID)
                badChannels = fillFitUncertaintyHists(outputFileName)
                if len(badChannels) > 0:
                        slot = -1
                        for i_link in linkMap:
                                if linkMap[i_link]['unique_ID']==uID.replace('_',' '):
                                        slot = linkMap[i_link]['slot']
                        problemCards.append([slot,uID.replace('_',' ')])
        for card in problemCards:
                print '*'*40
                print 'PROBLEM WITH FIT IN QIE CARD'
                print '    Slot: ',card[0]
                print '    UnID: ',card[1]

                
if __name__ == "__main__":
        parser = OptionParser()
        parser.add_option("-r", "--range", dest="range", default=-1,type='int',
                          help="Specify range to be used in scan (default is -1, which does all 4 ranges)" )
        parser.add_option("--NoSepCapID", action="store_false",dest="sepCapID",default=True,
                          help="don't separate the different capID histograms")
        parser.add_option("--SkipScan", action="store_true",dest="SkipScan",default=False,
                          help="Skip the scan, using presaved scan")
        parser.add_option("--SkipFit", action="store_true",dest="SkipFit",default=False,
                          help="Skip the fitting step")
        parser.add_option("--NoLinkInit", action="store_true",dest="NoLinkInit",default=False,
                          help="Skip the scan, using presaved scan")
        parser.add_option("--SkipTDC", action="store_false",dest="RunTDCScan",default=True,
                          help="Skip the TDC scans")
        parser.add_option("--SkipExtraTests", action="store_false",dest="RunExtraTests",default=True,
                          help="Skip the Range Transistion and TDC tests")
        parser.add_option("--SkipShunt", action="store_false",dest="RunShunt",default=True,
                          help="Skip the Shunt Scans")
        parser.add_option("--shuntList", dest="shuntList",default="-1",type="str",
                          help="List of shunts to run on, default is -1, which will run all the shunts")
        parser.add_option("-d","--dir", dest="Directory",default="",type="str",
                          help="Data file from previous data taking run to redo the fit on")
        parser.add_option("-f","--filename",dest="filename",default="",type="str",
                          help="Data file from previous data taking run to redo the fit on")
        parser.add_option("--saveGraph","--savegraph","--saveGraphs","--savegraphs",action="store_true",dest="saveGraphs",default=False,
                         help="Save Graphs")
        (options, args) = parser.parse_args()
        print 'start'
        if not options.range == -1:
                options.RunTDCScan=False
        if not options.RunTDCScan:
                options.RunExtraTests = False

        options.RunExtraTests = False

        QIECalibrationScan(options)
        


