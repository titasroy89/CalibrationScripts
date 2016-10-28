from ROOT import *
gROOT.SetBatch()
#from scan_forHE import *
from array import array
# from ROOT import *
# gROOT.SetBatch()
# c1 = TCanvas('c1', 'Plots', 1000, 500)
# c1.SetFillColor(0)
# c1.SetGrid()
# c1.Clear()
# c1.SetLogy()
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

def read_histo_2d(file_in="trial.root",shuntMult = 1):

        result = {}
        tf = TFile(file_in, "READ")

        histNameScheme = tf.GetListOfKeys()[9].GetName().split('_')
        histNameStart = histNameScheme[0]+'_'+histNameScheme[1]

        shuntVal = shunt_Val[shuntMult]

        results = {}
        for i_qieRange in range(4):
                if shuntVal > 0 and i_qieRange==2: continue
                results[i_qieRange] = {}
                rangeADCoffset = i_qieRange*64.
                for i_link in range(24):
                        goodLink = True
                        for i_channel in range(6):
                                histName = "%s_f%i_c%i_r%i_s%i"%(histNameStart, i_link, i_channel, i_qieRange, shuntVal)
                                #print histName
                                hist = tf.Get(histName)
                                if type(hist)==type(TObject()):
                                        goodLink = False
                                        break
                                histNum = 6*i_link + i_channel
                                results[i_qieRange][histNum] = {}
                                #DAC_val =array('d')
                                for i_bin in range(1,hist.GetNbinsX()+1):
                                        

                                        hist.GetXaxis().SetRange(i_bin,i_bin)
                                        dacVal = int(hist.GetXaxis().GetBinLowEdge(i_bin))
                                       # DAC_val.append(dacVal)
                                #        print DAC_val
#                                         print "range_%i_dac_%i"%(i_qieRange,dacVal)

                                        info = {}
                                        info["link"] = i_link
                                        info["channel"] = i_channel
                                        info["mean"] = []
                                        info["rms"] = []
                                        
                                        for i_capID in range(4):
                                                offset = 64*(i_capID)
                                                hist.GetYaxis().SetRangeUser(offset, offset+63)
                                                info["mean"].append(hist.GetMean(2)-offset+rangeADCoffset)
                                                info["rms"].append(max(hist.GetRMS(2), 0.01))
                                        results[i_qieRange][histNum][dacVal] = info

                        if not goodLink: continue
                                        
        tf.Close()
                                
        return results#DAC_val

# f = read_histo_2d(file_in="/home/hep/jmmans/chargy/hcal/hcalUHTR/Data_CalibrationScans/2016-07-26/Run_15/QIECalibration_2.root",shuntMult = 8.0)
# dac= f[0][90].keys()
# dac.sort()
# print dac
# #i_range = f.keys()
# #i_range.sort()
# #mean=f[0][0][320]['mean'][0]
# #print mean
# #channel = f[0].keys()
# #channel.sort()
# #print channel
# #for i in range(len(dac)):
#  #   print dac[i]
