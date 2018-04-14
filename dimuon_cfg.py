import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring(),
            operates_on_particles = cms.vint32(),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_file = cms.vstring(''),
            parameterSets = cms.vstring('EvtGen130')
        ),        
        PythiaParameters = cms.PSet(pythia8CommonSettingsBlock,
                                                     pythia8CP5SettingsBlock,
                                                     processParameters = cms.vstring("SoftQCD:nonDiffractive = on",
                                                                                     'PTFilter:filter = on', # this turn on the filter                                                                                
                                                                                     'PTFilter:quarkToFilter = 5', # PDG id of q quark
                                                                                     'PTFilter:scaleToFilter = 1.0'),
                                                     parameterSets = cms.vstring('pythia8CommonSettings',
                                                                                 'pythia8CP5Settings',
                                                                                 'processParameters',
                                                                                 )
                                                     )
                         )

### Filters ####

TwoMuonFilter = cms.EDFilter("MCParticlePairFilter",  
    Status = cms.untracked.vint32(1,1),
    MinPt = cms.untracked.vdouble(3.5, 3.5),
    MaxPt = cms.untracked.vdouble(9999.0,9999.0),
    MaxEta = cms.untracked.vdouble( 2.5,2.5),
    MinEta = cms.untracked.vdouble(-2.5,-2.5),
    ParticleID1 = cms.untracked.vint32(13),
    ParticleID2 = cms.untracked.vint32(-13),
    MinInvMass = cms.untracked.double(4.5),
    MaxInvMass = cms.untracked.double(6.5),
)

ProductionFilterSequence = cms.Sequence(generator*TwoMuonFilter)
