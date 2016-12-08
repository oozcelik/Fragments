import FWCore.ParameterSet.Config as cms
process = cms.Process('NTUPLE')

from Configuration.StandardSequences.Reconstruction_cff import*

process.options = cms.untracked.PSet(
        wantSummary = cms.untracked.bool(True)
     )
# import of standard configurations
process.load('FWCore/MessageService/MessageLogger_cfi')
process.MessageLogger.suppressInfo = cms.untracked.vstring( "mkcands" )
process.MessageLogger.suppressWarning = cms.untracked.vstring( "mkcands" )
process.MessageLogger.cerr.FwkReport.reportEvery = 10000
MC=True
# Input source
process.source = cms.Source("PoolSource",
                            #skipEvents = cms.untracked.uint32(0),
                            fileNames = cms.untracked.vstring(
'/store/mc/RunIISpring16DR80/BuToJpsiK_BMuonFilter_SoftQCDnonD_TuneCUEP8M1_13TeV-pythia8-evtgen/AODSIM/premix_withHLT_80X_mcRun2_asymptotic_v14-v1/100000/005190E2-F468-E611-B46F-002590E3A212.root'
#'/store/mc/RunIISummer15GS/BuToJpsiK_SoftQCDnonD_TuneCUEP8M1_13TeV-pythia8-evtgen/GEN-SIM/MCRUN2_71_V1-v1/00000/001F1A39-E5FC-E511-A89C-02163E01328A.root'
))

process.source.inputCommands = cms.untracked.vstring(
    "keep *",
    "drop L1GlobalTriggerObjectMapRecord_hltL1GtObjectMap__RECO",
    "drop *_MEtoEDMConverter_*_*",
    "drop GenLumiInfoProduct_*_*_*"
    )

process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration/EventContent/EventContent_cff')
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

#from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag.globaltag = cms.string('80X_mcRun2_asymptotic_v14') #-------> for extension //// MC Phase Space Summer12_DR53X tag: START53_V19F::All
process.load('HLTrigger/HLTfilters/hltLevel1GTSeed_cfi')

process.noscraping = cms.EDFilter("FilterOutScraping",
applyfilter = cms.untracked.bool(True),
debugOn = cms.untracked.bool(False),
numtrack = cms.untracked.uint32(10),
thresh = cms.untracked.double(0.25)
)

from PhysicsTools.PatAlgos.tools.trackTools import *
makeTrackCandidates(process,                                        #         patAODTrackCands
        label='TrackCands',                   # output collection will be 'allLayer0TrackCands', 'allLayer1TrackCands', 'selectedLayer1TrackCands'
        tracks=cms.InputTag('generalTracks'), # input track collection
        particleType='K+',                   # particle type (for assigning a mass), changed by yik to K+ from pi+
        preselection='pt > 0.5',              # preselection cut on candidates. Only methods of 'reco::Candidate' are available, changed to 0.5 from 0.1 by yik
        selection='pt > 0.5',                 # Selection on PAT Layer 1 objects ('selectedLayer1TrackCands'), changed to 0.5 from 0.1 by yik
        isolation={},                         # Isolations to use ('source':deltaR; set to {} for None)
        isoDeposits=[],
        mcAs=None                           # Replicate MC match as the one used for Muons
        );


# PAT Layer 0+1
process.load("PhysicsTools.PatAlgos.patSequences_cff")
from PhysicsTools.PatAlgos.cleaningLayer1.cleanPatCandidates_cff import *
from PhysicsTools.PatAlgos.producersLayer1.muonProducer_cfi import *
muonSource = 'muons'
patMuons.embedTrack = cms.bool(True)
patMuons.embedPickyMuon = cms.bool(False)
patMuons.embedTpfmsMuon = cms.bool(False)
patMuons.embedGenMatch = cms.bool(False) #set false for MCtruth matching

# Prune generated particles to muons and their parents
process.genMuons = cms.EDProducer("GenParticlePruner",
        src = cms.InputTag("genParticles"),
        select = cms.vstring(
            "drop  *  ",                     # this is the default
            "++keep abs(pdgId) = 13",        # keep muons and their parents
            "drop pdgId == 21 && status = 2" # remove intermediate qcd spam carrying no flavour info
            "drop pdgId == 15"
      )
 )

process.load("MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff")
from MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff import  addMCinfo, useExistingPATMuons, useL1MatchingWindowForSinglets, changeTriggerProcessName, switchOffAmbiguityResolution, addDiMuonTriggers

process.mkcands = cms.EDAnalyzer("JPsiKKKPATRunII",
     HLTriggerResults = cms.InputTag("TriggerResults", "", "HLT"),
     GenParticles  = cms.untracked.string('genParticles'),
     VtxSample   = cms.untracked.string('offlinePrimaryVertices'),
     muons = cms.untracked.InputTag("cleanPatMuons"),
     pattracks = cms.InputTag("cleanPatTrackCands")
##
)


process.TFileService = cms.Service("TFileService",
    fileName = cms.string('MuOniaRun2012_PhaseSpMC2012_ntpl.root')
)


# turn off MC matching for the process
from PhysicsTools.PatAlgos.tools.coreTools import *
removeMCMatching(process, ['Photons','Muons','Taus','Electrons','Jets','METs','PFAll'], outputModules=[ ])
process.patDefaultSequence.remove(process.patJetCorrFactors)
process.patDefaultSequence.remove(process.patJetCharge)
process.patDefaultSequence.remove(process.patJetPartonMatch)
process.patDefaultSequence.remove(process.patJetGenJetMatch)
process.patDefaultSequence.remove(process.patJets)
process.patDefaultSequence.remove(process.patMETs)
process.patDefaultSequence.remove(process.selectedPatJets)
process.patDefaultSequence.remove(process.cleanPatJets)
process.patDefaultSequence.remove(process.countPatJets)
process.out = cms.OutputModule("PoolOutputModule",
        fileName = cms.untracked.string('onia2MuMuPAT.root'),
        outputCommands = cms.untracked.vstring('drop *',
            #'keep *_genMuons_*_Onia2MuMuPAT',                      # generated muons and parents
            'keep patMuons_patMuonsWithTrigger_*_NTUPLE',    # All PAT muos including general tracks and matches to triggers
#            'keep   *_tracks_*'
     )
)

process.filter = cms.Sequence(process.noscraping)

## AF: replace EndPath with path
process.ntup = cms.Path(process.filter*process.patDefaultSequence*process.mkcands)
#process.ntup = cms.Path(process.filter*process.mkcands)
process.schedule = cms.Schedule(process.ntup)
