from ROOT import *
import sqlite3
import math
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

    paramDB = sqlite3.connect(paramFileName)
    cursor = paramDB.cursor()
    qieCards = [x[0] for x in list(set(cursor.execute("select id from qieshuntparams").fetchall()))]
    print qieCards

    for uniqueID in qieCards:
        
        print uniqueID
        hists = {}
        hists_ratio={}
        slopes_base ={}
        hists_diff={}
        parameterValues = cursor.execute("select * from qieshuntparams where id = ?", [str(uniqueID)]).fetchall()
        for shuntMult in shuntMultList:

            range0MinMax = cursor.execute("select min(slope), max(slope), min(offset), max(offset) from qieshuntparams where id = ? and range=? and shunt=?", [str(uniqueID),0,shuntMult]).fetchone()
            range1MinMax = cursor.execute("select min(slope), max(slope), min(offset), max(offset) from qieshuntparams where id = ? and range=? and shunt=?", [str(uniqueID),1,shuntMult]).fetchone()
            range2MinMax = cursor.execute("select min(slope), max(slope), min(offset), max(offset) from qieshuntparams where id = ? and range=? and shunt=?", [str(uniqueID),2,shuntMult]).fetchone()
            range3MinMax = cursor.execute("select min(slope), max(slope), min(offset), max(offset) from qieshuntparams where id = ? and range=? and shunt=?", [str(uniqueID),3,shuntMult]).fetchone()

            if shuntMult>1: range3MinMax = [1,1,1,1]
            

            hists[shuntMult] = {0:[TH1F("Range0Slopes_shunt%.1f"%shuntMult,"Range0Slopes_shunt%.1f"%shuntMult,50,range0MinMax[0]*0.8,range0MinMax[1]*1.2), TH1F("Range0Offsets_shunt%.1f"%shuntMult,"Range0Offsets_shunt%.1f"%shuntMult,50,range0MinMax[2]*1.2, range0MinMax[3]*1.2)],
                                1:[TH1F("Range1Slopes_shunt%.1f"%shuntMult,"Range1Slopes_shunt%.1f"%shuntMult,50,range1MinMax[0]*0.8,range1MinMax[1]*1.2), TH1F("Range1Offsets_shunt%.1f"%shuntMult,"Range1Offsets_shunt%.1f"%shuntMult,50,range1MinMax[2]*1.2, range1MinMax[3]*1.2)],
                                2:[TH1F("Range2Slopes_shunt%.1f"%shuntMult,"Range2Slopes_shunt%.1f"%shuntMult,50,range2MinMax[0]*0.8,range2MinMax[1]*1.2), TH1F("Range2Offsets_shunt%.1f"%shuntMult,"Range2Offsets_shunt%.1f"%shuntMult,50,range2MinMax[2]*1.2, range2MinMax[3]*1.2)],
                                3:[TH1F("Range3Slopes_shunt%.1f"%shuntMult,"Range3Slopes_shunt%.1f"%shuntMult,50,range3MinMax[0]*0.8,range3MinMax[1]*1.2), TH1F("Range3Offsets_shunt%.1f"%shuntMult,"Range3Offsets_shunt%.1f"%shuntMult,50,range3MinMax[2]*1.2, range3MinMax[3]*1.2)],
                     }
            hists_ratio[shuntMult]={0:[TH1F("Range0Sloperatio_shunt%.1f"%shuntMult,"Range0Sloperatio_shunt%.1f"%shuntMult,100,0,12)],
                                   1:[TH1F("Range1Sloperatio_shunt%.1f"%shuntMult,"Range1Sloperatio_shunt%.1f"%shuntMult,100,0,12)],
                                   }
            hists_diff[shuntMult]=[TH1F("diffR0R1_shunt%.1f"%shuntMult,"diffR0R1_shunt%.1f"%shuntMult,50,0,.1)]
            slopes_base[shuntMult]={0:[],
                                    1:[],
                                    2:[],
                                    3:[],                              
        
                                    } 
 #       print hists_ratio[11.5][0]
        for entry in parameterValues:
            qieID, serial, qieNum, i_capID, qieRange,shuntMult, directory, timestamp, slope, offset = entry
                     
            hists[shuntMult][qieRange][0].Fill(slope)
            hists[shuntMult][qieRange][1].Fill(offset)
            slopes_base[shuntMult][qieRange].append(slope)
#    print  len(slopes_base[11.5][1])
 #   print len(slopes_base[1][1])
    #print slopes_base[1][0][0]/slopes_base[1.5][0][0]
    ratio_1halfR0=[]
    ratio_2R0=[]
    ratio_3R0= []
    ratio_4R0= []
    ratio_5R0= []
    ratio_6R0=[]
    ratio_7R0=[]
    ratio_8R0=[]
    ratio_9R0=[]
    ratio_10R0=[]
    ratio_11R0=[]
    
    ratio_11halfR0=[]
    ratio_1halfR1 =[]
    ratio_2R1 = []
    ratio_3R1 = []
    ratio_4R1= []
    ratio_5R1 =[]
    ratio_6R1= []
    ratio_7R1=[]
    ratio_8R1=[]
    
    
    ratio_9R1=[]
    ratio_10R1=[]
    ratio_11R1 =[]
    ratio_11halfR1=[]
    diff_1half=[]
    diff_2=[]
    diff_3=[]
    diff_4=[]
    diff_5=[]
    diff_6=[]
    diff_7=[]
    diff_8=[]
    diff_9=[]
    diff_10=[]
    diff_11=[]
    diff_11half=[]
            
    for i in range(48):
            print slopes_base[1][0][i]/slopes_base[1.5][0][i]
            ratio_1halfR0.append(float(slopes_base[1][0][i]/slopes_base[1.5][0][i]))
            ratio_2R0.append(float(slopes_base[1][0][i]/slopes_base[2][0][i]))
            ratio_3R0.append(float(slopes_base[1][0][i]/slopes_base[3][0][i]))
            ratio_4R0.append(float(slopes_base[1][0][i]/slopes_base[4][0][i]))
            ratio_5R0.append(float(slopes_base[1][0][i]/slopes_base[5][0][i]))
            ratio_6R0.append(float(slopes_base[1][0][i]/slopes_base[6][0][i]))
            ratio_7R0.append(float(slopes_base[1][0][i]/slopes_base[7][0][i]))
            ratio_8R0.append(float(slopes_base[1][0][i]/slopes_base[8][0][i]))
            ratio_9R0.append(float(slopes_base[1][0][i]/slopes_base[9][0][i]))
            ratio_10R0.append(float(slopes_base[1][0][i]/slopes_base[10][0][i]))
            ratio_11R0.append(float(slopes_base[1][0][i]/slopes_base[11][0][i]))
            ratio_11halfR0.append(float(slopes_base[1][0][i]/slopes_base[11.5][0][i]))
    for i in range(48):         
            ratio_1halfR1.append(float(slopes_base[1][1][i]/slopes_base[1.5][1][i]))
            ratio_2R1.append(float(slopes_base[1][1][i]/slopes_base[2][1][i]))
            ratio_3R1.append(float(slopes_base[1][1][i]/slopes_base[3][1][i]))
            ratio_4R1.append(float(slopes_base[1][1][i]/slopes_base[4][1][i]))
            ratio_5R1.append(float(slopes_base[1][1][i]/slopes_base[5][1][i]))
            ratio_6R1.append(float(slopes_base[1][1][i]/slopes_base[6][1][i]))
            ratio_7R1.append(float(slopes_base[1][1][i]/slopes_base[7][1][i]))
            ratio_8R1.append(float(slopes_base[1][1][i]/slopes_base[8][1][i]))
            ratio_9R1.append(float(slopes_base[1][1][i]/slopes_base[9][1][i]))
            ratio_10R1.append(float(slopes_base[1][1][i]/slopes_base[10][1][i]))
            ratio_11R1.append(float(slopes_base[1][1][i]/slopes_base[11][1][i]))          
            ratio_11halfR1.append(float(slopes_base[1][1][i]/slopes_base[11.5][1][i]))
    for i in range(48):
        diff_1half.append(float(ratio_1halfR0[i]-ratio_1halfR1[i]))
        diff_2.append(float(ratio_2R0[i]-ratio_2R1[i]))
        diff_3.append(float(ratio_3R0[i]-ratio_3R1[i]))
        diff_4.append(float(ratio_4R0[i]-ratio_4R1[i]))
        diff_5.append(float(ratio_5R0[i]-ratio_5R1[i]))
        diff_6.append(float(ratio_6R0[i]-ratio_6R1[i]))
        diff_7.append(float(ratio_7R0[i]-ratio_7R1[i]))
        diff_8.append(float(ratio_8R0[i]-ratio_8R1[i]))
        diff_9.append(float(ratio_9R0[i]-ratio_9R1[i]))
        diff_10.append(float(ratio_10R0[i]-ratio_10R1[i]))
        diff_11.append(float(ratio_11R0[i]-ratio_11R1[i]))
        diff_11half.append(float(ratio_11halfR0[i]-ratio_11halfR1[i]))
  #  print len(ratio_1halfR0)
    for i in range(48):   
            hists_ratio[1.5][0][0].Fill(ratio_1halfR0[i])
            hists_ratio[2][0][0].Fill(ratio_2R0[i])
            hists_ratio[3][0][0].Fill(ratio_3R0[i])
            hists_ratio[4][0][0].Fill(ratio_4R0[i])
            hists_ratio[5][0][0].Fill(ratio_5R0[i])
            hists_ratio[6][0][0].Fill(ratio_6R0[i])
            hists_ratio[7][0][0].Fill(ratio_7R0[i])
            hists_ratio[8][0][0].Fill(ratio_8R0[i])
            hists_ratio[9][0][0].Fill(ratio_9R0[i])
            hists_ratio[10][0][0].Fill(ratio_10R0[i])
            hists_ratio[11][0][0].Fill(ratio_11R0[i])
            hists_ratio[11.5][0][0].Fill(ratio_11halfR0[i])
    for i in range(len(ratio_1halfR1)):
            hists_ratio[1.5][1][0].Fill(ratio_1halfR1[i])
            hists_ratio[2][1][0].Fill(ratio_2R1[i])
            hists_ratio[3][1][0].Fill(ratio_3R1[i])
            hists_ratio[4][1][0].Fill(ratio_4R1[i])
            hists_ratio[5][1][0].Fill(ratio_5R1[i])
            hists_ratio[6][1][0].Fill(ratio_6R1[i])
            hists_ratio[7][1][0].Fill(ratio_7R1[i])
            hists_ratio[8][1][0].Fill(ratio_8R1[i])
            hists_ratio[9][1][0].Fill(ratio_9R1[i])
            hists_ratio[10][1][0].Fill(ratio_10R1[i])
            hists_ratio[11][1][0].Fill(ratio_11R1[i])
            hists_ratio[11.5][1][0].Fill(ratio_11halfR1[i])
            hists_diff[1.5][0].Fill(diff_1half[i])
            hists_diff[2][0].Fill(diff_2[i])
            hists_diff[3][0].Fill(diff_3[i])
            hists_diff[4][0].Fill(diff_4[i])
            hists_diff[5][0].Fill(diff_5[i])
            hists_diff[6][0].Fill(diff_6[i])
            hists_diff[7][0].Fill(diff_7[i])
            hists_diff[8][0].Fill(diff_8[i])
            hists_diff[9][0].Fill(diff_9[i])
            hists_diff[10][0].Fill(diff_10[i])
            hists_diff[11][0].Fill(diff_11[i])
            hists_diff[11.5][0].Fill(diff_11half[i])

        
    outputParamRootFile = TFile("%s/fitResults_%s.root"%(outputDirectory, uniqueID.replace(" ","_")),"update")

    outputParamRootFile.cd("SummaryPlots")

    for shuntMult in hists:
        hists_diff[shuntMult][0].Write()
        for i_range in hists[shuntMult]:
            hists[shuntMult][i_range][0].Write()
            hists[shuntMult][i_range][1].Write()
            
        for i_range in hists_ratio[shuntMult]:
            hists_ratio[shuntMult][i_range][0].Write()
         


graphParamDist("/home/hep/jmmans/chargy/hcal/hcalUHTR/Data_CalibrationScans/2016-08-08/Run_01/qieCalibrationParameters_0xce000000_0xead01d70.db")

if __name__=="__main__":
    import sys

    if len(sys.argv)==2:
        outFile = sys.argv[1]

        graphParamDist(outFile)

