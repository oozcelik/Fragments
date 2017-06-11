
#include "../interface/JPsiKKKPATRunII.h"
#include "../interface/VertexReProducer.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/PatCandidates/interface/GenericParticle.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "PhysicsTools/PatExamples/interface/PatMuonAnalyzer.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/PATObject.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include <vector>
#include <string>
#include "TFile.h"
#include "TTree.h"

JPsiKKKPATRunII::JPsiKKKPATRunII(const edm::ParameterSet & iConfig):
     hlTriggerResults_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("HLTriggerResults"))),
     //hlTriggerResults_(iConfig.getUntrackedParameter < edm::InputTag > ("HLTriggerResults",edm::InputTag("TriggerResults::HLT"))),
     genParticles_ ( iConfig.getUntrackedParameter<std::string>("GenParticles",std::string("genParticles")) ),
     vtxSample(iConfig.getUntrackedParameter < std::string > ("VtxSample", std::string("offlinePrimaryVertices"))),       
     MuonType(consumes<edm::View<pat::Muon>>(iConfig.getUntrackedParameter< edm::InputTag>("muons"))),
     tracks_(consumes<std::vector<pat::GenericParticle>>(iConfig.getParameter< edm::InputTag>("pattracks"))),

//      MuonType(iConfig.getParameter<edm::InputTag >("muons")),    

     X_One_Tree_(0),
     trigNames(0),
     runNum(0),
     evtNum(0),
     lumiNum(0),
     priVtxX(0),
     priVtxY(0),
     priVtxZ(0),
     priVtxXE(0),
     priVtxYE(0),
     priVtxZE(0),
    trPx(0),
     trPy(0),
     trPz(0),
     trE(0)
/*     muPx(0),
     muPy(0),
     muPz(0),
     muCharge(0)*/
{
}

JPsiKKKPATRunII::~JPsiKKKPATRunII()
{
    // do anything here that needs to be done at desctruction time
    //     // (e.g. close files, deallocate resources etc.)
         }
void JPsiKKKPATRunII::analyze(const edm::Event & evt, const edm::EventSetup & iSetup)
{
 
    using std::vector;
    using namespace edm;
    using namespace reco;
    using namespace std;

    runNum = evt.id().run();
    evtNum = evt.id().event();
    lumiNum = evt.id().luminosityBlock(); 


    // HLT information 
    edm::Handle<edm::TriggerResults> trigResults;
    evt.getByToken(hlTriggerResults_,trigResults);

//edm::InputTag&, edm::Handle<edm::TriggerResults>&

    const edm::TriggerNames& triggerNames_ = evt.triggerNames(*trigResults);   

    int ntrigs = trigResults->size();
   for (int itrig = 0; itrig < ntrigs; itrig++)
   {

     string trigName = triggerNames_.triggerName(itrig);    
     trigNames->push_back(trigName);    
   }

    Handle < std::vector<pat::GenericParticle> >thePATTrackHandle;
    evt.getByToken(tracks_, thePATTrackHandle);

    Handle < View<pat::Muon> > thePATMuonHandle;
    evt.getByToken(MuonType, thePATMuonHandle);
 
	for ( View <pat::Muon>::const_iterator iMuonP = thePATMuonHandle->begin(); iMuonP != thePATMuonHandle->end(); ++iMuonP)
        {

           
          int much = iMuonP->charge();
  //      const reco::Muon * rmu = dynamic_cast < const reco::Muon * >(iMuonP->originalObject()); 
/*            muPx->push_back(iMuonP->p4());
            muPy->push_back(iMuonP->py());
            muPz->push_back(iMuonP->pz());
            muCharge->push_back(iMuonP->charge());*/
            
//            TrackRef muTrackP = iMuonP->track();

            for (View < pat::Muon >::const_iterator iMuonM = iMuonP + 1; iMuonM != thePATMuonHandle->end(); ++iMuonM)
            {

            //    TrackRef muTrackM = iMuonM->track(); 

 /*               ParticleMass  muon_mass = 0.10565837;    // pdg mass
                float muon_sigma = muon_mass * 1.e-6;     
                float chi = 0.;
                float ndf = 0.;
                vector < RefCountedKinematicParticle > muonParticles;
                KinematicParticleFactoryFromTransientTrack pFactory;
                muonParticles.push_back(pFactory.particle(muonPTT, muon_mass, chi, ndf, muon_sigma));
                muonParticles.push_back(pFactory.particle(muonMTT, muon_mass, chi, ndf, muon_sigma));
                KinematicParticleVertEXFitter fitter;
                RefCountedKinematicTree psiVertexFitTree;
                psiVertexFitTree = fitter.fit(muonParticles);   // fit to the muon pair
                if (!psiVertexFitTree->isValid()) continue;
                psiVertexFitTree->movePointerToTheTop();
                RefCountedKinematicParticle psi_vFit_noMC = psiVertexFitTree->currentParticle();
                RefCountedKinematicVertex psi_vFit_vertex_noMC = psiVertexFitTree->currentDecayVertex();
                JMass->push_back(psi_vFit_noMC->currentState().mass());
                JDecayVtxX->push_back(psi_vFit_vertex_noMC->position().x());
                JDecayVtxY->push_back(psi_vFit_vertex_noMC->position().y());
                JDecayVtxZ->push_back(psi_vFit_vertex_noMC->position().z());
                JDecayVtxXE->push_back(sqrt(psi_vFit_vertex_noMC->error().cxx()));
                JDecayVtxYE->push_back(sqrt(psi_vFit_vertex_noMC->error().cyy()));
                JDecayVtxZE->push_back(sqrt(psi_vFit_vertex_noMC->error().czz()));*/

         for (std::vector< pat::GenericParticle >::const_iterator iTrackP = thePATTrackHandle->begin(); iTrackP != thePATTrackHandle->end(); ++iTrackP)   // 1st
           {
            pat::GenericParticle MyTrackP = *iTrackP;

            trPx->push_back(MyTrackP.px());
            trPy->push_back(MyTrackP.py());
            trPz->push_back(MyTrackP.pz());
            trE->push_back(MyTrackP.pt());


       }
     }  
  }


    trigNames->clear();
 //   L1TT->clear();
    MatchTriggerNames->clear(); 
    runNum = 0;
    evtNum = 0;
    lumiNum = 0;
    trPx->clear();
    trPy->clear();
    trPz->clear();
    trE->clear();
}

void JPsiKKKPATRunII::beginRun(edm::Run const &iRun, edm::EventSetup const &iSetup)
{
}

void JPsiKKKPATRunII::beginJob()
{
    edm::Service < TFileService > fs;
    X_One_Tree_ = fs->make < TTree > ("X_data", "X Data");
    X_One_Tree_->Branch("TrigNames", &trigNames);
    X_One_Tree_->Branch("MatchTriggerNames", &MatchTriggerNames);
//    X_One_Tree_->Branch("L1TrigRes", &L1TT);
    X_One_Tree_->Branch("evtNum", &evtNum, "evtNum/i");
    X_One_Tree_->Branch("runNum", &runNum, "runNum/i");
    X_One_Tree_->Branch("lumiNum", &lumiNum, "lumiNum/i");
/*    X_One_Tree_->Branch("priVtxX", &priVtxX, "priVtxX/f");
    X_One_Tree_->Branch("priVtxY", &priVtxY, "priVtxY/f");
    X_One_Tree_->Branch("priVtxZ", &priVtxZ, "priVtxZ/f");
    X_One_Tree_->Branch("priVtxXE", &priVtxXE, "priVtxXE/f");
    X_One_Tree_->Branch("priVtxYE", &priVtxYE, "priVtxYE/f");
    X_One_Tree_->Branch("priVtxZE", &priVtxZE, "priVtxZE/f");
    X_One_Tree_->Branch("priVtxChiNorm", &priVtxChiNorm, "priVtxChiNorm/f");
    X_One_Tree_->Branch("priVtxChi", &priVtxChi, "priVtxChi/f");
    X_One_Tree_->Branch("priVtxCL", &priVtxCL, "priVtxCL/f");*/
    X_One_Tree_->Branch("nMu", &nMu, "nMu/i");
    X_One_Tree_->Branch("muPx", &muPx);
    X_One_Tree_->Branch("muPy", &muPy);
    X_One_Tree_->Branch("muPz", &muPz);
    X_One_Tree_->Branch("muD0", &muD0);
    X_One_Tree_->Branch("muCharge", &muCharge);
    X_One_Tree_->Branch("TrackPx", &trPx);
    X_One_Tree_->Branch("TrackPy", &trPy);
    X_One_Tree_->Branch("TrackPz", &trPz);
    X_One_Tree_->Branch("TrackEnergy", &trE);

}

void JPsiKKKPATRunII::endJob()
{
    X_One_Tree_->GetDirectory()->cd();
    X_One_Tree_->Write();
}

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(JPsiKKKPATRunII);
