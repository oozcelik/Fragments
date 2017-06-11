import FWCore.ParameterSet.Config as cms

process = cms.Process("NTUPLE")

process.options = cms.untracked.PSet(
        wantSummary = cms.untracked.bool(False)
)
runOnMC=False
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(200) )

process.load("Configuration.Geometry.GeometryRecoDB_cff")
#process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load('Configuration.StandardSequences.Services_cff')
#process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
#process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
#process.load('HLTrigger.HLTfilters.hltLevel1GTSeed_cfi') # not working 

process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.options.allowUnscheduled = cms.untracked.bool(True)

process.source = cms.Source("PoolSource",fileNames = cms.untracked.vstring(
#'/store/data/Run2016H/Charmonium/AOD/PromptReco-v3/000/284/036/00000/000C982D-B09F-E611-A1AF-02163E0142F3.root'
'/store/data/Run2016C/MuOnia/AOD/PromptReco-v2/000/275/768/00000/38155E0E-543C-E611-BE5E-02163E014593.root'
))

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '') ## applicable to MC
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_dataRun2_Prompt_v9', '')


process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
        #vertexCollection = cms.InputTag('offlinePrimaryVertices'),
        vertexCollection = cms.InputTag('offlinePrimaryVerticesWithBS'),
        minimumNDOF = cms.uint32(4) ,
        maxAbsZ = cms.double(24),
        maxd0 = cms.double(2)
)

process.noscraping = cms.EDFilter("FilterOutScraping",
    applyfilter = cms.untracked.bool(True),
        debugOn = cms.untracked.bool(False),
        numtrack = cms.untracked.uint32(10),
        thresh = cms.untracked.double(0.25)
)

process.load("PhysicsTools.PatAlgos.patSequences_cff")
process.load("PhysicsTools.PatAlgos.cleaningLayer1.genericTrackCleaner_cfi")
process.cleanPatTracks.checkOverlaps.muons.requireNoOverlaps = cms.bool(False)
process.cleanPatTracks.checkOverlaps.electrons.requireNoOverlaps = cms.bool(False)
from PhysicsTools.PatAlgos.producersLayer1.muonProducer_cfi import *
patMuons.embedTrack = cms.bool(True)
patMuons.embedPickyMuon = cms.bool(False)
patMuons.embedTpfmsMuon = cms.bool(False)
#process.load("MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff")

process.filter = cms.Sequence(process.primaryVertexFilter+process.noscraping)

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
        );                                    # you can specify more than one collection for this
l1cands = getattr(process, 'patTrackCands')
l1cands.addGenMatch = False

process.load("MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff")

from MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff import *
addDiMuonTriggers(process)
if runOnMC:
        addMCinfo(process)
changeTriggerProcessName(process, 'HLT')
process.muonMatch.resolveByMatchQuality = True
useL1MatchingWindowForSinglets(process)
switchOffAmbiguityResolution(process) # Switch off ambiguity resolution: allow multiple reco muons to match to the same trigger muon
process.muonL1Info.maxDeltaR = 0.3
process.muonL1Info.fallbackToME1 = True
process.muonMatchHLTL1.maxDeltaR = 0.3
process.muonMatchHLTL1.fallbackToME1 = True
process.muonMatchHLTL2.maxDeltaR = 0.3
process.muonMatchHLTL2.maxDPtRel = 10.0
process.muonMatchHLTL3.maxDeltaR = 0.1
process.muonMatchHLTL3.maxDPtRel = 10.0
process.muonMatchHLTCtfTrack.maxDeltaR = 0.1
process.muonMatchHLTCtfTrack.maxDPtRel = 10.0
process.muonMatchHLTTrackMu.maxDeltaR = 0.1
process.muonMatchHLTTrackMu.maxDPtRel = 10.0

from PhysicsTools.PatAlgos.tools.coreTools import *
removeMCMatching(process, names=['All'],outputModules=[])
#removeMCMatching(process, ['Photons','Electrons', 'Muons', 'Taus', 'Jets', 'METs', 'PFAll', 'PFElectrons', 'PFTaus', 'PFMuons'])

process.mkcands = cms.EDAnalyzer("JPsiKKKPATRunII",
     HLTriggerResults = cms.InputTag("TriggerResults","","HLT"),
     beamSpotTag = cms.InputTag("offlineBeamSpot"),
  #   VtxSample   = cms.InputTag('offlinePrimaryVertices'),
     Trak        = cms.InputTag('selectedPatTrackCands'), #selectedPatTracks
     muons       = cms.InputTag('patMuonsWithTrigger'), #oniaPATMuonsWithoutTrigger-  #selectedPatMuons
     revtxtrks   = cms.InputTag('generalTracks'),
     trackQualities = cms.untracked.vstring('loose','tight','highPurity'),
     TriggersForMatching = cms.untracked.vstring("HLT_Dimuon0_Jpsi_Muon_v18"),
     FiltersForMatching = cms.untracked.vstring("hltVertexmumuFilterJpsiMuon")
)

mytrigs = ["HLT_Dimuon20_Jpsi_v2"]

import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
if mytrigs is not None :
    process.hltSelection = hlt.hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = mytrigs)
    process.hltSelection.throw = False

process.filter = cms.Sequence(process.primaryVertexFilter+process.noscraping)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('MuOniaRun2012_PhaseSpMC2016_ntpl.root')
)
#process.ntup = cms.Path(process.filter*process.mkcands)
process.ntup = cms.Path(process.hltSelection*process.filter*process.patMuonsWithTriggerSequence*process.mkcands)
process.schedule = cms.Schedule(process.ntup)
