//+ Combined (simultaneous) fit of two histogram with separate functions
//  and some common parameters
//
// See http://root.cern.ch/phpBB3//viewtopic.php?f=3&t=11740#p50908
// for a modified version working with Fumili or GSLMultiFit
//
// N.B. this macro must be compiled with ACliC
//
//Author: L. Moneta - Dec 2010

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

void makeFits() {

  TFile* _file = TFile::Open("/Users/titasroy/cmshcal11_github/Data/2016-08-04/Run_05/fitResults_0x86000000_0xead65570.root","READ");

  TGraphErrors * g1 = (TGraphErrors*) _file->Get("LinadcVsCharge/ADCvsfC_120_1_range_0_shunt_1_0_capID_0_linearized");
  TGraphErrors * g2 = (TGraphErrors*) _file->Get("LinadcVsCharge/ADCvsfC_120_1_range_0_shunt_1_0_capID_1_linearized");
  TGraphErrors * g3 = (TGraphErrors*) _file->Get("LinadcVsCharge/ADCvsfC_120_1_range_0_shunt_1_0_capID_2_linearized");
  TGraphErrors * g4 = (TGraphErrors*) _file->Get("LinadcVsCharge/ADCvsfC_120_1_range_0_shunt_1_0_capID_3_linearized");
  TGraphErrors * g5 = (TGraphErrors*) _file->Get("LinadcVsCharge/ADCvsfC_120_1_range_1_shunt_1_0_capID_0_linearized");
  TGraphErrors * g6 = (TGraphErrors*) _file->Get("LinadcVsCharge/ADCvsfC_120_1_range_1_shunt_1_0_capID_1_linearized");
  TGraphErrors * g7 = (TGraphErrors*) _file->Get("LinadcVsCharge/ADCvsfC_120_1_range_1_shunt_1_0_capID_2_linearized");
  TGraphErrors * g8 = (TGraphErrors*) _file->Get("LinadcVsCharge/ADCvsfC_120_1_range_1_shunt_1_0_capID_3_linearized");
  TGraphErrors * g1shunt =(TGraphErrors*)  _file->Get("Shunted_LinadcVsCharge/ADCvsfC_120_1_range_0_shunt_6_0_capID_0_linearized");
  TGraphErrors * g2shunt =(TGraphErrors*)  _file->Get("Shunted_LinadcVsCharge/ADCvsfC_120_1_range_0_shunt_6_0_capID_1_linearized");
  TGraphErrors * g3shunt =(TGraphErrors*)  _file->Get("Shunted_LinadcVsCharge/ADCvsfC_120_1_range_0_shunt_6_0_capID_2_linearized");
  TGraphErrors * g4shunt =(TGraphErrors*)  _file->Get("Shunted_LinadcVsCharge/ADCvsfC_120_1_range_0_shunt_6_0_capID_3_linearized");

  TGraphErrors * g5shunt =(TGraphErrors*)  _file->Get("Shunted_LinadcVsCharge/ADCvsfC_120_1_range_1_shunt_6_0_capID_0_linearized");
  TGraphErrors * g6shunt =(TGraphErrors*)  _file->Get("Shunted_LinadcVsCharge/ADCvsfC_120_1_range_1_shunt_6_0_capID_1_linearized");
  TGraphErrors * g7shunt =(TGraphErrors*)  _file->Get("Shunted_LinadcVsCharge/ADCvsfC_120_1_range_1_shunt_6_0_capID_2_linearized");
  TGraphErrors * g8shunt =(TGraphErrors*)  _file->Get("Shunted_LinadcVsCharge/ADCvsfC_120_1_range_1_shunt_6_0_capID_3_linearized");

  std::cout << "before linear fit" << std::endl;
  TF1 *pol1 = new TF1("pol1","pol1",200,600);
  g1->Fit("pol1","R");
  g2->Fit("pol1","R");
  g3->Fit("pol1","R");
  g4->Fit("pol1","R");
  g5->Fit("pol1","0");
  g6->Fit("pol1","0");
  g7->Fit("pol1","0");
  g8->Fit("pol1","0");
  std::cout << "before get parameters" << std::endl;
  double offset1 = 0.0; //g1->GetFunction("pol1")->GetParameter(0);
  double offset2 = 0.0; //g2->GetFunction("pol1")->GetParameter(0);
  double offset3 = 0.0; //g3->GetFunction("pol1")->GetParameter(0);
  double offset4 = 0.0; //g4->GetFunction("pol1")->GetParameter(0);
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
  std::cout << offset1 << std::endl;
  // Define functions with slopes/offsets hardcoded in for testing purposes
//   TF1 * f1 = new TF1("fit1","[0]*(7.58965106426878929e-03+3.06953080266622103e-01*x)",0,100);
//   TF1 * f2 = new TF1("fit2","[0]*(9.82985765887945534e-04+3.06370846586603629e-01*x)",0,100);
//   TF1 * f3 = new TF1("fit3","[0]*(4.02000870236074708e-03+3.06782271158457964e-01*x)",0,100);
//   TF1 * f4 = new TF1("fit4","[0]*(1.60261147360417737e-02+3.06135228229022671e-01*x)",0,100);


  // define functions with slopes and offsets as additional parameters, these can then be set and fixed (not fit)
  TF1 * f1 = new TF1("fit1","[0]*([1]+[2]*x)",0,100);
  TF1 * f2 = new TF1("fit2","[0]*([1]+[2]*x)",0,100);
  TF1 * f3 = new TF1("fit3","[0]*([1]+[2]*x)",0,100);
  TF1 * f4 = new TF1("fit4","[0]*([1]+[2]*x)",0,100);
  TF1 * f5 = new TF1("fit5","[0]*([1]+[2]*x)",0,100);
  TF1 * f6 = new TF1("fit6","[0]*([1]+[2]*x)",0,100);
  TF1 * f7 = new TF1("fit7","[0]*([1]+[2]*x)",0,100);
  TF1 * f8 = new TF1("fit8","[0]*([1]+[2]*x)",0,100);

  // perform now global fit
  //cout << "HERE" << endl;


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
  range.SetRange(0,9e9);
  std::cout << "HERE" << std::endl;


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
  result.Print(std::cout);
  
  TCanvas * c1 = new TCanvas("Simfit","Simultaneous fit of 8 graphs",700,700);
  c1->Divide(2,4);
  c1->cd(1);
  gStyle->SetOptFit(1111);
  
  f1->SetFitResult(result, ipar1);
  f1->SetRange(range().first, range().second);   
  f1->SetLineColor(kRed);
  g1shunt->GetListOfFunctions()->Add(f1);
  g1shunt->Draw("alp"); 

  c1->cd(2);
  f2->SetFitResult(result, ipar2);
  f2->SetRange(range().first, range().second);
  f2->SetLineColor(kRed);
  g2shunt->GetListOfFunctions()->Add(f2);
  g2shunt->Draw("alp");

  c1->cd(3);
  f3->SetFitResult(result, ipar3);
  f3->SetRange(range().first, range().second);
  f3->SetLineColor(kRed);
  g3shunt->GetListOfFunctions()->Add(f3);
  g3shunt->Draw("alp");

  c1->cd(4);
  f4->SetFitResult(result, ipar4);
  f4->SetRange(range().first, range().second);
  f4->SetLineColor(kRed);
  g4shunt->GetListOfFunctions()->Add(f4);
  g4shunt->Draw("alp");
  
  c1->cd(5);
  f5->SetFitResult(result, ipar5);
  f5->SetRange(range().first, range().second);
  f5->SetLineColor(kRed);
  g5shunt->GetListOfFunctions()->Add(f5);
  g5shunt->Draw("alp"); 

  c1->cd(6);
  f6->SetFitResult(result, ipar6);
  f6->SetRange(range().first, range().second);
  f6->SetLineColor(kRed);
  g6shunt->GetListOfFunctions()->Add(f6);
  g6shunt->Draw("alp");

  c1->cd(7);
  f7->SetFitResult(result, ipar7);
  f7->SetRange(range().first, range().second);
  f7->SetLineColor(kRed);
  g7shunt->GetListOfFunctions()->Add(f7);
  g7shunt->Draw("alp");

  c1->cd(8);
  f8->SetFitResult(result, ipar8);
  f8->SetRange(range().first, range().second);
  f8->SetLineColor(kRed);
  g8shunt->GetListOfFunctions()->Add(f8);
  g8shunt->Draw("alp");


  c1->SaveAs("qie1_0x86000000_0xead65570_method2.pdf");
}
