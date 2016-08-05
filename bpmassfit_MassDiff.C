using namespace RooFit ;

void bpmassfit_MassDiff(char FileName[128]) 
{            
  
  TFile * myhbk= new TFile("myhbkBpmassfitsPlot_2011_noKaonTrackRefit.root","recreate");
  float JpsiPhiKMassmin=5.15, JpsiPhiKMassmax=5.45;

  RooRealVar varJpsiPhiKMass("varJpsiPhiKMass", "m(J/#\psi#phiK^{+}) GeV", JpsiPhiKMassmin,  JpsiPhiKMassmax) ;
  RooRealVar varJpsiPhiMass("varJpsiPhiMass", "m(J/#\psi#phi) GeV", 4.1047,  4.9047) ; 
  RooRealVar varKaon1Pt("Kaon1Pt","Kaon1Pt",1.5,99999.);
  RooRealVar varKaon2Pt("Kaon2Pt","Kaon2Pt",1.5,99999.);
  RooRealVar varKaon3Pt("Kaon3Pt","Kaon3Pt",1.5,99999.);
  RooRealVar varMuon1Pt("Muon1Pt","Muon1Pt",4.,99999.);
  RooRealVar varMuon2Pt("Muon2Pt","Muon2Pt",4.,99999.);
  RooRealVar varJpsiPt("varJpsiPt","varJpsiPt",7.,99999.);
  RooRealVar varEtaB("EtaB", "EtaB", 0., 999.);


  RooRealVar   Bp_peak  ("Bp_peak"    ,"Bp_peak"  ,5.2789, 5.26, 5.3 ); //org
  RooRealVar   Bp_width ("Bp_width"    ,"Bp_width"  ,0.0086181, 0.001, 0.1 ); //org
  
  RooAbsPdf* pdfBp = new RooGaussian( "pdfBp", "pdfBp",  varJpsiPhiKMass, Bp_peak ,Bp_width ) ;
  RooRealVar nSigBp ("nSigBp", "Number of signal 1 candidates ", 100,  -10.0, 1000000.0); 

  //Bp_peak.setConstant();  //Fix B mass
  //nSigBp.setConstant(); 
  //Bp_width.setConstant();    
 
  RooRealVar c1("c1", "c1", -4.66666e-02,  -10.0, 10.0); //org
  RooRealVar c2("c2", "c2", -3.54591e-01,  -10., 1.0); //org
  RooAbsPdf *  BkgPolPdf = new RooChebychev("BkgPolPdf","BkgPolPdf",varJpsiPhiKMass,RooArgSet(c1,c2));
  
  RooRealVar nBckPol("nBckPol", "Number of signal 2 candidates ", 10000,  0.0, 9000000.0);

  RooExtendPdf *  extendpdfSigBp = new RooExtendPdf("extendpdfSigBp","Signal 1 PDF",*pdfBp, nSigBp);
  RooExtendPdf *  extendpdfBkgPol = new RooExtendPdf("extendpdfBkgPol","Signal 1 PDF",*BkgPolPdf, nBckPol);

  RooAddPdf mytotalPdf("mytotPdf", "mytotPdf", RooArgList(*extendpdfSigBp, *extendpdfBkgPol), RooArgList(nSigBp,nBckPol) ) ;
  RooDataSet * dataSet= &(RooDataSet::read(FileName,RooArgSet(varJpsiPhiKMass, varKaon1Pt, varKaon2Pt, varKaon3Pt),"Q"));



  myfitresult= mytotalPdf.fitTo(*dataSet,"mer");  
 
  gROOT->SetStyle("Plain");  
  TCanvas * c=new TCanvas("c","c",800,600);
  RooPlot *frame = varJpsiPhiKMass.frame(60);
  dataSet->plotOn(frame);  
  mytotalPdf.plotOn(frame, Components(RooArgSet(*extendpdfBkgPol)),LineStyle(kDashed),LineColor(kBlue),Range(JpsiPhiKMassmin,JpsiPhiKMassmax) );
  mytotalPdf.paramOn(frame, Format("NE",FixedPrecision(5)));
  mytotalPdf.plotOn(frame);

varJpsiPhiKMass.setRange("selection",JpsiPhiKMassmin,JpsiPhiKMassmax);
  RooAbsReal*  pdfBptotal=pdfBp.createIntegral(RooArgSet(varJpsiPhiKMass),"selection");
  RooAbsReal* BkgPolPdftotal=BkgPolPdf.createIntegral(RooArgSet(varJpsiPhiKMass),"selection");

  frame->SetTitle("");  
  frame->GetXaxis()->SetTitleSize(0.05);
  frame->GetXaxis()->SetLabelSize(0.045);
  frame->GetXaxis()->SetTitleOffset(0.85);
  frame->GetYaxis()->SetTitleSize(0.05);
  frame->GetYaxis()->SetTitle ("Candidates / 0.005 GeV");
  frame->GetYaxis()->SetTitleOffset(0.85);
  frame->SetMarkerColor(1);
  frame->SetMarkerSize(2.0);
  frame->Draw();
   
  double myBGausSigma = Bp_width.getVal();
/*  varJpsiPhiKMass.setRange("selectioan1",5.279-3.0*myBGausSigma, 5.279+3.0*myBGausSigma);
 *    RooAbsReal*  pdfBpsignalregion=pdfBp->createIntegral(RooArgSet(varJpsiPhiKMass),"selection1");
 *      RooAbsReal* BkgPolPdfsignalregion=BkgPolPdf->createIntegral(RooArgSet(varJpsiPhiKMass),"selection1");
 *      */
  varJpsiPhiKMass.setRange("selection2",5.279-1.5*myBGausSigma, 5.279+1.5*myBGausSigma);
  RooAbsReal*  pdfBpsignalregion2=pdfBp->createIntegral(RooArgSet(varJpsiPhiKMass),"selection2");
  RooAbsReal* BkgPolPdfsignalregion2=BkgPolPdf->createIntegral(RooArgSet(varJpsiPhiKMass),"selection2");

 // double myBration=pdfBpsignalregion->getVal()/pdfBptotal->getVal();
 // double myBckration=BkgPolPdfsignalregion->getVal()/BkgPolPdftotal->getVal();
  double myBration2=pdfBpsignalregion2->getVal()/pdfBptotal->getVal();
   double myBckration2=BkgPolPdfsignalregion2->getVal()/BkgPolPdftotal->getVal();

    double Ratio1p5sigma1 = (myBration2*nSigBp.getVal())/(myBckration2*nBckPol.getVal()+myBration2*nSigBp.getVal()) ;
//      double Ratio1p5sigma2 = (myBration2*nSigBp.getVal())/sqrt((myBckration2*nBckPol.getVal()+myBration2*nSigBp.getVal())) ;
//        //double Ratio3sigma = (myBration*nSigBp.getVal())/(myBckration*nBckPol.getVal() + myBration*nSigBp.getVal());
//
//          TLatex *t = new TLatex();
//            t->SetNDC();
//              t->SetTextColor(kBlack);
//                t->SetTextSize(0.04);
//                  t->SetTextAlign(12);
//                    char type[128];
//                      t->SetTextFont(42);
//                        char num1[128];
//                          char num2[128];
//
//                            sprintf(num1, "#frac{S}{S+B} (#pm 1.5 #sigma) =  %.2f",Ratio1p5sigma1);
//                              sprintf(num2, "#frac{S}{#sqrt{S+B}} (#pm 1.5 #sigma) =  %.2f",Ratio1p5sigma2);
//                                //t->DrawLatex(0.2, 0.85, num2);
//                                  //t->DrawLatex(0.2, 0.65, num1);*/
//
                                  cout << Ratio1p5sigma1 << endl;


}

