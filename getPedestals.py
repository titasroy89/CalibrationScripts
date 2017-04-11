from ROOT import *
from linearADC import *
import os
from array import array

bin0startLevel = -0.5

def linearizeGraph(graph, i_range):
    vOffset = i_range*64
    points = range(graph.GetN())
    points.reverse()
    removeRest = False
    graph.SetNameTitle(graph.GetName().replace("ADC","linADC"),graph.GetName().replace("ADC","linADC"))

    for n in points:
        x = graph.GetX()[n]-vOffset
        if x<1 or x>62:
            graph.RemovePoint(n)
            continue

#         if x>62:
#             graph.RemovePoint(n)
#             continue
#         if n==0:
#             graph.RemovePoint(n)
#             continue

#         if x < 1:
#             removeRest=True

#         if removeRest:
#             graph.RemovePoint(n)
#             continue

        _linADC, _linADCErr = linADC(graph.GetX()[n],graph.GetEX()[n])
        _charge = graph.GetY()[n]
        _chargeErr = graph.GetEY()[n]
        graph.GetX()[n] = _charge
        graph.GetEX()[n] = _chargeErr
        graph.GetY()[n] = _linADC
        graph.GetEY()[n] = _linADCErr
    if i_range==0:
        graph.RemovePoint(0)
    return graph


def getPedestals(graphs_shunt, shuntMult_list, histoList,dirName, date, run):
    pedestalVals = {}

    if not os.path.exists("%s/PedestalPlots"%dirName):
        os.mkdir("%s/PedestalPlots"%dirName)
    

    _file = TFile("%s/PedestalPlots/pedestalMeasurement_%s_%s.root"%(dirName,date,run),"update")

    c1 = TCanvas()
    c1.Divide(2,2)

    shuntPeds = {}
    
    for ih in histoList:
        _file.mkdir("h%i"%ih)
        _file.cd("h%i"%ih)
        print ih
        #get low current
        lowCurrentPeds = []
        for i_capID in range(4):
            #linearize the graph first 
            graph = linearizeGraph(graphs_shunt[1.0][ih][i_capID],0)
            print graph.GetName()
            graph.Fit("pol1","0")
            line = graph.GetFunction("pol1")
            graph.Write()
            #pedestal is the x-intercept of the graph (-offset/slope)
            lowCurrentPeds.append(-1*(line.GetParameter(0)-bin0startLevel)/line.GetParameter(1))


        #get high current peds
        highCurrentPeds = []
        highCurrentShuntPeds = {}
        for i_shunt in shuntMult_list:
            if i_shunt==1:
                continue
            highCurrentShuntPeds[i_shunt]=[]
            for i_capID in range(4):
                graph = linearizeGraph(graphs_shunt[i_shunt][ih][i_capID],0)
                graph.Fit("pol1","0")
                graph.Write()
                line = graph.GetFunction("pol1")
                highCurrentShuntPeds[i_shunt].append(-1*(line.GetParameter(0)-bin0startLevel)/line.GetParameter(1))


        #make graphs of the shunt vs measured pedestal
        graphs = []

        for i_capID in range(4):
            x = shuntMult_list[1:]
            y = []
            for s in shuntMult_list[1:]:
                y.append(highCurrentShuntPeds[s][i_capID])

            _x = array('d',x)
            _y = array('d',y)
                
            graphs.append(TGraph(len(x),_x,_y))
            graphs[-1].SetNameTitle(graphs_shunt[1.0][ih][i_capID].GetTitle().replace("_shunt_1_0_","_"),graphs_shunt[1.0][ih][i_capID].GetTitle().replace("_shunt_1_0_","_"))
	    graphs[-1].GetYaxis().SetRangeUser(-500,150)
            graphs[-1].Fit("pol1")
            line = graphs[-1].GetFunction("pol1")
            c1.cd(i_capID+1)
            graphs[-1].SetMarkerStyle(7)
            graphs[-1].SetMarkerSize(2)
            graphs[-1].GetXaxis().SetTitle("Shunt Value (nominal)")
            graphs[-1].GetYaxis().SetTitle("Measured total pedestal")
            graphs[-1].Draw("ap")
            graphs[-1].Write()

            highCurrentPeds.append(line.Eval(1))
            
        c1.SaveAs("%s/PedestalPlots/%s.pdf"%(dirName,graphs_shunt[1.0][ih][0].GetTitle().replace("_shunt_1_0_capID_0","")))
        
        pedestalVals[ih] = {"low":lowCurrentPeds,
                            "high":highCurrentPeds,
                            "shunts":highCurrentShuntPeds,
                            }

    _file.Close()

    return pedestalVals
