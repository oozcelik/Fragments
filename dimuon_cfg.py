import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(14000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring(),
            operates_on_particles = cms.vint32(),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_file = cms.vstring('')
            ),
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
                         
bfilter = cms.EDFilter("PythiaFilter",  # in order to select the b quark.
                       ParticleID = cms.untracked.int32(5)
)
                         
muFilter = cms.EDFilter("MCSmartSingleParticleFilter", # in order to select the muon 
                           MinPt = cms.untracked.vdouble(2.5,2.5),
                           MinEta = cms.untracked.vdouble(-2.5,-2.5),
                           MaxEta = cms.untracked.vdouble( 2.5, 2.5),
                           ParticleID = cms.untracked.vint32(13,-13),
                           Status = cms.untracked.vint32(1,1),                        
                           )
                         
                        
mumuFilter = cms.EDFilter("MCMultiParticleFilter",  # make sure there will be an extra! muon in addition to the one comes from b.
            src = cms.untracked.InputTag("generator","unsmeared"),
            Status = cms.vint32(1),
            ParticleID = cms.vint32(13),
            PtMin = cms.vdouble(0.),
            NumRequired = cms.int32(2),
            EtaMax = cms.vdouble(999.),
            AcceptMore = cms.bool(True)
            )
                       
TwoMuonFilter = cms.EDFilter("MCParticlePairFilter",  # in order to put accceptance cuts on muons 
    Status = cms.untracked.vint32(1,1),
    MinPt = cms.untracked.vdouble(0., 0.),
    MaxPt = cms.untracked.vdouble(9999.0,9999.0),
    MaxEta = cms.untracked.vdouble( 2.5,2.5),
    MinEta = cms.untracked.vdouble(-2.5,-2.5),
    ParticleID1 = cms.untracked.vint32(13),
    ParticleID2 = cms.untracked.vint32(-13),
    MinInvMass = cms.untracked.double(4.5),
    MaxInvMass = cms.untracked.double(6.5),
)

ProductionFilterSequence = cms.Sequence(generator*bfilter*muFilter*mumuFilter*TwoMuonFilter)
