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


struct GlobalChi2 {
  GlobalChi2(  ROOT::Math::IMultiGenFunction & f1,
	       ROOT::Math::IMultiGenFunction & f2,
	       ROOT::Math::IMultiGenFunction & f3,
	       ROOT::Math::IMultiGenFunction & f4) :
    fChi2_1(&f1), fChi2_2(&f2),fChi2_3(&f3), fChi2_4(&f4) {}

  // parameter vector is first background (in common 1 and 2)
  // and then is signal (only in 2)
  double operator() (const double *par) const {
    double p1[3];
    double p2[3];
    double p3[3];
    double p4[3];
    for (int i = 0; i < 3; ++i) {
      p1[i] = par[ipar1[i] ];
      p2[i] = par[ipar2[i] ];
      p3[i] = par[ipar3[i] ];
      p4[i] = par[ipar4[i] ];
    }


    return (*fChi2_1)(p1) + (*fChi2_2)(p2) + (*fChi2_3)(p3) + (*fChi2_4)(p4);
  }

  const  ROOT::Math::IMultiGenFunction * fChi2_1;
  const  ROOT::Math::IMultiGenFunction * fChi2_2;
  const  ROOT::Math::IMultiGenFunction * fChi2_3;
  const  ROOT::Math::IMultiGenFunction * fChi2_4;
};

void makeFits() {

  TFile* _file = TFile::Open("testGraphs.root","READ");

  TGraphErrors * g1 = (TGraphErrors*) _file->Get("ADCvsfC_132_1_range_0_shunt_1_0_capID_0_linearized");
  TGraphErrors * g2 = (TGraphErrors*) _file->Get("ADCvsfC_132_1_range_0_shunt_1_0_capID_1_linearized");
  TGraphErrors * g3 = (TGraphErrors*) _file->Get("ADCvsfC_132_1_range_0_shunt_1_0_capID_2_linearized");
  TGraphErrors * g4 = (TGraphErrors*) _file->Get("ADCvsfC_132_1_range_0_shunt_1_0_capID_3_linearized");

  TGraphErrors * g1shunt =(TGraphErrors*)  _file->Get("ADCvsfC_132_1_range_0_shunt_6_0_capID_0_linearized");
  TGraphErrors * g2shunt =(TGraphErrors*)  _file->Get("ADCvsfC_132_1_range_0_shunt_6_0_capID_1_linearized");
  TGraphErrors * g3shunt =(TGraphErrors*)  _file->Get("ADCvsfC_132_1_range_0_shunt_6_0_capID_2_linearized");
  TGraphErrors * g4shunt =(TGraphErrors*)  _file->Get("ADCvsfC_132_1_range_0_shunt_6_0_capID_3_linearized");

  double offset1 = g1->GetFunction("pol1")->GetParameter(0);
  double offset2 = g2->GetFunction("pol1")->GetParameter(0);
  double offset3 = g3->GetFunction("pol1")->GetParameter(0);
  double offset4 = g4->GetFunction("pol1")->GetParameter(0);
  double slope1 = g1->GetFunction("pol1")->GetParameter(1);
  double slope2 = g2->GetFunction("pol1")->GetParameter(1);
  double slope3 = g3->GetFunction("pol1")->GetParameter(1);
  double slope4 = g4->GetFunction("pol1")->GetParameter(1);

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


  // perform now global fit
  //cout << "HERE" << endl;


  ROOT::Math::WrappedMultiTF1 wf1(*f1,1);
  ROOT::Math::WrappedMultiTF1 wf2(*f2,1);
  ROOT::Math::WrappedMultiTF1 wf3(*f3,1);
  ROOT::Math::WrappedMultiTF1 wf4(*f4,1);

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

  ROOT::Fit::Chi2Function chi2_1(data1, wf1);
  ROOT::Fit::Chi2Function chi2_2(data2, wf2);
  ROOT::Fit::Chi2Function chi2_3(data3, wf3);
  ROOT::Fit::Chi2Function chi2_4(data4, wf4);
  std::cout << "HERE" << std::endl;


  GlobalChi2 globalChi2(chi2_1, chi2_2, chi2_3, chi2_4);

  ROOT::Fit::Fitter fitter;
  std::cout << "HERE" << std::endl;


  const int Npar = 9;
  double par0[Npar] = { 6, 
			offset1, slope1,
			offset2, slope2,
			offset3, slope3,
			offset4, slope4};
//  std::cout << "HERE" << std::endl;


  // create before the parameter settings in order to fix or set range on them
  fitter.Config().SetParamsSettings(9,par0);
  fitter.Config().ParSettings(1).Fix();
  fitter.Config().ParSettings(2).Fix();
  fitter.Config().ParSettings(3).Fix();
  fitter.Config().ParSettings(4).Fix();
  fitter.Config().ParSettings(5).Fix();
  fitter.Config().ParSettings(6).Fix();
  fitter.Config().ParSettings(7).Fix();
  fitter.Config().ParSettings(8).Fix();

 // cout << "HERE2" << endl;

  fitter.Config().MinimizerOptions().SetPrintLevel(0);
  fitter.Config().SetMinimizer("Minuit2","Migrad");
 // cout << "HERE2" << endl;

  // fit FCN function directly
  // (specify optionally data size and flag to indicate that is a chi2 fit)
 // cout << "HERE2" << endl;
  fitter.FitFCN(9,globalChi2,0,data1.Size()+data2.Size()+data3.Size()+data4.Size(),true);
  ROOT::Fit::FitResult result = fitter.Result();
  result.Print(std::cout);
  //std::cout<< result.Parameter(0), result.Parameter(2) <<std::endl;
 // cout << "HERE2" << endl;
  TCanvas * c1 = new TCanvas("Simfit","Simultaneous fit of 4 graphs",700,700);
  //TCanvas * c1 = new TCanvas("Simultaneous fit");
  c1->Divide(1,4);
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

  c1->SaveAs("trial_simult.pdf");
}
