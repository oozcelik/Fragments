//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Mon Nov 14 13:23:00 2016 by ROOT version 5.34/18
// from TTree X_data/X(3872) Data
// found on file: MuOniaRun2012_JPsiKKKPAT_ntpl_998_1_F78.root
//////////////////////////////////////////////////////////

#ifndef _JPsiKKKPATRunII_h
#define _JPsiKKKPATRunII_h

#include <memory>
#include "../interface/VertexReProducer.h"
#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include "DataFormats/PatCandidates/interface/GenericParticle.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "DataFormats/Common/interface/Handle.h"
// Header file for the classes stored in the TTree if any.
#include <vector>
#include <vector>
#include <vector>
#include <vector>
#include <vector>
#include <vector>
#include "TFile.h"
#include "TTree.h"
#include <string>
// Fixed size dimensions of array or collections stored in the TTree if any.

using std::vector;
using namespace edm;
using namespace reco;
using namespace std;


class JPsiKKKPATRunII : public EDAnalyzer{
public :
  explicit JPsiKKKPATRunII(const ParameterSet&);
  ~JPsiKKKPATRunII();

private:
  virtual void beginJob() ;
  virtual void beginRun(Run const & iRun, EventSetup const& iSetup);
  virtual void analyze(const Event&, const EventSetup&);
  virtual void endJob() ;

   // Declaration of leaf types
//   InputTag hlTriggerResults_;
  edm::EDGetTokenT<edm::TriggerResults> hlTriggerResults_;
   string genParticles_;
   string vtxSample;
  edm::EDGetTokenT<edm::View<pat::Muon>>MuonType;
  edm::EDGetTokenT<std::vector<pat::GenericParticle>>tracks_; 
 //  InputTag MuonType;
   vector<unsigned int> *TrigRes;
   vector<string>  *TrigNames;
   vector<string>  *MatchTriggerNames;
   vector<unsigned int> *L1TrigRes;
   TTree* X_One_Tree_;
  vector<std::string>* trigNames;
   UInt_t          runNum;
   UInt_t          evtNum;
   UInt_t          lumiNum;
   Float_t         priVtxX;
   Float_t         priVtxY;
   Float_t         priVtxZ;
   Float_t         priVtxXE;
   Float_t         priVtxYE;
   Float_t         priVtxZE;
   Float_t         priVtxChiNorm;
   Float_t         priVtxChi;
   Float_t         priVtxCL;
   UInt_t          nMu;
  vector<float>       *trPx;
  vector<float>       *trPy;
  vector<float>       *trPz;
  vector<float>       *trE;
   vector<double>  *muPx;
   vector<double>  *muPy;
   vector<double>  *muPz;
   vector<double>  *muD0;
   vector<float>   *muD0E;
   vector<float>   *cosAlpha;
   vector<float>   *mumuVtxCL;
   vector<float>   *mumuFLSig;
   vector<float>   *mumurVtxMag2D;
   vector<float>   *mumusigmaRvtxMag2D;
   vector<float>   *muDz;
   vector<float>   *muChi2;
   vector<int>     *muNDF;
   vector<int>     *muPhits;
   vector<int>     *muShits;
   vector<float>   *muGlChi2;
   vector<int>     *muGlNDF;
   vector<int>     *muGlMuHits;
   vector<int>     *muType;
   vector<int>     *muQual;
   vector<int>     *muTrack;
   vector<float>   *muCharge;
   vector<float>   *mufHits;
   vector<bool>    *muFirstBarrel;
   vector<bool>    *muFirstEndCap;
   vector<float>   *muDzVtx;
   vector<float>   *muDxyVtx;
   vector<int>     *ThreeGoodTracks;
   vector<int>     *trackQuality;
   vector<float>   *TrackPx;
   vector<float>   *TrackPy;
   vector<float>   *TrackPz;
   vector<float>   *TrackEnergy;
   vector<int>     *TrackNDF;
   vector<int>     *TrackPhits;
   vector<int>     *TrackShits;
   vector<float>   *TrackChi2;
   vector<float>   *TrackD0;
   vector<float>   *TrackD0Err;
   vector<float>   *TrackCharge;
   vector<float>   *trfHits;
   vector<bool>    *trFirstBarrel;
   vector<bool>    *trFirstEndCap;
   vector<float>   *trDzVtx;
   vector<float>   *trDxyVtx;
   vector<float>   *trVx;
   vector<float>   *trVy;
   vector<double>  *tr_nsigdedx;
   vector<float>   *tr_dedx;
   vector<float>   *tr_dedxMass;
   vector<float>   *tr_theo;
   vector<float>   *tr_sigma;
   UInt_t          nX;
   UInt_t          nK;
   UInt_t          nMC;
   UInt_t          nJPsi;
   UInt_t          MCnX;
   vector<float>   *xMass;
   vector<float>   *xVtxCL;
   vector<float>   *xVtxC2;
   vector<float>   *PsiTwoSMass;
   vector<float>   *SecondPairMass;
   vector<float>   *BsMass;
   vector<float>   *BsVtxCL;
   vector<float>   *BsVtxC2;
   vector<double>  *xPx;
   vector<double>  *xPy;
   vector<double>  *xPz;
   vector<double>  *xPxE;
   vector<double>  *xPyE;
   vector<double>  *xPzE;
   vector<float>   *xDecayVtxX;
   vector<float>   *xDecayVtxY;
   vector<float>   *xDecayVtxZ;
   vector<double>  *xDecayVtxXE;
   vector<double>  *xDecayVtxYE;
   vector<double>  *xDecayVtxZE;
   vector<float>   *PriVtxXCorrX;
   vector<float>   *PriVtxXCorrY;
   vector<float>   *PriVtxXCorrZ;
   vector<double>  *PriVtxXCorrEX;
   vector<double>  *PriVtxXCorrEY;
   vector<double>  *PriVtxXCorrEZ;
   vector<float>   *PriVtxXCorrC2;
   vector<float>   *PriVtxXCorrCL;
   vector<float>   *MyPriVtxX;
   vector<float>   *MyPriVtxY;
   vector<float>   *MyPriVtxZ;
   vector<float>   *MyPriVtxXE;
   vector<float>   *MyPriVtxYE;
   vector<float>   *MyPriVtxZE;
   vector<float>   *MyPriVtxChiNorm;
   vector<float>   *MyPriVtxChi;
   vector<float>   *MyPriVtxCL;
   vector<double>  *xLxyPV;
   vector<double>  *xLxyPVE;
   vector<double>  *xCosAlpha;
   vector<double>  *xCTauPV;
   vector<double>  *xCTauPVE;
   vector<double>  *xLxyBS;
   vector<double>  *xLxyBSE;
   vector<double>  *xExtraTrkabsDxywrtXvtxmin;
   vector<double>  *xExtraTrkabsDxywrtXvtxminMaxDz0dot5cm;
   vector<double>  *xExtraTrkabsDxywrtXvtxminMaxDz1dot0cm;
   vector<double>  *xExtraTrkabsDxywrtXvtxminMaxDz1dot5cm;
   vector<double>  *xExtraTrkabsDxywrtXvtxminMaxDz2dot0cm;
   vector<double>  *xExtraTrkabsDxywrtXvtxminMaxDz3dot0cm;
   vector<double>  *xExtraTrkabsDxywrtXvtxminMaxDz4dot0cm;
   vector<double>  *xExtraTrkabsDxywrtXvtxminMaxDz5dot0cm;
   vector<double>  *xExtraTrkabsDxywrtXvtxminMaxDz0dot1cm;
   vector<double>  *xExtraTrkabsDxywrtXvtxminMaxDz0dot05cm;
   vector<double>  *xExtraTrkabsDxywrtXvtxminMaxDz0dot04cm;
   vector<double>  *xExtraTrkabsDxywrtXvtxminMaxDz0dot03cm;
   vector<double>  *xExtraTrkabsDxywrtXvtxminMaxDz0dot02cm;
   vector<double>  *xExtraTrkabsDxywrtXvtxminMaxDz0dot01cm;
   vector<double>  *xCosAlphaBS;
   vector<double>  *xCTauBS;
   vector<double>  *xCTauBSE;
   vector<int>     *JPsiIndex;
   vector<int>     *pipIndex;
   vector<int>     *pimIndex;
   vector<int>     *pi3rdIndex;
   vector<float>   *fitpi1Px;
   vector<float>   *fitpi1Py;
   vector<float>   *fitpi1Pz;
   vector<float>   *fitpi1E;
   vector<float>   *fitpi2Px;
   vector<float>   *fitpi2Py;
   vector<float>   *fitpi2Pz;
   vector<float>   *fitpi2E;
   vector<float>   *fitpi3Px;
   vector<float>   *fitpi3Py;
   vector<float>   *fitpi3Pz;
   vector<float>   *fitpi3E;
   vector<float>   *fitmu1Px;
   vector<float>   *fitmu1Py;
   vector<float>   *fitmu1Pz;
   vector<float>   *fitmu1E;
   vector<float>   *fitmu2Px;
   vector<float>   *fitmu2Py;
   vector<float>   *fitmu2Pz;
   vector<float>   *fitmu2E;
   UInt_t          nJ;
   vector<float>   *JMass;
   vector<float>   *JVtxCL;
   vector<float>   *JVtxC2;
   vector<float>   *JPx;
   vector<float>   *JPy;
   vector<float>   *JPz;
   vector<float>   *JDecayVtxX;
   vector<float>   *JDecayVtxY;
   vector<float>   *JDecayVtxZ;
   vector<float>   *JDecayVtxXE;
   vector<float>   *JDecayVtxYE;
   vector<float>   *JDecayVtxZE;
   vector<int>     *mupIdx;
   vector<int>     *mumIdx;
   vector<float>   *mumPx;
   vector<float>   *mumPy;
   vector<float>   *mumPz;
   vector<float>   *mupPx;
   vector<float>   *mupPy;
   vector<float>   *mupPz;
   vector<float>   *mumfChi2;
   vector<int>     *mumfNDF;
   vector<float>   *mupfChi2;
   vector<int>     *mupfNDF;
   vector<bool>    *JPsiMuonTrigMatch;
   vector<bool>    *mupTrigMatch;
   vector<bool>    *mumTrigMatch;
   vector<float>   *MCPdgId;
   vector<float>   *MCDauphi_Pt;
   vector<float>   *phiind;
   vector<float>   *psiind;
   vector<float>   *kaonind;
   vector<float>   *MCDauphi_mass;
   vector<float>   *MCDauphi_Px;
   vector<float>   *MCDauphi_Py;
   vector<float>   *MCDauphi_Pz;
   vector<float>   *MCDauphi_E;
   vector<float>   *BDauIdx;
   vector<float>   *MCDauJpsi_Pt;
   vector<float>   *MCDauJpsi_Px;
   vector<float>   *MCDauJpsi_Py;
   vector<float>   *MCDauJpsi_Pz;
   vector<float>   *MCDauJpsi_mass;
   vector<float>   *MCDauJpsi_E;
   vector<float>   *MCDauK_Pt;
   vector<float>   *MCDauK_Px;
   vector<float>   *MCDauK_Py;
   vector<float>   *MCDauK_Pz;
   vector<float>   *MCDauK_mass;
   vector<float>   *MCDauK_E;
   vector<float>   *MCmass;
   vector<float>   *MCPx;
   vector<float>   *MCPy;
   vector<float>   *MCPz;
   vector<float>   *MCPt;
   vector<float>   *MCE;
   vector<float>   *MCJidx;
   vector<float>   *MCPhidx;
   vector<float>   *MCKidx;
   vector<float>   *MCBIdx;
   vector<float>   *MCStatus;

};

#endif

