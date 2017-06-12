from ROOT import *
import sqlite3
from array import array
gROOT.SetBatch(kTRUE)
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

def graphParamDist(paramFileName):

    outputDirectory = paramFileName.split('qieCalibrationParam')[0]
    #outputDirectory = '/Users/titasroy/cmshcal11_github/Data/database_05_22/'
    paramDB = sqlite3.connect(paramFileName)
    cursor = paramDB.cursor()
    qieCards = [x[0] for x in list(set(cursor.execute("select id from qieshuntparams").fetchall()))]
    print qieCards

    for uniqueID in qieCards:
        
        print uniqueID
        hists = {}
	#slopes_ = [[[array('d') for i in range(12)] for i in range(13)] for i in range(2)]
	slopes_ = {}
       
        parameterValues = cursor.execute("select * from qieshuntparams where id = ?", [str(uniqueID)]).fetchall()
        for shuntMult in shuntMultList:
	    slopes_[shuntMult]={}
	    slopes_[shuntMult][0] = {0:array('d'),
				  1:array('d'),
				  2:array('d'),
				  3:array('d'),} 
            slopes_[shuntMult][1] = {0:array('d'),
                                  1:array('d'),
                                  2:array('d'),
                                  3:array('d'),} 
            slopes_[shuntMult][2] = {0:array('d'),
                                  1:array('d'),
                                  2:array('d'),
                                  3:array('d'),} 
     
	    slopes_[shuntMult][3] = {0:array('d'),
                                  1:array('d'),
                                  2:array('d'),
                                  3:array('d'),} 
            range0MinMax = cursor.execute("select min(slope), max(slope), min(offset), max(offset), min(uncertainty), max(uncertainty) from qieshuntparams where id = ? and range=? and shunt=?", [str(uniqueID),0,shuntMult]).fetchone()
            range1MinMax = cursor.execute("select min(slope), max(slope), min(offset), max(offset), min(uncertainty), max(uncertainty) from qieshuntparams where id = ? and range=? and shunt=?", [str(uniqueID),1,shuntMult]).fetchone()
            range2MinMax = cursor.execute("select min(slope), max(slope), min(offset), max(offset), min(uncertainty), max(uncertainty) from qieshuntparams where id = ? and range=? and shunt=?", [str(uniqueID),2,shuntMult]).fetchone()
            range3MinMax = cursor.execute("select min(slope), max(slope), min(offset), max(offset), min(uncertainty), max(uncertainty) from qieshuntparams where id = ? and range=? and shunt=?", [str(uniqueID),3,shuntMult]).fetchone()

           # if shuntMult>1: 
            #    range3MinMax= [1,1,1,1] 
             #   range2MinMax= [1,1,1,1] 
                #range1MinMax= [1,1,1,1]
            

            hists[shuntMult] = {0:[TH1F("Range0Slopes_shunt%.1f"%shuntMult,"Range0Slopes_shunt%.1f"%shuntMult,100,.94*.3/shuntMult,1.1*.3/shuntMult), TH1F("Range0Offsets_shunt%.1f"%shuntMult,"Range0Offsets_shunt%.1f"%shuntMult,100,-1., 0.), TH1F("Range0Uncertainties_shunt%.1f"%shuntMult,"Range0Uncertainties_shunt%.1f"%shuntMult, 50,1.*10**-8,10.*10**-6)],
                                1:[TH1F("Range1Slopes_shunt%.1f"%shuntMult,"Range1Slopes_shunt%.1f"%shuntMult,100,.94*.3/shuntMult,1.1*.3/shuntMult), TH1F("Range1Offsets_shunt%.1f"%shuntMult,"Range1Offsets_shunt%.1f"%shuntMult,100,-20,150),TH1F("Range1Uncertainties_shunt%.1f"%shuntMult,"Range1Uncertainties_shunt%.1f"%shuntMult, 50,1.*10**-8,10.*10**-6)],
                                2:[TH1F("Range2Slopes_shunt%.1f"%shuntMult,"Range2Slopes_shunt%.1f"%shuntMult,100,.94*.3/shuntMult,1.1*.3/shuntMult), TH1F("Range2Offsets_shunt%.1f"%shuntMult,"Range2Offsets_shunt%.1f"%shuntMult,100,-20,150), TH1F("Range2Uncertainties_shunt%.1f"%shuntMult,"Range2Uncertainties_shunt%.1f"%shuntMult, 50,1.*10**-8,10.*10**-6)],
                                3:[TH1F("Range3Slopes_shunt%.1f"%shuntMult,"Range3Slopes_shunt%.1f"%shuntMult,100,.94*.3/shuntMult,1.1*.3/shuntMult), TH1F("Range3Offsets_shunt%.1f"%shuntMult,"Range3Offsets_shunt%.1f"%shuntMult,100,-20,150), TH1F("Range3Uncertainties_shunt%.1f"%shuntMult,"Range3Uncertainties_shunt%.1f"%shuntMult, 50,1.*10**-8,10.*10**-6)],
                     }

        for entry in parameterValues:
            qieID, barcode, qieNum, i_capID, qieRange,shuntMult, Gsel, slope, offset, uncertainty= entry
            slopes_[shuntMult][i_capID][qieRange].append(float(slope))         
            hists[shuntMult][qieRange][0].Fill(slope)
            hists[shuntMult][qieRange][1].Fill(offset)
            hists[shuntMult][qieRange][2].Fill(uncertainty)
#        print slopes_[1][0][0]
        file_1 = open("%s/Method1_R0_C0_%s.txt"%(outputDirectory, uniqueID.replace(" ","_")), "w")
	for index in range(12):
    		file_1.write(str(slopes_[1][0][0][index]) + " " + str(slopes_[1.5][0][0][index]) +" " + str(slopes_[2][0][0][index]) + " " + str(slopes_[3][0][0][index]) +" " + str(slopes_[4][0][0][index]) + " " + str(slopes_[5][0][0][index]) +  " " + str(slopes_[6][0][0][index]) + " " + str(slopes_[7][0][0][index]) + " " + str(slopes_[8][0][0][index]) + " " + str(slopes_[9][0][0][index]) +" " + str(slopes_[10][0][0][index]) + " " + str(slopes_[11][0][0][index]) + " " + str(slopes_[11.5][0][0][index]) +"\n")
	file_1.close()        
        file_2 = open("%s/Method1_R0_C1_%s.txt"%(outputDirectory, uniqueID.replace(" ","_")), "w")
        for index in range(12):
                file_2.write(str(slopes_[1][1][0][index]) + " " + str(slopes_[1.5][1][0][index]) +" " + str(slopes_[2][1][0][index]) + " " + str(slopes_[3][1][0][index]) +" " + str(slopes_[4][1][0][index]) + " " + str(slopes_[5][1][0][index]) +  " " + str(slopes_[6][1][0][index]) + " " + str(slopes_[7][1][0][index]) + " " + str(slopes_[8][1][0][index]) + " " + str(slopes_[9][1][0][index]) +" " + str(slopes_[10][1][0][index]) + " " + str(slopes_[11][1][0][index]) + " " + str(slopes_[11.5][1][0][index]) +"\n")
        file_2.close()
        file_3 = open("%s/Method1_R0_C2_%s.txt"%(outputDirectory, uniqueID.replace(" ","_")), "w")
        for index in range(12):
                file_3.write(str(slopes_[1][2][0][index]) + " " + str(slopes_[1.5][2][0][index]) +" " + str(slopes_[2][2][0][index]) + " " + str(slopes_[3][2][0][index]) +" " + str(slopes_[4][2][0][index]) + " " + str(slopes_[5][2][0][index]) +  " " + str(slopes_[6][2][0][index]) + " " + str(slopes_[7][2][0][index]) + " " + str(slopes_[8][2][0][index]) + " " + str(slopes_[9][2][0][index]) +" " + str(slopes_[10][2][0][index]) + " " + str(slopes_[11][2][0][index]) + " " + str(slopes_[11.5][2][0][index]) +"\n")
        file_3.close()
        file_4 = open("%s/Method1_R0_C3_%s.txt"%(outputDirectory, uniqueID.replace(" ","_")), "w")
        for index in range(12):
                file_4.write(str(slopes_[1][3][0][index]) + " " + str(slopes_[1.5][3][0][index]) +" " + str(slopes_[2][3][0][index]) + " " + str(slopes_[3][3][0][index]) +" " + str(slopes_[4][3][0][index]) + " " + str(slopes_[5][3][0][index]) +  " " + str(slopes_[6][3][0][index]) + " " + str(slopes_[7][3][0][index]) + " " + str(slopes_[8][3][0][index]) + " " + str(slopes_[9][3][0][index]) +" " + str(slopes_[10][3][0][index]) + " " + str(slopes_[11][3][0][index]) + " " + str(slopes_[11.5][3][0][index]) +"\n")
        file_4.close()
	file_5 = open("%s/Method1_R1_C0_%s.txt"%(outputDirectory, uniqueID.replace(" ","_")), "w")
        for index in range(12):
                file_5.write(str(slopes_[1][0][1][index]) + " " + str(slopes_[1.5][0][1][index]) +" " + str(slopes_[2][0][1][index]) + " " + str(slopes_[3][0][1][index]) +" " + str(slopes_[4][0][1][index]) + " " + str(slopes_[5][0][1][index]) +  " " + str(slopes_[6][0][1][index]) + " " + str(slopes_[7][0][1][index]) + " " + str(slopes_[8][0][1][index]) + " " + str(slopes_[9][0][1][index]) +" " + str(slopes_[10][0][1][index]) + " " + str(slopes_[11][0][1][index]) + " " + str(slopes_[11.5][0][1][index]) +"\n")
        file_5.close()   
        file_6 = open("%s/Method1_R1_C1_%s.txt"%(outputDirectory, uniqueID.replace(" ","_")), "w")
        for index in range(12):
                file_6.write(str(slopes_[1][1][1][index]) + " " + str(slopes_[1.5][1][1][index]) +" " + str(slopes_[2][1][1][index]) + " " + str(slopes_[3][1][1][index]) +" " + str(slopes_[4][1][1][index]) + " " + str(slopes_[5][1][1][index]) +  " " + str(slopes_[6][1][1][index]) + " " + str(slopes_[7][1][1][index]) + " " + str(slopes_[8][1][1][index]) + " " + str(slopes_[9][1][1][index]) +" " + str(slopes_[10][1][1][index]) + " " + str(slopes_[11][1][1][index]) + " " + str(slopes_[11.5][1][1][index]) +"\n")
        file_6.close() 
        file_7 = open("%s/Method1_R1_C2_%s.txt"%(outputDirectory, uniqueID.replace(" ","_")), "w")
        for index in range(12):
                file_7.write(str(slopes_[1][2][1][index]) + " " + str(slopes_[1.5][2][1][index]) +" " + str(slopes_[2][2][1][index]) + " " + str(slopes_[3][2][1][index]) +" " + str(slopes_[4][2][1][index]) + " " + str(slopes_[5][2][1][index]) +  " " + str(slopes_[6][2][1][index]) + " " + str(slopes_[7][2][1][index]) + " " + str(slopes_[8][2][1][index]) + " " + str(slopes_[9][2][1][index]) +" " + str(slopes_[10][2][1][index]) + " " + str(slopes_[11][2][1][index]) + " " + str(slopes_[11.5][2][1][index]) +"\n")
        file_7.close() 

        file_8 = open("%s/Method1_R1_C3_%s.txt"%(outputDirectory, uniqueID.replace(" ","_")), "w")
        for index in range(12):
                file_8.write(str(slopes_[1][3][1][index]) + " " + str(slopes_[1.5][3][1][index]) +" " + str(slopes_[2][3][1][index]) + " " + str(slopes_[3][3][1][index]) +" " + str(slopes_[4][3][1][index]) + " " + str(slopes_[5][3][1][index]) +  " " + str(slopes_[6][3][1][index]) + " " + str(slopes_[7][3][1][index]) + " " + str(slopes_[8][3][1][index]) + " " + str(slopes_[9][3][1][index]) +" " + str(slopes_[10][3][1][index]) + " " + str(slopes_[11][3][1][index]) + " " + str(slopes_[11.5][3][1][index]) +"\n")
        file_8.close() 

        outputParamRootFile = TFile("%s/fitResults_%s.root"%(outputDirectory, uniqueID.replace(" ","_")),"update")

        outputParamRootFile.cd("SummaryPlots")

        for shuntMult in hists:
            for i_range in hists[shuntMult]:
                hists[shuntMult][i_range][0].Write()
                hists[shuntMult][i_range][1].Write()
                hists[shuntMult][i_range][2].Write()
                


if __name__=="__main__":

    import sys

    if len(sys.argv)==2:
        outFile = sys.argv[1]

#        graphParamDist(outFile)

#graphParamDist("/Users/titasroy/cmshcal11_github/sqlite_05_22/qieCalibrationParameters_0x83000000_0xeaaeaa70.db")
#graphParamDist("/Users/titasroy/cmshcal11_github/sqlite_05_22/qieCalibrationParameters_0xd0000000_0xeaa72770.db")
#graphParamDist("/Users/titasroy/cmshcal11_github/sqlite_05_22/qieCalibrationParameters_0x3e000000_0xeabfc070.db")
#graphParamDist("/Users/titasroy/cmshcal11_github/sqlite_05_22/qieCalibrationParameters_0xb9000000_0xeabcff70.db")
#graphParamDist("/Users/titasroy/cmshcal11_github/sqlite_05_22/qieCalibrationParameters_0xee000000_0xeaa7ef70.db")
#graphParamDist("/Users/titasroy/cmshcal11_github/sqlite_05_22/qieCalibrationParameters_0x1d000000_0xea9e6d70.db")
#graphParamDist("/Users/titasroy/cmshcal11_github/sqlite_05_22/qieCalibrationParameters_0x89000000_0xead3d470.db")

