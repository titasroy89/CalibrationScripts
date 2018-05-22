from ROOT import *
import re
from array import array
import os
import sys
import numpy
import csv
import sqlite3 as lite
from Style import *
import time
start_time = time.time()
c1 = TCanvas('c1', 'Plots', 1000, 1000)
c1.SetFillColor(0)
c1.SetGrid()
c2 = TCanvas('c2', 'Plots', 1000, 1000)
c2.SetFillColor(0)
c2.SetGrid()
l = c1.GetLeftMargin()
gStyle.SetOptStat(111111)
#gStyle.SetStatY(0.9)
#gStyle.SetStatX(0.4)
#gStyle.SetStatW(0.2)
#gStyle.SetStatH(2.3)
#thestyle = Style()
#thestyle.SetStyle()
gROOT.SetBatch(kTRUE)
directory = "/Users/titasroy/HE_shunt_fits/CalibrationScripts/database_Oct16/"
database_=[]
for paramFileName in os.listdir(directory):
       # print paramFileName
        outputDirectory = paramFileName.split('qieCalibrationParameters')[1]
        name= outputDirectory.split('.db')[0]

        database_.append(name.split('_')[2])

f=open("sentcern.txt","r")
lines=f.readlines()
result=[]
for x in lines:
    result.append(x.split(' ')[0])
f.close()
results_new=[]
for i in range(639):
        results_new.append(result[i].strip())
#print len(results_new)

for elements in database_:	
	if elements not in results_new:
		database_.remove(elements)

#print "Finally running over :", len(database_)


slope0=[[] for i in range(12)]
slope1=[[] for i in range(12)]
h1=[]
h1.append(TH1D("Shunt_Factors", "Shunt 1.5",100,1.3,1.8))
h1.append(TH1D("Shunt_Factors", "Shunt 2",100,1.8,2.3))
h1.append(TH1D("Shunt_Factors", "Shunt 3",100,2.8,3.3))
h1.append(TH1D("Shunt_Factors", "Shunt 4",100,3.5,4.3))
h1.append(TH1D("Shunt_Factors", "Shunt 5",100,4.5,5.3))
h1.append(TH1D("Shunt_Factors", "Shunt 6",100,5.5,6.5))
h1.append(TH1D("Shunt_Factors", "Shunt 7",100,6.5,7.5))
h1.append(TH1D("Shunt_Factors", "Shunt 8",100,7.0,8.7))
h1.append(TH1D("Shunt_Factors", "Shunt 9",100,8.0,9.5))
h1.append(TH1D("Shunt_Factors", "Shunt 10",100,9.0,10.5))
h1.append(TH1D("Shunt_Factors", "Shunt 11",100,9.5,11.5))
h1.append(TH1D("Shunt_Factors", "Shunt 11.5",100,10.2,12.2))
h2=[]

h2.append(TH2D("Comparing R0 &R1 Shunt_Factors","Comparing R0 & R1 Shunt_Factors Shunt 1.5",100,1.3,1.8,100,1.3,1.8))
h2.append(TH2D("Comparing R0 &R1 Shunt_Factors","Comparing R0 & R1 Shunt_Factors Shunt 2",100,1.8,2.3,100,1.8,2.3))
h2.append(TH2D("Comparing R0 &R1 Shunt_Factors","Comparing R0 & R1 Shunt_Factors Shunt 3",100,2.8,3.3,100,2.8,3.3))
h2.append(TH2D("Comparing R0 &R1 Shunt_Factors","Comparing R0 & R1 Shunt_Factors Shunt 4",100,3.5,4.3,100,3.5,4.3))
h2.append(TH2D("Comparing R0 &R1 Shunt_Factors","Comparing R0 & R1 Shunt_Factors Shunt 5",100,4.5,5.3,100,4.5,5.3))
h2.append(TH2D("Comparing R0 &R1 Shunt_Factors","Comparing R0 & R1 Shunt_Factors Shunt 6",100,5.5,6.5,100,5.5,6.5))
h2.append(TH2D("Comparing R0 &R1 Shunt_Factors","Comparing R0 & R1 Shunt_Factors Shunt 7",100,6.5,7.5,100,6.5,7.5,))
h2.append(TH2D("Comparing R0 &R1 Shunt_Factors","Comparing R0 & R1 Shunt_Factors Shunt 8",100,7.0,8.7,100,7.0,8.7))
h2.append(TH2D("Comparing R0 &R1 Shunt_Factors","Comparing R0 & R1 Shunt_Factors Shunt 9",100,8.0,9.5,100,8.0,9.5))
h2.append(TH2D("Comparing R0 &R1 Shunt_Factors","Comparing R0 & R1 Shunt_Factors Shunt 10",100,9.0,10.5,100,9.0,10.5))
h2.append(TH2D("Comparing R0 &R1 Shunt_Factors","Comparing R0 & R1 Shunt_Factors Shunt 11",100,9.5,11.5,100,9.5,11.5))
h2.append(TH2D("Comparing R0 &R1 Shunt_Factors","Comparing R0 & R1 Shunt_Factors Shunt 11.5",100,10.2,12.2,100,10.2,12.2))

h3=[]
h3.append(TH1D("Shunt_Factors", "(R1-R0/R1) Shunt 1.5",100,-1,1))
h3.append(TH1D("Shunt_Factors", "(R1-R0/R1) Shunt 2",100,-1,1))
h3.append(TH1D("Shunt_Factors", "(R1-R0/R1) Shunt 3",100,-1,1))
h3.append(TH1D("Shunt_Factors", "(R1-R0/R1) Shunt 4",100,-1,1))
h3.append(TH1D("Shunt_Factors", "(R1-R0/R1) Shunt 5",100,-1,1))
h3.append(TH1D("Shunt_Factors", "(R1-R0/R1) Shunt 6",100,-1,1))
h3.append(TH1D("Shunt_Factors", "(R1-R0/R1) Shunt 7",100,-1,1))
h3.append(TH1D("Shunt_Factors", "(R1-R0/R1) Shunt 8",100,-1,1))
h3.append(TH1D("Shunt_Factors", "(R1-R0/R1) Shunt 9",100,-1,1))
h3.append(TH1D("Shunt_Factors", "(R1-R0/R1) Shunt 10",100,-1,1))
h3.append(TH1D("Shunt_Factors", "(R1-R0/R1) Shunt 11",100,-1,1))
h3.append(TH1D("Shunt_Factors", "(R1-R0/R1) Shunt 11.5",100,-1,1))

count=0
hist_slope =[[[] for i in range(4)] for i in range(13)]
hist_offset = [[[] for i in range(4)] for i in range(13)]
list_file = []
list_file_1 =[]
barcode_UID= lite.connect("HE_all639cards_parameters.db")
cursor = barcode_UID.cursor()
shunts=[1,1.5,2,3,4,5,6,7,8,9,10,11,11.5]
for shunt in shunts:
	if shunt==1:gsel=0
	if shunt==1.5: gsel = 1
	elif shunt == 2 :gsel=2
	elif shunt == 3: gsel=3
	elif shunt == 4: gsel=4
	elif shunt ==5: gsel=5
	elif shunt == 6 : gsel =6
	elif shunt == 7: gsel = 7
	elif shunt ==8 : gsel =8
	elif shunt ==9 : gsel=9
	elif shunt == 10 : gsel=10
	elif shunt ==11: gsel=11
	elif shunt ==11.5 : gsel=12
	for r in range(4):
		
		cursor.execute('select min(slope),max(slope), min(offset), max(offset) from qieshuntparams where range="%i" and shunt="%s"'%(r,shunt))
		result=cursor.fetchone()
		hist_offset[gsel][r]=(TH1D("Offsets", "Shunt_%s"%shunt,100,result[2]-20,result[3]+20))	
		hist_slope[gsel][r]=(TH1D("Slopes", "Shunt_%s"%shunt,100,.9*result[0],1.1*result[1])) 
		 	
#		print result


print("--- done with setting ranges for the TH1 in %s seconds ---" % (time.time() - start_time))
gsel=0		
for paramFileName in os.listdir(directory):
	print "Now on file:",paramFileName
	outputDirectory = paramFileName.split('qieCalibrationParameters')[1]
	count+=1
	
	name= outputDirectory.split('.db')[0]
	for element in database_:
		if element != name.split('_')[2]:
			continue
	name1= name.lstrip('_')
	name=name.replace('_',' ').lstrip(' ')
	slopes_shunts={}	
        file_in =directory+paramFileName
        barcode_UID = lite.connect(file_in)
	cursor = barcode_UID.cursor()
 	slopes_s0 = [[[] for i in range(4)] for i in range(4)]
	
	offsets_s0 = [[[] for i in range(4)] for i in range(4)]
        slopes_shunts=[[[[] for i in range(4)] for i in range(4)] for i in range(13)]
	offsets_shunts=[[[[] for i in range(4)] for i in range(4)] for i in range(13)]
        shunt_factors = [[[] for i in range(12)] for i in range(12)]
	shunt_factorsR0 = [[[] for i in range(12)] for i in range(12)]
	shunt_factorsR1 = [[[] for i in range(12)] for i in range(12)]
	method1ShuntFactor =[array('d') for i in range(12)]
	method1ShuntFactorR0 =[array('d') for i in range(12)]
	method1ShuntFactorR1 =[array('d') for i in range(12)]
	shunts=[1,1.5,2,3,4,5,6,7,8,9,10,11,11.5]
        
	for shunt in shunts:
		if shunt==1:gsel=0
		elif shunt==1.5: gsel = 1
		elif shunt == 2 :gsel=2
		elif shunt == 3: gsel=3
		elif shunt == 4: gsel=4
		elif shunt ==5: gsel=5
		elif shunt == 6 : gsel =6
		elif shunt == 7: gsel = 7
		elif shunt ==8 : gsel =8
		elif shunt ==9 : gsel=9
		elif shunt == 10 : gsel=10
		elif shunt ==11: gsel=11
		elif shunt ==11.5 : gsel=12
		#print shunt, gsel
		for i_qie in range(1,13):
    		    for r in range(4):
                	for i_capID in range(4):
				cursor.execute('SELECT slope, offset FROM qieshuntparams WHERE id="%s" and shunt="%s" and qie="%i" and range="%i" and capid="%i"'%(name,shunt, i_qie,r, i_capID))
				result = cursor.fetchone()
				
				if shunt==1:	
					slopes_shunts[0][r][i_capID].append(result[0])
					offsets_shunts[0][r][i_capID].append(result[1])
				else:
					slopes_shunts[gsel][r][i_capID].append(result[0])
					offsets_shunts[gsel][r][i_capID].append(result[1])

	

	print("--- done with getting slopes and offsets for one card in %s seconds ---" % (time.time() - start_time))
	gsels=[0,1,2,3,4,5,6,7,8,9,10,11,12]
	for gsel in gsels:
		if gsel==0:shunt=1
		elif gsel==1:shunt=1.5
		elif gsel==2:shunt=2
		elif gsel==3:shunt=3
		elif gsel==4:shunt=4
		elif gsel==5:shunt=5
		elif gsel==6:shunt=6
                elif gsel==7:shunt=7
                elif gsel==8:shunt=8
                elif gsel==9:shunt=9
                elif gsel==10:shunt=10
		elif gsel==11:shunt=11
		elif gsel==12:shunt=11.5
		#print "lenghth of shunt slopes:",len(slopes_shunts[gsel][0][0])
		
		for r in range(4):
			for c in range(4):
				for i in range(len(slopes_shunts[0][0][0])):
					#print gsel, r, c, i
					hist_slope[gsel][r].Fill(slopes_shunts[gsel][r][c][i])
					hist_offset[gsel][r].Fill(offsets_shunts[gsel][r][c][i])
	
			hist_slope[gsel][r].SetMarkerStyle(7)
			hist_slope[gsel][r].SetMarkerSize(2)
			hist_slope[gsel][r].SetMarkerColor(kRed)
	
			hist_slope[gsel][r].GetXaxis().SetTitle("Slopes LinADC/fC")
			hist_slope[gsel][r].GetYaxis().SetTitle("Shunt_%.1f"%(shunt))
	
			hist_slope[gsel][r].Draw()
                        c1.SetLogy()
			c1.SaveAs("Oct_plots_png/Slopes_%.1f_range%i_summary.png"%(shunt,r))
			c1.Clear()
			hist_offset[gsel][r].SetMarkerStyle(7)
			hist_offset[gsel][r].SetMarkerSize(2)
			hist_offset[gsel][r].SetMarkerColor(kRed)

			hist_offset[gsel][r].GetXaxis().SetTitle("Offsets LinADC")
			hist_offset[gsel][r].SetTitle("Shunt_%.1f"%(shunt))

			hist_offset[gsel][r].Draw()
			c1.SaveAs("Oct_plots_png/Offsets_%.1f_range%i_summary.png"%(shunt,r))
			c1.Clear()
	
	
	print "files done:",count
	gsels=[1,2,3,4,5,6,7,8,9,10,11,12]
	for gsel in gsels:
                if gsel==1:shunt=1.5
                elif gsel==2:shunt=2
                elif gsel==3:shunt=3
                elif gsel==4:shunt=4
                elif gsel==5:shunt=5
                elif gsel==6:shunt=6
                elif gsel==7:shunt=7
                elif gsel==8:shunt=8
                elif gsel==9:shunt=9
                elif gsel==10:shunt=10
                elif gsel==11:shunt=11
                elif gsel==12:shunt=11.5	
	 	for i_qie in range(12):
			for i_capid in range(4):
			#	slope0[gsel-1].append(slopes_shunts[0][0][i_capID][i_qie]/slopes_shunts[gsel
			#	slope1[gsel-1].append(slopes_shunts[0][1][i_capID][i_qie]/slopes_shunts[gsel][1][i_capID][i_qie])
				#shunt_factorsR0[i_qie][gsel-1].append(slopes_shunts[0][0][i_capID][i_qie]/slopes_shunts[gsel][0][i_capID][i_qie])
				shunt_factorsR1[i_qie][gsel-1].append(slopes_shunts[0][1][i_capID][i_qie]/slopes_shunts[gsel][1][i_capID][i_qie])
				for i_range in range(2):
					shunt_factors[i_qie][gsel-1].append(slopes_shunts[0][i_range][i_capID][i_qie]/slopes_shunts[gsel][i_range][i_capID][i_qie])
			method1ShuntFactor[gsel-1].append(numpy.mean(shunt_factors[i_qie][gsel-1]))
		#	method1ShuntFactorR0[gsel-1].append(numpy.mean(shunt_factorsR0[i_qie][gsel-1]))
			method1ShuntFactorR1[gsel-1].append(numpy.mean(shunt_factorsR1[i_qie][gsel-1]))
	#	for i in range(len(method1ShuntFactorR0[0])):
	#		h2[gsel-1].Fill(method1ShuntFactorR0[gsel-1][i],method1ShuntFactorR1[gsel-1][i])
	#		h2[gsel-1].GetXaxis().SetTitle("ShuntFactors from R0")
	#		h2[gsel-1].GetYaxis().SetTitle("ShuntFactors from R1")	
	#		h2[gsel-1].Draw("colz")	
	#		c2.SaveAs("Oct_plots_png/Comparing_method1fromR0R1_shunt_%.1f.png"%(shunt))
	#		c2.Clear()
	        
	#		h3[gsel-1].Fill((method1ShuntFactorR0[gsel-1][i]-method1ShuntFactorR1[gsel-1][i])/method1ShuntFactorR1[gsel-1][i])
	#		h3[gsel-1].GetXaxis().SetTitle("ShuntFactors from R1-R0/R1")
        #                h3[gsel-1].GetYaxis().SetTitle("Entries")
        #                h3[gsel-1].Draw() 
        #                c2.SaveAs("Oct_plots_png/Fractional_changebwR0R1_shunt_%.1f.png"%(shunt))
        #                c2.Clear()
		for i in range(len(method1ShuntFactor[0])):
			h1[gsel-1].Fill(method1ShuntFactorR1[gsel-1][i])
			h1[gsel-1].GetXaxis().SetTitle("ShuntFactors")
			h1[gsel-1].GetYaxis().SetTitle("Entries")
			c1.SetLogy()
			h1[gsel-1].Draw()
			
			c1.SaveAs("Oct_plots_png/ShuntFactors_%.1f_summary.png"%(shunt))
			c1.Clear()
	print("--- Done with shunt factors in %s seconds ---" % (time.time() - start_time))
#	with open("Shuntfactors/slopes_method1%s.csv"%(name1),"w") as file1_: 
#		writer = csv.writer(file1_, delimiter=',')
#		writer.writerows(zip(method1ShuntFactor[0],method1ShuntFactor[1],method1ShuntFactor[2],method1ShuntFactor[3],method1ShuntFactor[4],method1ShuntFactor[5],method1ShuntFactor[6],method1ShuntFactor[7],method1ShuntFactor[8],method1ShuntFactor[9],method1ShuntFactor[10],method1ShuntFactor[11]))
#	with open("Shuntfactors/slopes_method1%s_R0.csv"%(name1),"w") as file2_:
#		writer = csv.writer(file2_, delimiter=',')
#		writer.writerows(zip(method1ShuntFactorR0[0],method1ShuntFactorR0[1],method1ShuntFactorR0[2],method1ShuntFactorR0[3],method1ShuntFactorR0[4],method1ShuntFactorR0[5],method1ShuntFactorR0[6],method1ShuntFactorR0[7],method1ShuntFactorR0[8],method1ShuntFactorR0[9],method1ShuntFactorR0[10],method1ShuntFactorR0[11]))

#	with open("Shuntfactors/slopes_method1%s_R1.csv"%(name1),"w") as file3_:
#		writer = csv.writer(file3_, delimiter=',')
 #               writer.writerows(zip(method1ShuntFactorR1[0],method1ShuntFactorR1[1],method1ShuntFactorR1[2],method1ShuntFactorR1[3],method1ShuntFactorR1[4],method1ShuntFactorR1[5],method1ShuntFactorR1[6],method1ShuntFactorR1[7],method1ShuntFactorR1[8],method1ShuntFactorR1[9],method1ShuntFactorR1[10],method1ShuntFactorR1[11]))




