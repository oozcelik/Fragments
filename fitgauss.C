#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "TColor.h"
#include "TCanvas.h"
#include "TTree.h"
#include "TH1D.h"
#include "TH1F.h"
#include "TRandom.h"
#include "TGraph.h"
#include <TH2.h>
#include <fstream>

using namespace RooFit ;
using namespace std;

void fitgauss()
{
    std::ofstream myoutfile("abseff.txt");
    TH2F *h2= new TH2F("","", 40,16.85,23.85, 20,2.,5.);
    //TH2F *hNew1 = new TH2F("","",20,16.85,23.85,20,2.,5.);
    TFile * f1=TFile::Open("OffMCPhSpAllwNoCut.root");
    f1->cd();
    TH2F * hNew;
    hNew = (TH2F*)f1->Get("myDalitz_Gen");
    TH2F *hist_new=(TH2F*)hNew->Clone();
    TFile * f2=TFile::Open("OffMCPhSpAllwPurityCuts.root");
    f2->cd();
    TH2F * hNew1;
    hNew1 = (TH2F*)f2->Get("myDalitz_Rec");
    TH2F *hist_new1=(TH2F*)hNew1->Clone();
    hist_new->SetTitle("Gen before trigger selection");
    hist_new1->SetTitle("Reco w/cut-based selections");
//    h2->SetTitle("Reco over gen");
    h2->SetTitle("Relative Efficiency");
    h2->SetXTitle("m^{2} (J/#psi#phi) (GeV^{2}/c^{4})");
    h2->SetYTitle("m^{2} (#phiK^{+}) (GeV^{2}/c^{4})");

    hist_new1->RebinX(8,"");
    hist_new1->RebinY(8,"");

    hist_new->RebinX(8,"");
    hist_new->RebinY(8,"");


    const Int_t NRGBs = 7, NCont = 25;
    gStyle->SetNumberContours(NCont);
    Double_t red[NRGBs]   = { 0.90, 0.60, 0.30, 0.20, 0.0, 0.97, 1.0 };
    Double_t green[NRGBs] = { 0.90, 0.60, 0.40, 0.25, 0.30, 0.0, 1.00 };
    Double_t blue[NRGBs]  = { 0.97, 0.90, 0.95, 0.95, 0.97, 0.37, 0.00 };
    TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);

    // Dalitz contour
    Int_t m = 19800;
    Double_t x[19800], m23_max[19800], m23_min[19800];
    Double_t E2[19800], E3[19800];

    Double_t m_mother = 5.279;
    Double_t m_dau1 = 0.493, m_dau2 = 1.019, m_dau3 = 3.0967 ;

    Double_t m12_min = (m_dau1+m_dau2)*(m_dau1+m_dau2);
    Double_t m12_max = (m_mother-m_dau3)*(m_mother-m_dau3);
    Double_t step = (m12_max - m12_min)/(m-1);

    x[0] = m12_min + 0.00001;

    Int_t binx = hist_new1->GetXaxis()->GetNbins(); // 320
    Int_t biny = hist_new1->GetYaxis()->GetNbins(); // 160
    Int_t bin = hist_new1->GetBin(binx,biny); // 51840



    for (Int_t k=1; k<m; k++ )
        x[k] = x[k-1] + step;



    Int_t n = 19799;
    for (Int_t i=0; i<n; i++)
    {
        E2[i] = (x[i] - m_dau1*m_dau1 + m_dau2*m_dau2)/(2*sqrt(x[i]));
        E3[i] = (m_mother*m_mother - x[i] - m_dau3*m_dau3)/(2*sqrt(x[i]));
        m23_min[i] = (E2[i]+E3[i])*(E2[i]+E3[i]) - TMath::Power((sqrt(E2[i]*E2[i] - m_dau2*m_dau2) + sqrt(E3[i]*E3[i] - m_dau3*m_dau3)),2)+0.06;
        m23_max[i] = (E2[i]+E3[i])*(E2[i]+E3[i]) - TMath::Power((sqrt(E2[i]*E2[i] - m_dau2*m_dau2) - sqrt(E3[i]*E3[i] - m_dau3*m_dau3)),2);
    }


    TGraph *cont_up = new TGraph(n,m23_min, x);
    cont_up->SetLineWidth(2); //cont_up->SetLineColor(kRed);
    TGraph *cont_down = new TGraph(n,m23_max, x);
    cont_down->SetLineWidth(2); //cont_down->SetLineColor(kRed);



    TCutG *mycutup = new TCutG("mycutup",n);
    TCutG *mycutdown = new TCutG("mycutdown",n);


    int downBin = cont_down->GetN();
    int upBin = cont_up->GetN();

    float avg=0.;
    float content;
    float sigma, error;

    TH1F *h1 = new TH1F(" ", "Spectrum of the values of the absEff efficiency ", 1000, -0.001, 0.006);
    h1->GetXaxis()->SetTitle("Abs eff");
    h1->GetYaxis()->SetTitle("#bins");
    h1->SetMarkerStyle(1);

    int rebin=0;

    for(int l=0; l<bin; l++)
    {
        content = hist_new1->GetBinContent(l)/hist_new->GetBinContent(l);
        if ( (hist_new1->GetBinContent(l)==0)  ||  (hist_new->GetBinContent(l)==0) || hist_new->GetBinContent(l)<500 || hist_new1->GetBinContent(l)==1) continue;
        avg+=content;
        myoutfile << content << " " << hist_new1->GetBinContent(l) << " " << hist_new->GetBinContent(l) << endl;
        rebin++;
    }

    float  mean= avg/rebin;

    cout << " Avarage mean value of absolute eff: "  << mean << endl;


    Float_t xminh2  = cont_up->GetXaxis()->GetXmin();
    Float_t xmaxh2  = cont_up->GetXaxis()->GetXmax();
    Float_t yminh2  = cont_up->GetYaxis()->GetXmin();
    Float_t ymaxh2  = cont_up->GetYaxis()->GetXmax();

    Float_t xmind  = cont_down->GetXaxis()->GetXmin();
    Float_t xmaxd  = cont_down->GetXaxis()->GetXmax();
    Float_t ymind  = cont_down->GetYaxis()->GetXmin();
    Float_t ymaxd  = cont_down->GetYaxis()->GetXmax();

    Double_t ax[19800];
    Double_t ay[19800];
    Double_t bx[19800];
    Double_t by[19800];

    Double_t  xcontent;
    Double_t xlow, ylow, x2, y2;
    Double_t nevnts;
    int aaa=0;

    for (int k=1; k<downBin+1; k++)
    {

        cont_down->GetPoint(k,ax[k], ay[k]); // m23_max
        cont_up->GetPoint(k,bx[k], by[k]);  // m23_min
        mycutup->SetPoint(k, ax[k], ay[k]);
        mycutdown->SetPoint(k, bx[k], by[k]);
    }



    for (int t =0; t < binx; t++)
    {
        xlow = hist_new1->GetXaxis()->GetBinUpEdge(t+1);
        x2 = hist_new->GetXaxis()->GetBinUpEdge(t+1);


        for (int z =0; z< biny; z++)
        {
            ylow = hist_new1->GetYaxis()->GetBinUpEdge(z+1);
            y2 = hist_new->GetYaxis()->GetBinUpEdge(z+1);

            bool DownIn = false;
            bool DownOut = false;
            bool UpIn = false;
            bool UpOut = false;

            int CutD = mycutdown->IsInside(xlow, ylow);
            int CutU = mycutup->IsInside(xlow, ylow);

            if( mycutdown->IsInside(xlow, ylow))  DownOut = true;
            else DownIn = true;

            if ( mycutup->IsInside(xlow, ylow))  UpIn = true;
            else UpOut = true;



            float absEff =  hist_new1->GetBinContent(t+1,z+1)/hist_new->GetBinContent(t+1,z+1);
            float relEff = absEff/0.000275786;            //8.31679e-05; //7.94668e-05;      //0.000275786;    //the number must be the closest bin content to the avarage of bin contents!
                if( hist_new->GetBinContent(t+1,z+1)==0 || hist_new1->GetBinContent(t+1,z+1)==0 || hist_new->GetBinContent(t+1,z+1)<500 || hist_new1->GetBinContent(t+1,z+1)==1)   continue;
//             h2->SetBinContent(t+1,z+1, absEff);
            h2->SetBinContent(t+1,z+1, relEff);
            h1->Fill(hist_new1->GetBinContent(t+1,z+1)/hist_new->GetBinContent(t+1,z+1));
        }
    }
    gStyle->SetOptStat(10);
    h2->SetLabelSize(0.03, "z");
    h2->GetZaxis()->SetRangeUser(0., 2.2);
    h2->Draw("colz");
    cont_up->Draw("lsame");
    cont_down->Draw("lsame");
    TCanvas * c=new TCanvas("c","c",600,600);
    //h1->SetStats(kFALSE);
    h1->Draw();

}
