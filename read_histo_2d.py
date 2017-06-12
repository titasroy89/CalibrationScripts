from ROOT import *
gROOT.SetBatch()
#from scan_forHE import *
import sqlite3 as lite
from array import array
from linearADC import *
import math
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

def read_histo_2d(file_in="trial.root",shuntMult = 1, linkMap={}, injectionCardMap={}):
	shuntVal = shunt_Val[shuntMult]
        result = {}
        tf = TFile(file_in, "READ")
	rms={}
	mean={}
	conSlopes = lite.connect("Slopes_Offsets_new.db")        
        histNameScheme = tf.GetListOfKeys()[9].GetName().split('_')
        histNameStart = histNameScheme[0]+'_'+histNameScheme[1]

#	adcDist={}
        results = {}
	chargeBins={}
	charge={}
	histo_={}
	histo_charge={}
	if shuntMult == 1:
            qieRange = range(4)
    	else :
            qieRange = range(2)
        for i_qieRange in qieRange:
		if i_qieRange == 0 and shuntMult==1:
			 highCurrent = False
        	else:
                	highCurrent = True
       		print "Now on shunt %.1f and range %i"%(shuntMult,i_qieRange)
        #	if highCurrent:
         #       	print "Using high-current mode"
        #	else:
         #       	print "Using low-current mode"
		rms[i_qieRange]={}
		mean[i_qieRange]={}
                chargeBins[i_qieRange]={}
		charge[i_qieRange]={}
		histo_[i_qieRange]={}
		histo_charge[i_qieRange]={}
#		adcDist[i_qieRange]={}
                if shuntVal > 0 and i_qieRange==3: continue
                results[i_qieRange] = {}
                rangeADCoffset = i_qieRange*64.
                for i_link in range(24):
                        goodLink = True
                        for i_channel in range(6):
                                histName = "%s_f%i_c%i_r%i_s%i"%(histNameStart, i_link, i_channel, i_qieRange, shuntVal)
                                hist = tf.Get(histName)
                                if type(hist)==type(TObject()):
                                        goodLink = False
                                        break
				histBins = hist.GetNbinsX()
                                histNum = 6*i_link + i_channel
				ih = 6*i_link + i_channel
				channel = (ih % 12 + 1)
				backplane_slotNum = linkMap[i_link]['slot']
				
				if not backplane_slotNum in injectionCardMap:
					 print 'backplane slot not mapped to charge injection card!!!'
					 sys.exit()
				injectioncard = injectionCardMap[backplane_slotNum][0]
				dac = injectionCardMap[backplane_slotNum][1]
                                results[i_qieRange][histNum] = {}
				rms[i_qieRange][histNum]={}
                		mean[i_qieRange][histNum]={}
				chargeBins[i_qieRange][histNum]=array('d')
				charge[i_qieRange][histNum]=array('d')
				linADCBins=array('d')
				for i in range(i_qieRange*64,(i_qieRange+1)*64):
    					linADCBins.append(linADC(i-.5)[0])
				DACBins=array('d')
                                for i_bin in range(1,hist.GetNbinsX()+1):
					hist.GetXaxis().SetRange(i_bin,i_bin)
					DACBins.append(int(hist.GetXaxis().GetBinLowEdge(i_bin)))
                                        

                                        hist.GetXaxis().SetRange(i_bin,i_bin)
                                        dacVal = int(hist.GetXaxis().GetBinLowEdge(i_bin))
					

                                        info = {}
                                        info["link"] = i_link
                                        info["channel"] = i_channel
                                        info["mean"] = []
                                        info["rms"] = []
                                        bincontents=[]
                                        for i_capID in range(4):
                                                offset = 64*(i_capID)
                                                hist.GetYaxis().SetRangeUser(offset, offset+63.5)
                                               # info["mean"].append(hist.GetMean(2)-offset+rangeADCoffset)
                                               # info["rms"].append(max(hist.GetRMS(2), 0.01))
                                        results[i_qieRange][histNum][dacVal] = info
				cursor = conSlopes.cursor()		
				charge_=[]	
				for dacvalue in DACBins:
					if dacvalue > 48000: continue
					query = ( injectioncard, int(dac), channel, int(highCurrent), dacvalue, dacvalue)
					cursor.execute('SELECT offset, slope FROM CARDCAL WHERE card=? AND dac=? AND channel=? AND highcurrent=? AND rangelow<=? AND rangehigh>=?', query )
					result_t = cursor.fetchone()
	
					offset = result_t[0]
					slope = result_t[1]

					current = dacvalue*slope + offset
					chargeq = current*25e6
					chargeBins[i_qieRange][histNum].append(-1.*chargeq)

				
				histo_charge[i_qieRange][histNum]={}
				for i_capID in range(4):
					
					histo_charge[i_qieRange][histNum][i_capID]=TH2F("histocharge_fC_%i_%i_qieRange_%i_shunt_%i_%i_capID_%i"%(ih, channel,i_qieRange,int(shuntMult),int(shuntMult%1*10),i_capID),"histocharge_fC_%i_%i_range_%i_shunt_%i_%i_capID_%i"%(ih, channel,i_qieRange,int(shuntMult),int(shuntMult%1*10),i_capID),len(chargeBins[i_qieRange][histNum])-1,chargeBins[i_qieRange][histNum], len(linADCBins)-1, linADCBins)
					for ix in range(1,hist.GetNbinsX()+1):
						for iy in range(1,64):
							histo_charge[i_qieRange][histNum][i_capID].SetBinContent(ix,iy,hist.GetBinContent(ix,iy+i_capID*64))
					rms[i_qieRange][histNum][i_capID]=array('d')
					mean[i_qieRange][histNum][i_capID]=array('d')
					for ix in range(1,hist.GetNbinsX()+1):	
						charge[i_qieRange][histNum].append(float(chargeBins[i_qieRange][histNum][ix-1]))
				
						adcDist = histo_charge[i_qieRange][histNum][i_capID].ProjectionY("adc_%i_%i_qieRange_%i_shunt_%i_%i_capID_%i"%(ih, channel,i_qieRange,int(shuntMult),int(shuntMult%1*10),i_capID),ix,ix)
						#mean[i_qieRange][histNum][i_capID].append(adcDist.GetMean())
						N = adcDist.Integral()
						if N==0:continue
						mean[i_qieRange][histNum][i_capID].append(adcDist.GetMean())
						
				#		if adcDist.GetRMS()==0:
				#			 rms[i_qieRange][histNum][i_capID].append(1/math.sqrt(12*N))
				#		else:
				#			 rms[i_qieRange][histNum][i_capID].append(adcDist.GetRMS()/math.sqrt(N))
					       	rms[i_qieRange][histNum][i_capID].append(max(adcDist.GetRMS(),1/math.sqrt(12))/math.sqrt(N))
					
							
					
		

                       		if not goodLink: continue
                                        
        tf.Close()
                               
        return results, mean, rms, charge
