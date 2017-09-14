//+ Combined (simultaneous) fit of two histogram with separate functions
//  and some common parameters
//
// See http://root.cern.ch/phpBB3//viewtopic.php?f=3&t=11740#p50908
// for a modified version working with Fumili or GSLMultiFit
//
// N.B. this macro must be compiled with ACliC
//
//Author: L. Moneta - Dec 2010
//#include <experimental/filesystem>
#include "Fit/Fitter.h"
#include "Fit/BinData.h"
#include "Fit/Chi2FCN.h"
#include "TH1.h"
#include "TGraphErrors.h"
#include "TGraph.h"
#include "TFile.h"
#include "TList.h"
#include "Math/WrappedMultiTF1.h"
#include "HFitInterface.h"
#include "TCanvas.h"
#include "TStyle.h"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;
// definition of shared parameter
int ipar1[3] = { 0 , 1, 2}; //par[0] is shunt, par[1] and par[2] are slope/offset for graph1
int ipar2[3] = { 0 , 3, 4}; //par[0] is shunt, par[3] and par[4] are slope/offset for graph2
int ipar3[3] = { 0 , 5, 6}; //par[0] is shunt, par[5] and par[6] are slope/offset for graph3
int ipar4[3] = { 0 , 7, 8}; //par[0] is shunt, par[7] and par[8] are slope/offset for graph4
int ipar5[3] = { 0 , 9, 10}; //par[0] is shunt, par[9] and par[10] are slope/offset for graph1
int ipar6[3] = { 0 , 11, 12}; //par[0] is shunt, par[11] and par[12] are slope/offset for graph2
int ipar7[3] = { 0 , 13, 14}; //par[0] is shunt, par[13] and par[14] are slope/offset for graph3
int ipar8[3] = { 0 , 15, 16}; //par[0] is shunt, par[15] and par[16] are slope/offset for graph4

struct GlobalChi2 {
  GlobalChi2(  ROOT::Math::IMultiGenFunction & f1,
	       ROOT::Math::IMultiGenFunction & f2,
	       ROOT::Math::IMultiGenFunction & f3,
	       ROOT::Math::IMultiGenFunction & f4,
	       ROOT::Math::IMultiGenFunction & f5,
               ROOT::Math::IMultiGenFunction & f6,
               ROOT::Math::IMultiGenFunction & f7,
               ROOT::Math::IMultiGenFunction & f8) :
    fChi2_1(&f1), fChi2_2(&f2),fChi2_3(&f3), fChi2_4(&f4),  fChi2_5(&f5), fChi2_6(&f6),fChi2_7(&f7), fChi2_8(&f8) {}

  // parameter vector is first background (in common 1 and 2)
  // and then is signal (only in 2)
  double operator() (const double *par) const {
    double p1[3];
    double p2[3];
    double p3[3];
    double p4[3];
    double p5[3];
    double p6[3];
    double p7[3];
    double p8[3];
    for (int i = 0; i < 3; ++i) {
      p1[i] = par[ipar1[i] ];
      p2[i] = par[ipar2[i] ];
      p3[i] = par[ipar3[i] ];
      p4[i] = par[ipar4[i] ];
      p5[i] = par[ipar5[i] ];
      p6[i] = par[ipar6[i] ];
      p7[i] = par[ipar7[i] ];
      p8[i] = par[ipar8[i] ];

    }


    return (*fChi2_1)(p1) + (*fChi2_2)(p2) + (*fChi2_3)(p3) + (*fChi2_4)(p4)+(*fChi2_5)(p5) + (*fChi2_6)(p6) + (*fChi2_7)(p7) + (*fChi2_8)(p8);
  }

  const  ROOT::Math::IMultiGenFunction * fChi2_1;
  const  ROOT::Math::IMultiGenFunction * fChi2_2;
  const  ROOT::Math::IMultiGenFunction * fChi2_3;
  const  ROOT::Math::IMultiGenFunction * fChi2_4;
  const  ROOT::Math::IMultiGenFunction * fChi2_5;
  const  ROOT::Math::IMultiGenFunction * fChi2_6;
  const  ROOT::Math::IMultiGenFunction * fChi2_7;
  const  ROOT::Math::IMultiGenFunction * fChi2_8;
};

#include <stdlib.h> 
void makeFits_loop() {
  string x, y;
  string z;
  string UIDall[60];
  string UID1[650];
  string UID2[650];
  ifstream infile;
  int num = 0;
 // string line;
  infile.open("UID_all.txt");
  while(!infile.eof())
	{
       // getline(infile, line);
	//istringstream iss(line);
        infile>>std::hex >> z;
        UIDall[num]=z;
        ++num;
  }
  infile.close();  
//  cout << UID1[0] << endl;
 // int num1=0;
 // ifstream infile1;  
 // infile1.open("UID2.txt");
 // while(!infile1.eof())

 // {
   //     infile1 >>std::hex>>y;
     //   UID2[num1]=y; 
       // ++num1;
 // }
  //infile1.close(); 
  cout << UIDall[30] << endl;
  //exit;
  //string f2 = "0x94000000_0xeaa10570";
  char f2[640];
  for( int a = 0; a < 55; a = a+ 1 ) {
 // string code1 = UID2[a]+"_"+UID1[a];
  string code1 = UIDall[a];
  cout <<code1<<endl; 
 
 // sprintf(f2,code);
  char f1[100];
  sprintf(f1,"/Users/titasroy/HE_shunt_fits/CalibrationScripts/small_rootfiles/fitResults_%s.root",code1.c_str());
 // ++count;
 // cout <<count<<endl;
 // cout <<code<<endl;
  TFile* _file = TFile::Open(f1,"READ");
  char filename[100];
  char filename1[100];
  char filename2[100];
  char filename3[100];
  char filename4[100];
  char filename5[100];
  char filename6[100];
  char filename7[100];
  char filename8[100];
  char filename9[100];
  char filename10[100];
  char filename11[100];
  char filename12[100];
  char filename13[100];
  char filename14[100];
  char filename15[100];
  vector<float> shuntMult = {1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 11.5};
  vector<float> shunt_factor;
  vector<float> shunt_factor1;
  vector<float> shunt_factor2;
  vector<float> shunt_factor3;
  vector<float> shunt_factor4;
  vector<float> shunt_factor5;
  vector<float> shunt_factor6;
  vector<float> shunt_factor7;
  vector<float> shunt_factor8;
  vector<float> shunt_factor9;
  vector<float> slopes_0_r0;
  vector<float> slopes_1_r0;
  vector<float> slopes_2_r0;
  vector<float> slopes_3_r0;
  vector<float> slopes_0_r1;
  vector<float> slopes_1_r1;
  vector<float> slopes_2_r1;
  vector<float> slopes_3_r1;
  vector<float> slopeshunted_0_r0;
  vector<float> slopeshunted_1_r0;
  vector<float> slopeshunted_2_r0;
  vector<float> slopeshunted_3_r0;
  vector<float> slopeshunted_0_r1;
  vector<float> slopeshunted_1_r1;
  vector<float> slopeshunted_2_r1;
  vector<float> slopeshunted_3_r1;
  //string testName=“”;
  char testName[100];
  int start = 0;
  for (int i = 0; i < 12; i++){
	sprintf(testName,"LinadcVsCharge/LinADCvsfC_%d_1_range_0_shunt_1.0_capID_0_linearized",i*12);
   if (_file->Get(testName)!=0x0) { start=i*12; cout << "here" << i << endl;}
    }
  cout << start << endl;
  for (int m = 0; m < shuntMult.size(); m++){
  	for( int k=0; k < 12; k++ ){
		int j =k+1;
		int i = k+start;                

		
  		sprintf(filename,"LinadcVsCharge/LinADCvsfC_%d_%d_range_0_shunt_1.0_capID_0_linearized",i,j);
  		sprintf(filename1,"LinadcVsCharge/LinADCvsfC_%d_%d_range_0_shunt_1.0_capID_1_linearized",i,j);
  		sprintf(filename2,"LinadcVsCharge/LinADCvsfC_%d_%d_range_0_shunt_1.0_capID_2_linearized",i,j);
  		sprintf(filename3,"LinadcVsCharge/LinADCvsfC_%d_%d_range_0_shunt_1.0_capID_3_linearized",i,j);
  		sprintf(filename4,"LinadcVsCharge/LinADCvsfC_%d_%d_range_1_shunt_1.0_capID_0_linearized",i,j);
  		sprintf(filename5,"LinadcVsCharge/LinADCvsfC_%d_%d_range_1_shunt_1.0_capID_1_linearized",i,j);
  		sprintf(filename6,"LinadcVsCharge/LinADCvsfC_%d_%d_range_1_shunt_1.0_capID_2_linearized",i,j);
  		sprintf(filename7,"LinadcVsCharge/LinADCvsfC_%d_%d_range_1_shunt_1.0_capID_3_linearized",i,j);
  
  		sprintf(filename8,"Shunted_LinadcVsCharge/LinADCvsfC_%d_%d_range_0_shunt_%.1f_capID_0_linearized",i,j,shuntMult[m]);
  		sprintf(filename9,"Shunted_LinadcVsCharge/LinADCvsfC_%d_%d_range_0_shunt_%.1f_capID_1_linearized",i,j,shuntMult[m]);
  		sprintf(filename10,"Shunted_LinadcVsCharge/LinADCvsfC_%d_%d_range_0_shunt_%.1f_capID_2_linearized",i,j,shuntMult[m]);
  		sprintf(filename11,"Shunted_LinadcVsCharge/LinADCvsfC_%d_%d_range_0_shunt_%.1f_capID_3_linearized",i,j,shuntMult[m]);
  		sprintf(filename12,"Shunted_LinadcVsCharge/LinADCvsfC_%d_%d_range_1_shunt_%.1f_capID_0_linearized",i,j,shuntMult[m]);
  		sprintf(filename13,"Shunted_LinadcVsCharge/LinADCvsfC_%d_%d_range_1_shunt_%.1f_capID_1_linearized",i,j,shuntMult[m]);
  		sprintf(filename14,"Shunted_LinadcVsCharge/LinADCvsfC_%d_%d_range_1_shunt_%.1f_capID_2_linearized",i,j,shuntMult[m]);
  		sprintf(filename15,"Shunted_LinadcVsCharge/LinADCvsfC_%d_%d_range_1_shunt_%.1f_capID_3_linearized",i,j,shuntMult[m]);
	
	
		std::cout<<filename<<std::endl;	
        
  		//TKey *key = _file->FindKey(filename);
	//	if (key ==0){
 	//		cout << "!!Histogram does not exist!!" << endl;
	//		continue;
		
		std::cout<<filename8<<std::endl;

  		TGraphErrors *g1 = (TGraphErrors*)_file->Get(filename);
  		TGraphErrors * g2 = (TGraphErrors*) _file->Get(filename1);
  		TGraphErrors * g3 = (TGraphErrors*) _file->Get(filename2);
  		TGraphErrors * g4 = (TGraphErrors*) _file->Get(filename3);
		TGraphErrors * g5 = (TGraphErrors*) _file->Get(filename4);
		TGraphErrors * g6 = (TGraphErrors*) _file->Get(filename5);
		TGraphErrors * g7 = (TGraphErrors*) _file->Get(filename6);
		TGraphErrors * g8 = (TGraphErrors*) _file->Get(filename7);
		TGraphErrors * g1shunt =(TGraphErrors*)  _file->Get(filename8);
		TGraphErrors * g2shunt =(TGraphErrors*)  _file->Get(filename9);
		TGraphErrors * g3shunt =(TGraphErrors*)  _file->Get(filename10);
		TGraphErrors * g4shunt =(TGraphErrors*)  _file->Get(filename11);

		TGraphErrors * g5shunt =(TGraphErrors*)  _file->Get(filename12);
		TGraphErrors * g6shunt =(TGraphErrors*)  _file->Get(filename13);
		TGraphErrors * g7shunt =(TGraphErrors*)  _file->Get(filename14);
		TGraphErrors * g8shunt =(TGraphErrors*)  _file->Get(filename15);
  		
		std::cout << "before linear fit" << std::endl;
		TF1 *pol1 = new TF1("pol1","pol1",200,600);
		g1->Fit("pol1","R0");
		g2->Fit("pol1","R0");
		g3->Fit("pol1","R0");
		g4->Fit("pol1","R0");
		g5->Fit("pol1","0");
		g6->Fit("pol1","0");
		g7->Fit("pol1","0");
		g8->Fit("pol1","0");
                g1shunt->Fit("pol1","0");
                g2shunt->Fit("pol1","0");
                g3shunt->Fit("pol1","0");
                g4shunt->Fit("pol1","0");
                g5shunt->Fit("pol1","0");
                g6shunt->Fit("pol1","0");
                g7shunt->Fit("pol1","0");
                g8shunt->Fit("pol1","0");
		std::cout << "before get parameters" << std::endl;
		double offset1 = g1->GetFunction("pol1")->GetParameter(0);
		double offset2 = g2->GetFunction("pol1")->GetParameter(0);
		double offset3 = g3->GetFunction("pol1")->GetParameter(0);
		double offset4 = g4->GetFunction("pol1")->GetParameter(0);
		double offset5 = g5->GetFunction("pol1")->GetParameter(0);
		double offset6 = g6->GetFunction("pol1")->GetParameter(0);
		double offset7 = g7->GetFunction("pol1")->GetParameter(0);
		double offset8 = g8->GetFunction("pol1")->GetParameter(0);
		double slope1 = g1->GetFunction("pol1")->GetParameter(1);
		double slope2 = g2->GetFunction("pol1")->GetParameter(1);
		double slope3 = g3->GetFunction("pol1")->GetParameter(1);
		double slope4 = g4->GetFunction("pol1")->GetParameter(1);
		double slope5 = g5->GetFunction("pol1")->GetParameter(1);
		double slope6 = g6->GetFunction("pol1")->GetParameter(1);
		double slope7 = g7->GetFunction("pol1")->GetParameter(1);
		double slope8 = g8->GetFunction("pol1")->GetParameter(1);
		double slope9 = g1shunt->GetFunction("pol1")->GetParameter(1);
                double slope10 = g2shunt->GetFunction("pol1")->GetParameter(1);
                double slope11 = g3shunt->GetFunction("pol1")->GetParameter(1);
                double slope12 = g4shunt->GetFunction("pol1")->GetParameter(1);
                double slope13 = g5shunt->GetFunction("pol1")->GetParameter(1);
                double slope14 = g6shunt->GetFunction("pol1")->GetParameter(1);
                double slope15 = g7shunt->GetFunction("pol1")->GetParameter(1);
                double slope16 = g8shunt->GetFunction("pol1")->GetParameter(1);
  
  // define functions with slopes and offsets as additional parameters, these can then be set and fixed (not fit)
		TF1 * f1 = new TF1("fit1","[0]*([1]+[2]*x)",200,9e9);
		TF1 * f2 = new TF1("fit2","[0]*([1]+[2]*x)",200,9e9);
		TF1 * f3 = new TF1("fit3","[0]*([1]+[2]*x)",200,9e9);
		TF1 * f4 = new TF1("fit4","[0]*([1]+[2]*x)",200,9e9);
		TF1 * f5 = new TF1("fit5","[0]*([1]+[2]*x)",200,9e9);
		TF1 * f6 = new TF1("fit6","[0]*([1]+[2]*x)",200,9e9);
		TF1 * f7 = new TF1("fit7","[0]*([1]+[2]*x)",200,9e9);
		TF1 * f8 = new TF1("fit8","[0]*([1]+[2]*x)",200,9e9);

  // perform now global fit


		ROOT::Math::WrappedMultiTF1 wf1(*f1,1);
		ROOT::Math::WrappedMultiTF1 wf2(*f2,1);
		ROOT::Math::WrappedMultiTF1 wf3(*f3,1);
		ROOT::Math::WrappedMultiTF1 wf4(*f4,1);
		ROOT::Math::WrappedMultiTF1 wf5(*f5,1);
		ROOT::Math::WrappedMultiTF1 wf6(*f6,1);
		ROOT::Math::WrappedMultiTF1 wf7(*f7,1);
		ROOT::Math::WrappedMultiTF1 wf8(*f8,1);
		ROOT::Fit::DataOptions opt;
		ROOT::Fit::DataRange range;
  // set the data range
		range.SetRange(200,9e9);


		ROOT::Fit::BinData data1(opt,range);
		ROOT::Fit::FillData(data1, g1shunt);

		ROOT::Fit::BinData data2(opt,range);
		ROOT::Fit::FillData(data2, g2shunt);

		ROOT::Fit::BinData data3(opt,range);
		ROOT::Fit::FillData(data3, g3shunt);

		ROOT::Fit::BinData data4(opt,range);
		ROOT::Fit::FillData(data4, g4shunt);

		ROOT::Fit::BinData data5(opt,range);
		ROOT::Fit::FillData(data5, g5shunt);

		ROOT::Fit::BinData data6(opt,range);
		ROOT::Fit::FillData(data6, g6shunt);

		ROOT::Fit::BinData data7(opt,range);
		ROOT::Fit::FillData(data7, g7shunt);

		ROOT::Fit::BinData data8(opt,range);
		ROOT::Fit::FillData(data8, g8shunt);

		ROOT::Fit::Chi2Function chi2_1(data1, wf1);
		ROOT::Fit::Chi2Function chi2_2(data2, wf2);
		ROOT::Fit::Chi2Function chi2_3(data3, wf3);
		ROOT::Fit::Chi2Function chi2_4(data4, wf4);
		ROOT::Fit::Chi2Function chi2_5(data5, wf5);
		ROOT::Fit::Chi2Function chi2_6(data6, wf6);
		ROOT::Fit::Chi2Function chi2_7(data7, wf7);
		ROOT::Fit::Chi2Function chi2_8(data8, wf8);


		GlobalChi2 globalChi2(chi2_1, chi2_2, chi2_3, chi2_4, chi2_5, chi2_6, chi2_7, chi2_8);

		ROOT::Fit::Fitter fitter;

		const int Npar = 17;
		double par0[Npar] = { 6, 
			offset1, slope1,
			offset2, slope2,
			offset3, slope3,
			offset4, slope4,
                        offset5, slope5,
                        offset6, slope6,
                        offset7, slope7,
                        offset8, slope8};
//  std::cout << "HERE" << std::endl;


  // create before the parameter settings in order to fix or set range on them
		fitter.Config().SetParamsSettings(17,par0);
		fitter.Config().ParSettings(1).Fix();
		fitter.Config().ParSettings(2).Fix();
		fitter.Config().ParSettings(3).Fix();
		fitter.Config().ParSettings(4).Fix();
		fitter.Config().ParSettings(5).Fix();
		fitter.Config().ParSettings(6).Fix();
		fitter.Config().ParSettings(7).Fix();
		fitter.Config().ParSettings(8).Fix();
		fitter.Config().ParSettings(9).Fix();
		fitter.Config().ParSettings(10).Fix();
		fitter.Config().ParSettings(11).Fix();
		fitter.Config().ParSettings(12).Fix();
		fitter.Config().ParSettings(13).Fix();
		fitter.Config().ParSettings(14).Fix();
		fitter.Config().ParSettings(15).Fix();
		fitter.Config().ParSettings(16).Fix();


		fitter.Config().MinimizerOptions().SetPrintLevel(0);
		fitter.Config().SetMinimizer("Minuit2","Migrad");
		fitter.FitFCN(17,globalChi2,0,data1.Size()+data2.Size()+data3.Size()+data4.Size()+data5.Size()+data6.Size()+data7.Size()+data8.Size(),true);
		ROOT::Fit::FitResult result = fitter.Result();
                //  result.Print(std::cout);
  
		shunt_factor.push_back(1/(result.Parameter(0)));
		shunt_factor1.push_back(slope1/slope9);
                shunt_factor2.push_back(slope2/slope10);
                shunt_factor3.push_back(slope3/slope11);
                shunt_factor4.push_back(slope4/slope12);
                shunt_factor5.push_back(slope5/slope13);
                shunt_factor6.push_back(slope6/slope14);
                shunt_factor7.push_back(slope7/slope15);
                shunt_factor8.push_back(slope8/slope16);
		slopes_0_r0.push_back(slope1);
  		slopes_1_r0.push_back(slope2);
  		slopes_2_r0.push_back(slope3);
  		slopes_3_r0.push_back(slope4);
		slopes_0_r1.push_back(slope5);
                slopes_1_r1.push_back(slope6);
                slopes_2_r1.push_back(slope7);
                slopes_3_r1.push_back(slope8); //slopeshunted_0_r0
		slopeshunted_0_r0.push_back(slope9);
                slopeshunted_1_r0.push_back(slope10);
                slopeshunted_2_r0.push_back(slope11);
                slopeshunted_3_r0.push_back(slope12);
                slopeshunted_0_r1.push_back(slope13);
                slopeshunted_1_r1.push_back(slope14);
                slopeshunted_2_r1.push_back(slope15);
                slopeshunted_3_r1.push_back(slope16);
                shunt_factor9.push_back((slope1/slope9 +slope2/slope10+slope3/slope11+slope4/slope12+slope5/slope13+slope6/slope14+slope7/slope15+slope8/slope16)/8.);
		
//		}
		}
	}


ofstream file_;
//std::ifstream file_("slopes_method2_%s.txt",f2);
char f3[100];
sprintf(f3,"slopes_method2_%s.txt",code1.c_str());

file_.open (f3);
for (int i = 0; i < 12; i++) {
	file_ << shunt_factor[i] << std::setw(10) << shunt_factor[i+12] << std::setw(10) << shunt_factor[i+24] << std::setw(10) << shunt_factor[i+36] << std::setw(10) << shunt_factor[i+48] << std::setw(10) << shunt_factor[i+60] << std::setw(10) << shunt_factor[i+72] << std::setw(10) << shunt_factor[i+84] << std::setw(10) << shunt_factor[i+96] << std::setw(10) << shunt_factor[i+108] << std::setw(10) << shunt_factor[i+120] << std::setw(10) << shunt_factor[i+132] <<'\n';
  }
}
}
