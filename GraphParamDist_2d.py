from ROOT import *
import sqlite3

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
        parameterValues = cursor.execute("select * from qieshuntparams where id = ?", [str(uniqueID)]).fetchall()
        for shuntMult in shuntMultList:

            range0MinMax = cursor.execute("select min(slope), max(slope), min(offset), max(offset), min(uncertainty), max(uncertainty) from qieshuntparams where id = ? and range=? and shunt=?", [str(uniqueID),0,shuntMult]).fetchone()
            range1MinMax = cursor.execute("select min(slope), max(slope), min(offset), max(offset), min(uncertainty), max(uncertainty) from qieshuntparams where id = ? and range=? and shunt=?", [str(uniqueID),1,shuntMult]).fetchone()
            range2MinMax = cursor.execute("select min(slope), max(slope), min(offset), max(offset), min(uncertainty), max(uncertainty) from qieshuntparams where id = ? and range=? and shunt=?", [str(uniqueID),2,shuntMult]).fetchone()
            range3MinMax = cursor.execute("select min(slope), max(slope), min(offset), max(offset), min(uncertainty), max(uncertainty) from qieshuntparams where id = ? and range=? and shunt=?", [str(uniqueID),3,shuntMult]).fetchone()

            if shuntMult>1: 
                range3MinMax= [1,1,1,1] 
                range2MinMax= [1,1,1,1] 
                #range1MinMax= [1,1,1,1]
            

            hists[shuntMult] = {0:[TH1F("Range0Slopes_shunt%.1f"%shuntMult,"Range0Slopes_shunt%.1f"%shuntMult,50,range0MinMax[0]*0.8,range0MinMax[1]*1.2), TH1F("Range0Offsets_shunt%.1f"%shuntMult,"Range0Offsets_shunt%.1f"%shuntMult,50,range0MinMax[2]*1.2, range0MinMax[3]*1.2), TH1F("Range0Uncertainties_shunt%.1f"%shuntMult,"Range0Uncertainties_shunt%.1f"%shuntMult, 50,1.*10**-8,10.*10**-6)],
                                1:[TH1F("Range1Slopes_shunt%.1f"%shuntMult,"Range1Slopes_shunt%.1f"%shuntMult,50,range1MinMax[0]*0.8,range1MinMax[1]*1.2), TH1F("Range1Offsets_shunt%.1f"%shuntMult,"Range1Offsets_shunt%.1f"%shuntMult,50,range1MinMax[2]*1.2, range1MinMax[3]*1.2),TH1F("Range1Uncertainties_shunt%.1f"%shuntMult,"Range1Uncertainties_shunt%.1f"%shuntMult, 50,1.*10**-8,10.*10**-6)],
                                2:[TH1F("Range2Slopes_shunt%.1f"%shuntMult,"Range2Slopes_shunt%.1f"%shuntMult,50,range2MinMax[0]*0.8,range2MinMax[1]*1.2), TH1F("Range2Offsets_shunt%.1f"%shuntMult,"Range2Offsets_shunt%.1f"%shuntMult,50,range2MinMax[2]*1.2, range2MinMax[3]*1.2), TH1F("Range2Uncertainties_shunt%.1f"%shuntMult,"Range2Uncertainties_shunt%.1f"%shuntMult, 50,1.*10**-8,10.*10**-6)],
                                3:[TH1F("Range3Slopes_shunt%.1f"%shuntMult,"Range3Slopes_shunt%.1f"%shuntMult,50,range3MinMax[0]*0.8,range3MinMax[1]*1.2), TH1F("Range3Offsets_shunt%.1f"%shuntMult,"Range3Offsets_shunt%.1f"%shuntMult,50,range3MinMax[2]*1.2, range3MinMax[3]*1.2), TH1F("Range3Uncertainties_shunt%.1f"%shuntMult,"Range3Uncertainties_shunt%.1f"%shuntMult, 50,1.*10**-8,10.*10**-6)],
                     }
            # if shuntMult == 1:
            #     hists_1 = {0:[TH1F("Range0Slopes","Range0Slopes",50,range0MinMax[0]*0.8,range0MinMax[1]*1.2), TH1F("Range0Offsets","Range0Offsets",50,range0MinMax[2]*1.2, range0MinMax[3]*1.2)],
            #      1:[TH1F("Range1Slopes","Range1Slopes",50,range1MinMax[0]*0.8,range1MinMax[1]*1.2), TH1F("Range1Offsets","Range1Offsets",50,range1MinMax[2]*1.2, range1MinMax[3]*1.2)],
            #      2:[TH1F("Range2Slopes","Range2Slopes",50,range2MinMax[0]*0.8,range2MinMax[1]*1.2), TH1F("Range2Offsets","Range2Offsets",50,range2MinMax[2]*1.2, range2MinMax[3]*1.2)],
            #      3:[TH1F("Range3Slopes","Range3Slopes",50,range3MinMax[0]*0.8,range3MinMax[1]*1.2), TH1F("Range3Offsets","Range3Offsets",50,range3MinMax[2]*1.2, range3MinMax[3]*1.2)],
            #      }
            # elif shuntMult == 1.5:
            #     hists_1half = {0:[TH1F("Range0Slopes","Range0Slopes",50,range0MinMax[0]*0.8,range0MinMax[1]*1.2), TH1F("Range0Offsets","Range0Offsets",50,range0MinMax[2]*1.2, range0MinMax[3]*1.2)],
            #                    1:[TH1F("Range1Slopes","Range1Slopes",50,range1MinMax[0]*0.8,range1MinMax[1]*1.2), TH1F("Range1Offsets","Range1Offsets",50,range1MinMax[2]*1.2, range1MinMax[3]*1.2)],
            #                    2:[TH1F("Range2Slopes","Range2Slopes",50,range2MinMax[0]*0.8,range2MinMax[1]*1.2), TH1F("Range2Offsets","Range2Offsets",50,range2MinMax[2]*1.2, range2MinMax[3]*1.2)],
            #      }
            # elif shuntMult == 2:
            #      hists_2 = {0:[TH1F("Range0Slopes","Range0Slopes",50,range0MinMax[0]*0.8,range0MinMax[1]*1.2), TH1F("Range0Offsets","Range0Offsets",50,range0MinMax[2]*1.2, range0MinMax[3]*1.2)],
            #                     1:[TH1F("Range1Slopes","Range1Slopes",50,range1MinMax[0]*0.8,range1MinMax[1]*1.2), TH1F("Range1Offsets","Range1Offsets",50,range1MinMax[2]*1.2, range1MinMax[3]*1.2)],
            #                     2:[TH1F("Range2Slopes","Range2Slopes",50,range2MinMax[0]*0.8,range2MinMax[1]*1.2), TH1F("Range2Offsets","Range2Offsets",50,range2MinMax[2]*1.2, range2MinMax[3]*1.2)],
            #     }
            # elif shuntMult == 3 :
            #     hists_3 = {0:[TH1F("Range0Slopes","Range0Slopes",50,range0MinMax[0]*0.8,range0MinMax[1]*1.2), TH1F("Range0Offsets","Range0Offsets",50,range0MinMax[2]*1.2, range0MinMax[3]*1.2)],
            #                1:[TH1F("Range1Slopes","Range1Slopes",50,range1MinMax[0]*0.8,range1MinMax[1]*1.2), TH1F("Range1Offsets","Range1Offsets",50,range1MinMax[2]*1.2, range1MinMax[3]*1.2)],
            #                2:[TH1F("Range2Slopes","Range2Slopes",50,range2MinMax[0]*0.8,range2MinMax[1]*1.2), TH1F("Range2Offsets","Range2Offsets",50,range2MinMax[2]*1.2, range2MinMax[3]*1.2)],
            #     }          
            # elif shuntMult == 4:
            #     hists_4 = {0:[TH1F("Range0Slopes","Range0Slopes",50,range0MinMax[0]*0.8,range0MinMax[1]*1.2), TH1F("Range0Offsets","Range0Offsets",50,range0MinMax[2]*1.2, range0MinMax[3]*1.2)],
            #                1:[TH1F("Range1Slopes","Range1Slopes",50,range1MinMax[0]*0.8,range1MinMax[1]*1.2), TH1F("Range1Offsets","Range1Offsets",50,range1MinMax[2]*1.2, range1MinMax[3]*1.2)],
            #                2:[TH1F("Range2Slopes","Range2Slopes",50,range2MinMax[0]*0.8,range2MinMax[1]*1.2), TH1F("Range2Offsets","Range2Offsets",50,range2MinMax[2]*1.2, range2MinMax[3]*1.2)],
            #    }
            # elif shuntMult == 5:

            #      hists_5 = {0:[TH1F("Range0Slopes","Range0Slopes",50,range0MinMax[0]*0.8,range0MinMax[1]*1.2), TH1F("Range0Offsets","Range0Offsets",50,range0MinMax[2]*1.2, range0MinMax[3]*1.2)],
            #                 1:[TH1F("Range1Slopes","Range1Slopes",50,range1MinMax[0]*0.8,range1MinMax[1]*1.2), TH1F("Range1Offsets","Range1Offsets",50,range1MinMax[2]*1.2, range1MinMax[3]*1.2)],
            #                 2:[TH1F("Range2Slopes","Range2Slopes",50,range2MinMax[0]*0.8,range2MinMax[1]*1.2), TH1F("Range2Offsets","Range2Offsets",50,range2MinMax[2]*1.2, range2MinMax[3]*1.2)],
            #                 }
            # elif shuntMult == 6:
            #      hists_6 = {0:[TH1F("Range0Slopes","Range0Slopes",50,range0MinMax[0]*0.8,range0MinMax[1]*1.2), TH1F("Range0Offsets","Range0Offsets",50,range0MinMax[2]*1.2, range0MinMax[3]*1.2)],
            #                 1:[TH1F("Range1Slopes","Range1Slopes",50,range1MinMax[0]*0.8,range1MinMax[1]*1.2), TH1F("Range1Offsets","Range1Offsets",50,range1MinMax[2]*1.2, range1MinMax[3]*1.2)],
            #                 2:[TH1F("Range2Slopes","Range2Slopes",50,range2MinMax[0]*0.8,range2MinMax[1]*1.2), TH1F("Range2Offsets","Range2Offsets",50,range2MinMax[2]*1.2, range2MinMax[3]*1.2)],
            #             }
            # elif shuntMult == 7:
            #      hists_7 =  {0:[TH1F("Range0Slopes","Range0Slopes",50,range0MinMax[0]*0.8,range0MinMax[1]*1.2), TH1F("Range0Offsets","Range0Offsets",50,range0MinMax[2]*1.2, range0MinMax[3]*1.2)],
            #                 1:[TH1F("Range1Slopes","Range1Slopes",50,range1MinMax[0]*0.8,range1MinMax[1]*1.2), TH1F("Range1Offsets","Range1Offsets",50,range1MinMax[2]*1.2, range1MinMax[3]*1.2)],
            #                 2:[TH1F("Range2Slopes","Range2Slopes",50,range2MinMax[0]*0.8,range2MinMax[1]*1.2), TH1F("Range2Offsets","Range2Offsets",50,range2MinMax[2]*1.2, range2MinMax[3]*1.2)],
            #                     }
            # elif shuntMult ==8:
            #     hists_8 =  {0:[TH1F("Range0Slopes","Range0Slopes",50,range0MinMax[0]*0.8,range0MinMax[1]*1.2), TH1F("Range0Offsets","Range0Offsets",50,range0MinMax[2]*1.2, range0MinMax[3]*1.2)],
            #                 1:[TH1F("Range1Slopes","Range1Slopes",50,range1MinMax[0]*0.8,range1MinMax[1]*1.2), TH1F("Range1Offsets","Range1Offsets",50,range1MinMax[2]*1.2, range1MinMax[3]*1.2)],
            #                 2:[TH1F("Range2Slopes","Range2Slopes",50,range2MinMax[0]*0.8,range2MinMax[1]*1.2), TH1F("Range2Offsets","Range2Offsets",50,range2MinMax[2]*1.2, range2MinMax[3]*1.2)],
            #                 }
            # elif shuntMult == 9:
            #     hists_9 = {0:[TH1F("Range0Slopes","Range0Slopes",50,range0MinMax[0]*0.8,range0MinMax[1]*1.2), TH1F("Range0Offsets","Range0Offsets",50,range0MinMax[2]*1.2, range0MinMax[3]*1.2)],
            #                1:[TH1F("Range1Slopes","Range1Slopes",50,range1MinMax[0]*0.8,range1MinMax[1]*1.2), TH1F("Range1Offsets","Range1Offsets",50,range1MinMax[2]*1.2, range1MinMax[3]*1.2)],
            #                2:[TH1F("Range2Slopes","Range2Slopes",50,range2MinMax[0]*0.8,range2MinMax[1]*1.2), TH1F("Range2Offsets","Range2Offsets",50,range2MinMax[2]*1.2, range2MinMax[3]*1.2)],
            #                }
            # elif shuntMult == 10:
            #     hists_10 = {0:[TH1F("Range0Slopes","Range0Slopes",50,range0MinMax[0]*0.8,range0MinMax[1]*1.2), TH1F("Range0Offsets","Range0Offsets",50,range0MinMax[2]*1.2, range0MinMax[3]*1.2)],
            #                 1:[TH1F("Range1Slopes","Range1Slopes",50,range1MinMax[0]*0.8,range1MinMax[1]*1.2), TH1F("Range1Offsets","Range1Offsets",50,range1MinMax[2]*1.2, range1MinMax[3]*1.2)],
            #                 2:[TH1F("Range2Slopes","Range2Slopes",50,range2MinMax[0]*0.8,range2MinMax[1]*1.2), TH1F("Range2Offsets","Range2Offsets",50,range2MinMax[2]*1.2, range2MinMax[3]*1.2)],
            #                 }
            # elif shuntMult == 11:
            #     hists_11 = {0:[TH1F("Range0Slopes","Range0Slopes",50,range0MinMax[0]*0.8,range0MinMax[1]*1.2), TH1F("Range0Offsets","Range0Offsets",50,range0MinMax[2]*1.2, range0MinMax[3]*1.2)],
            #                 1:[TH1F("Range1Slopes","Range1Slopes",50,range1MinMax[0]*0.8,range1MinMax[1]*1.2), TH1F("Range1Offsets","Range1Offsets",50,range1MinMax[2]*1.2, range1MinMax[3]*1.2)],
            #                 2:[TH1F("Range2Slopes","Range2Slopes",50,range2MinMax[0]*0.8,range2MinMax[1]*1.2), TH1F("Range2Offsets","Range2Offsets",50,range2MinMax[2]*1.2, range2MinMax[3]*1.2)],
            #                 }
            # elif shuntMult == 11.5:
            #     hists_11half = {0:[TH1F("Range0Slopes","Range0Slopes",50,range0MinMax[0]*0.8,range0MinMax[1]*1.2), TH1F("Range0Offsets","Range0Offsets",50,range0MinMax[2]*1.2, range0MinMax[3]*1.2)],
            #                     1:[TH1F("Range1Slopes","Range1Slopes",50,range1MinMax[0]*0.8,range1MinMax[1]*1.2), TH1F("Range1Offsets","Range1Offsets",50,range1MinMax[2]*1.2, range1MinMax[3]*1.2)],
            #                     2:[TH1F("Range2Slopes","Range2Slopes",50,range2MinMax[0]*0.8,range2MinMax[1]*1.2), TH1F("Range2Offsets","Range2Offsets",50,range2MinMax[2]*1.2, range2MinMax[3]*1.2)],
            #                     }

        for entry in parameterValues:
            qieID, serial, qieNum, i_capID, qieRange,shuntMult, directory, timestamp, slope, offset, uncertainty = entry
                     
            hists[shuntMult][qieRange][0].Fill(slope)
            hists[shuntMult][qieRange][1].Fill(offset)
            hists[shuntMult][qieRange][2].Fill(uncertainty)
                

        outputParamRootFile = TFile("%s/fitResults_%s.root"%(outputDirectory, uniqueID.replace(" ","_")),"update")

        outputParamRootFile.cd("SummaryPlots")

        for shuntMult in hists:
            for i_range in hists[shuntMult]:
                hists[shuntMult][i_range][0].Write()
                hists[shuntMult][i_range][1].Write()
                hists[shuntMult][i_range][2].Write()
                
# # print hists                                                                                                                       
#             for i_range in hists:
#                 hists[shuntMult][i_range][0].Write()
#                 hists[shuntMult][i_range][1].Write()

#                 outputParamRootFile.Close()
#                 c1 = TCanvas()
#                 c1.cd()
#                 c1.Divide(2,2)

#                 c1.cd(1)
#                 hists[1][0][0].Draw()
#                 hists[shuntMult][0][0].Draw()
#                 c1.cd(2)
#                 hists[1][1][0].Draw()
#                 hists[shuntMult][1][0].Draw()
#                 c1.cd(3)
#                 hists[1][2][0].Draw()
#                 hists[shuntMult][2][0].Draw()
#                 c1.cd(4)
#                 hists[1][3][0].Draw()
#                 hists[shuntMult][3][0].Draw()
#                 c1.SaveAs(outputDirectory+"Slopes_%s.pdf"%str(uniqueID).replace(" ","_"))

#                 c1.cd(1)
#                 hists[1][0][1].Draw()
#                 hists[shuntMult][0][1].Draw()
#                 c1.cd(2)
#                 hists[1][1][1].Draw()
#                 hists[shuntMult][1][1].Draw()
#                 c1.cd(3)
#                 hists[1][2][1].Draw()
#                 hists[shuntMult][2][1].Draw()
#                 c1.cd(4)
#                 hists[1][3][1].Draw()
#                 hists[shuntMult][3][1].Draw()
#                 c1.SaveAs(outputDirectory+"Offsets_%s.pdf"%str(uniqueID).replace(" ","_"))


if __name__=="__main__":

    import sys

    if len(sys.argv)==2:
        outFile = sys.argv[1]

        graphParamDist(outFile)

#graphParamDist("/home/hep/jmmans/chargy/hcal/hcalUHTR/Data_CalibrationScans/2016-08-03/Run_12/qieCalibrationParameters_0x38000000_0xea99a870.db")
