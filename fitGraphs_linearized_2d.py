from ROOT import *
import sys
import numpy
from array import array
import os

from linearADC import *

####Change the fit to return slopes/offsets in terms of range 0 values for all ranges

#gROOT.SetBatch(kTRUE)
#ROOT.gStyle.SetCanvasColor(kWhite)
#gStyle.SetStatStyle(kWhite)
#gStyle.SetTitleStyle(kWhite)

graphOffset = [100,500,3000,8000]

startVal = [[3.2,-15],
            [3.2,-20],
            [3.2,-20],
            [3.2,-20]]


Varlimits = [[[2.5,4.0],[-50,100]],
             [[2.5,4.0],[-50,1000]],
             [[2.5,4.0],[-500,1000]],
             [[2.5,4.0],[-5000,10000]]]



lineColors = [kRed, kBlue, kGreen+2, kCyan] 
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


def doFit_combined(graphList, saveGraph = False, qieNumber = 0, qieUniqueID = "", useCalibrationMode = True, outputDir = '', shuntMult = 1, pedestalVals = {"low":[0,0,0,0],"high":[0,0,0,0],"shunt":{}}):

        fitLines =  []
        slopes =  []
        offsets =  []
        
#        pedestal = [0]*4
        linearizedGraphList =  []

        #print graphList

        outputTGraphs = TFile(outputDir.replace("outputPlots","")+"fitResults_%s.root"%qieUniqueID,"update")

        saveName = None


        if shuntMult == 1: 
                ranges = range(4)
        else :
                ranges = range(2)
        for i_range in ranges:

	#choose the pedestal to subtract according to the whether it is low current or high current
		if i_range == 0 and shuntMult==1:
			pedestal = pedestalVals["low"]
		elif  shuntMult==1:
			pedestal = pedestalVals["high"]
		else:
			pedestal = pedestalVals["shunts"][shuntMult]


                vOffset = i_range*64
                graphs = graphList[i_range]
                if graphs==None: 
                        fitLines.append(None)
                        continue
                else:                   
                        fitLines.append([])


# 		if pedestal==None:
# 			pedestal = []

                for i_capID in range(4):
                        #print i_graph
                        nominalgraph =  graphs[i_capID]
			print nominalgraph.GetName()
                        if shuntMult == 1:
                                outputTGraphs.cd("adcVsCharge")
                        else:
                                outputTGraphs.cd("Shunted_adcVsCharge")
                        nominalgraph.Write()
                        graph = nominalgraph.Clone("%s_linearized"%nominalgraph.GetName())
                        graph.SetNameTitle("%s_linearized"%nominalgraph.GetName(),"%s_linearized"%nominalgraph.GetName())

                        points = range(graph.GetN())
                        points.reverse()
                        maxCharge = -9e9
                        minCharge = 9e9
                        for p in points:
                                x = graph.GetX()[p]-vOffset
                                nominalgraph.GetX()[p] -= pedestal[i_capID]
                                graph.GetX()[p] -= pedestal[i_capID]


                        graph.GetXaxis().SetTitle("Charge (fC)")
			if i_range==0 and shuntMult==1:
				graph.GetXaxis().SetLimits(200,600)
			if i_range==1 and shuntMult==1:
				graph.GetXaxis().SetLimits(500,5000)
                        graph.GetYaxis().SetTitle("Linearized ADC")

                        if shuntMult == 1: 
                                outputTGraphs.cd("LinadcVsCharge")
                        else:
                                outputTGraphs.cd("Shunted_LinadcVsCharge")
                        

#			print pedestal

                        if graph.GetN() > 1:
				print graph.GetN()
				f1= TF1("f1","pol1",200,600);
				f2= TF1("f2","pol1",500,5000);
 				if (i_range==0 and shuntMult==1):
 					graph.Fit("f1","R") 
				if (i_range==1 and shuntMult==1):
					graph.Fit("f2","R") 
 				else:
 					graph.Fit("f1","0") 
								
                                linearizedGraphList.append(graph) 
				if (i_range==1 and shuntMult==1):
					fitLine = graph.GetFunction("f2")
				else:                               
                        	        fitLine = graph.GetFunction("f1")

                                fitLine.SetNameTitle("fit_%s"%graph.GetName(),"fit_%s"%graph.GetName())
                                fitLines[-1].append(fitLine)
                        else:
                                linearizedGraphList.append(graph)
                                fitLine = TF1("fit_%s"%graph.GetName(),"pol1",-999,999)
                                fitLine.SetParameter(0,0)
                                fitLine.SetParameter(1,0)
                                fitLine.SetParError(0,999)
                                fitLine.SetParError(1,999)
                                fitLine.SetNameTitle("fit_%s"%graph.GetName(),"fit_%s"%graph.GetName())
                                fitLines[-1].append(fitLine)
                                print 'PROBLEM'
                                print graph.GetName()
                                continue
                        graph.Write()
                                
                        if saveGraph:
                                qieInfo = ""

                                saveName = outputDir
                                if saveName[-1]!='/':
                                        saveName += '/'
                                saveName += "plots/"
                                if qieUniqueID != "": 
                                        qieInfo += ", Card ID "+qieUniqueID
                                else:
                                        qieUniqueID = "UnknownID"
                                saveName += qieUniqueID
                                if not os.path.exists(saveName):
                                        os.system("mkdir -p %s"%saveName)
                                saveName += "/LinADCvsfC"
                                if qieNumber != 0: 
                                        qieInfo += ", QIE " + str(qieNumber)
                                        saveName += "_qie"+str(qieNumber)
                                qieInfo += ", CapID " + str(i_capID)
                                saveName += "_range"+str(i_range)
                                saveName += "_capID"+str(i_capID)
                                saveName += "_shunt_"+str(shuntMult)
                                if not useCalibrationMode: saveName += "_NotCalMode"
                                saveName += ".pdf"
                                graph.SetTitle("LinADC vs Charge, Range %i%s" % (i_range,qieInfo))
                                graph.GetYaxis().SetTitle("Lin ADC")
                                graph.GetYaxis().SetTitleOffset(1.2)
                                graph.GetXaxis().SetTitle("Charge fC")
				if i_range==0 and shuntMult==1:
					graph.GetXaxis().SetRangeUser(200,600)
				if i_range==1 and shuntMult==1:
					graph.GetXaxis().SetRangeUser(500,5000)
                                xVals = graph.GetX()
                                exVals = graph.GetEX()
                                yVals = graph.GetY()
                                eyVals = graph.GetEY()
                                residuals = []
                                residualErrors = []
#                               residualsY = []
#                               residualErrorsY = []
                                eUp = []
                                eDown = []
                                N = graph.GetN()
                                x = []
                                y = []

                                for i in range(N):
                                        #    if yVals[i] != 0:
                                        residuals.append((yVals[i]-fitLine.Eval(xVals[i]))/max(yVals[i],0.001))
				#	residuals.append((yVals[p]-fitLine.Eval(xVals[p])))
                                        xLow = (xVals[i]-exVals[i])
                                        xHigh = (xVals[i]+exVals[i])
                                        #eUp.append((yVals[i]-fitLine(xLow))/max(yVals[i],0.001))
                                        #eDown.append((yVals[i]-fitLine(xLow))/max(yVals[i],0.001))
                                        residualErrors.append(eyVals[i]/max(yVals[i],0.001))
				#	residualErrors.append(eyVals[p])
                                        x.append(xVals[i])


                                resArray = array('d',residuals)
                                resErrArray = array('d',residualErrors)
                                resErrUpArray = array('d',eUp)
                                resErrDownArray = array('d',eDown)
                                xArray = array('d',x)
                                xErrorsArray = array('d',[0]*len(x))

                                print  "the residuals are:",resArray

                                residualGraphX = TGraphErrors(len(x),xArray,resArray, xErrorsArray, resErrArray)

                                residualGraphX.SetTitle("")
                                c1 = TCanvas()
                                p1 = TPad("","",0,0.2,0.9,1)
                                p2 = TPad("","",0,0,0.9,0.2)
                                p1.Draw()
                                p2.Draw()
                                p1.SetFillColor(kWhite)
                                p2.SetFillColor(kWhite)
#                               p3.SetFillColor(kWhite)
                                p1.cd()
                                p1.SetBottomMargin(0)
                                p1.SetRightMargin(0)
			#	p2.SetTopMargin(0)
			#	p2.SetBottomMargin(0.3)
                                graph.Draw("ap")
                                fitLine.SetLineColor(kRed)
                                fitLine.SetLineWidth(2)
                                fitLine.Draw("same")

                                xmin = graph.GetXaxis().GetXmin()
                                xmax = graph.GetXaxis().GetXmax()
                                ymin = graph.GetYaxis().GetXmin()
                                ymax = graph.GetYaxis().GetXmax()
				if (i_range==0 and shuntMult==1):
					text = TPaveText(200 + (600-200)*.2, 200 - (200-50)*(.3),200 + (600-200)*.6,200-(200-50)*.1)
				if  (i_range==1 and shuntMult==1):
					text = TPaveText(500 + (5000-500)*.2, 1800 - (1800-50)*(.3),500 + (5000-500)*.6,1800-(1800-50)*.1)
				else:
                        	        text = TPaveText(xmin + (xmax-xmin)*.2, ymax - (ymax-ymin)*(.3),xmin + (xmax-xmin)*.6,ymax-(ymax-ymin)*.1)
                                text.SetFillColor(kWhite)
				text.SetTextSize(0.75*text.GetTextSize())
                                text.SetFillStyle(8000)
                                text.AddText("Slope =  %.4f +- %.4f ADC/fC" % (fitLine.GetParameter(1), fitLine.GetParError(1)))
                                text.AddText("Offset =  %.2f +- %.2f ADC" % (fitLine.GetParameter(0), fitLine.GetParError(0)))
                                text.Draw("same")


                                p2.cd()
                                p2.SetTopMargin(0)
                                p2.SetRightMargin(0)
                                p2.SetBottomMargin(0.35)
                                residualGraphX.Draw("ap")
                                zeroLine = TF1("zero","0",-9e9,9e9)
                                zeroLine.SetLineColor(kBlack)
                                zeroLine.SetLineWidth(1)
                                zeroLine.Draw("same")

                                # xmin = xmin-10
                                # xmax = xmax+10
                                if minCharge < 10: minCharge = -10
                        # graph.GetXaxis().SetLimits(xmin-10,xmax+10)
                                #graph.GetXaxis().SetLimits(minCharge*0.9, maxCharge*1.1)
				graph.GetXaxis().SetLimits(xmin*0.9, xmax*1.1)
                                graph.GetYaxis().SetLimits(ymin*.9,ymax*1.1)
				if (i_range==0 and shuntMult==1):
					 residualGraphX.GetXaxis().SetLimits(200, 600)
				if (i_range==1 and shuntMult==1):
					 residualGraphX.GetXaxis().SetLimits(500, 5000)
				else:
                                	 residualGraphX.GetXaxis().SetLimits(xmin*0.9, xmax*1.1)
                                residualGraphX.GetYaxis().SetRangeUser(-0.1,0.1)
                                residualGraphX.SetMarkerStyle(7)
                                residualGraphX.GetYaxis().SetNdivisions(3,5,0)

                                residualGraphX.GetXaxis().SetLabelSize(0.15)
                                residualGraphX.GetYaxis().SetLabelSize(0.15)
                                residualGraphX.GetYaxis().SetTitle("Residuals")
                                residualGraphX.GetXaxis().SetTitle("Charge (fC)")
                                residualGraphX.GetXaxis().SetTitleSize(0.15)
                                residualGraphX.GetYaxis().SetTitleSize(0.15)
                                residualGraphX.GetYaxis().SetTitleOffset(0.33)

                                p1.cd()

                                c1.SaveAs(saveName)

        if shuntMult == 1:
                ranges = range(4)
                
                params = [[],[],[],[]]
        else:
                ranges = range(2)
                params = [[],[],[]]

        for irange in ranges:
                if fitLines[irange]==None:
                        for icapID in range(4):
                                params[irange].append([-1,-1])
                        continue
                for icapID in range(4):
                        offset = fitLines[irange][icapID].GetParameter(0)
                        slope = fitLines[irange][icapID].GetParameter(1)
                        uncertainty = fitLines[irange][icapID].GetParError(1)
                        params[irange].append([slope,offset,uncertainty])



        # outputTGraphs.cd("LinadcVsCharge")
        # for graph in linearizedGraphList:
        #       graph.Write()

        if shuntMult==1:
                outputTGraphs.cd("fitLines")
                ranges = range(4)
        else:
                outputTGraphs.cd("Shunted_fitLines")
                ranges = range(3)
        for i_range in ranges:
                if graphList[i_range]==None: continue
#                print 'Writing'
                for fitLine in fitLines[i_range]:
                        fitLine.SetNpx(1000)
                        fitLine.Write()

                if saveGraph:
                        if saveName==None: continue
                        saveName = saveName.replace("_capID"+str(i_capID),"")
                        c1 = TCanvas()
                        slopes = []
                        offsets = []
                        for i_capID in range(4):
                                graph = graphList[i_range][i_capID]
                                fitLine = fitLines[i_range][i_capID]
                                #            graph.SetMarkerStyle(20+i_capID)
                                fitLine.SetLineColor(lineColors[i_capID])
                                fitLine.SetLineWidth(2)

                                slopes.append( (fitLine.GetParameter(0), fitLine.GetParError(0) ) )
                                offsets.append( (fitLine.GetParameter(1), fitLine.GetParError(1) ) )
                                if i_capID==0:
                                        graph.Draw("ap")
                                        if shuntMult == -1:
                                                graph.SetTitle("LinADC vs Charge, Range %i, %s, QIE %.1f" % (i_range,qieUniqueID,qieNumber))
                                        else:
                                                graph.SetTitle("LinADC vs Charge, Range %i, %s, QIE %i,Shunt %.1f" % (i_range,qieUniqueID,qieNumber,shuntMult))
                                        graph.GetYaxis().SetRangeUser(ymin-graphOffset[i_range],graph.GetYaxis().GetXmax()+graphOffset[i_range]*4)
                                else:
                                        N_ = graph.GetN()
                                        x_ = graph.GetX()
                                        y_ = graph.GetY()
                                        for n in range(N_):
                                                graph.SetPoint(n,x_[n],y_[n]+(graphOffset[i_range]*i_capID))
                                                fitLine.SetParameter(1,fitLine.GetParameter(1)+(graphOffset[i_range]*i_capID))
                                graph.Draw("p, same")
                                fitLine.Draw("same")
                                if not i_range==3:
                                        text = TPaveText(xmin +5, ymax + 3*graphOffset[i_range] - (ymax-ymin)*(.7) ,xmin + 50 ,ymax+3.75*graphOffset[i_range])
                                else:
                                        text = TPaveText(xmin +25, ymax + 2*graphOffset[i_range] - (ymax-ymin)*(.7) ,xmin + 75 ,ymax+3.75*graphOffset[i_range])

                        text.SetFillColor(kWhite)
                        text.SetFillStyle(4000)
                        text.SetTextAlign(11)
                        text.AddText("CapID 0:")
                        text.AddText("    Slope =  %.2f +- %.2f fC/ADC" % slopes[0])
                        text.AddText("    Offset =  %.2f +- %.2f fC" % offsets[0])
                        text.AddText("CapID 1:")
                        text.AddText("    Slope =  %.2f +- %.2f fC/ADC" % slopes[1])
                        text.AddText("    Offset =  %.2f +- %.2f fC" % offsets[1])
                        text.AddText("CapID 2:")
                        text.AddText("    Slope =  %.2f +- %.2f fC/ADC" % slopes[2])
                        text.AddText("    Offset =  %.2f +- %.2f fC" % offsets[2])
                        text.AddText("CapID 3:")
                        text.AddText("    Slope =  %.2f +- %.2f fC/ADC" % slopes[3])
                        text.AddText("    Offset =  %.2f +- %.2f fC" % offsets[3])
                        text.Draw("same")
                                
                        c1.SaveAs(saveName)

        return params




