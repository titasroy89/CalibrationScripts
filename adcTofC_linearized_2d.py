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



def makeADCvsfCgraphSepCapID(values, histo_list = range(0,96), linkMap = {}, injectionCardMap = {},qieRange=0,shuntMult=1):

    conSlopes = lite.connect("Slopes_Offsets_new.db")
   

    print 'Making TGraphs from histos'


    graphs = {}
    graphs_2={}
    i_range=qieRange
    if shuntMult == 1:
            qierange = range(4)
    else :
            qierange = range(2)
    if i_range > 0 or shuntMult>1:
        highCurrent = True
    else:
        highCurrent = False
    print "Now on shunt %.1f and range %i"%(shuntMult,i_range)
    if highCurrent:
        print "Using high-current mode"
    else:
        print "Using low-current mode"
    lsbList = values[histo_list[0]].keys()
    lsbList.sort()
    for ih in histo_list:
            QIE_values = []

            channel = (ih % 12 + 1)
            linkNum = int(ih/6)

            backplane_slotNum = linkMap[linkNum]['slot']

            if not backplane_slotNum in injectionCardMap:
                print 'backplane slot not mapped to charge injection card!!!'
                sys.exit()

            injectioncard = injectionCardMap[backplane_slotNum][0]
            dac = injectionCardMap[backplane_slotNum][1]
        
        
            cur_Slopes = conSlopes.cursor()

            for i_lsb in lsbList:
        
                if i_lsb> 48000: continue
                query = ( injectioncard, int(dac), channel, int(highCurrent), i_lsb, i_lsb)
                cur_Slopes.execute('SELECT offset, slope FROM CARDCAL WHERE card=? AND dac=? AND channel=? AND highcurrent=? AND rangelow<=? AND rangehigh>=?', query )
                result_t = cur_Slopes.fetchone()

                offset = result_t[0]
                slope = result_t[1]
                

                current = i_lsb*slope + offset
                charge = current*25e6
                
                mean_ = []
                rms_ = []
                for i_capID in range(4):
                    mean_.append(values[ih][i_lsb]['mean'][i_capID])
                    rms_.append(values[ih][i_lsb]['rms'][i_capID])
                QIE_values.append([i_lsb,-1*charge,mean_,rms_])

            QIE_values.sort()
            graphs[ih] = []
            for i_capID in range(4):
                adcerr_array_new = array('d')
                fc_array_div = array('d')
                fc_array = array('d',[b[1] for b in QIE_values])
                for i in fc_array:
                    fc_array_div.append(i/shuntMult)
                fCerror_array = array('d',[0]*len(fc_array))
                adc_array = array('d',[b[2][i_capID] for b in QIE_values])
                adcerr_array = array('d',[b[3][i_capID] for b in QIE_values])
                myInt = len(adcerr_array)
                for i in adcerr_array:
                    adcerr_array_new.append(i/myInt)
                    
                ADCvsfC=TGraphErrors(len(fc_array),adc_array,fc_array,adcerr_array_new,fCerror_array)
                ADCvsfC.SetNameTitle("ADCvsfC_%i_%i_range_%i_shunt_%i_%i_capID_%i"%(ih, channel,i_range,int(shuntMult),int(shuntMult%1*10),i_capID),"ADCvsfC_%i_%i_range_%i_shunt_%i_%i_capID_%i"%(ih, channel,i_range,int(shuntMult),int(shuntMult%1*10),i_capID))

                graphs[ih].append(ADCvsfC)
         
    return graphs

    
