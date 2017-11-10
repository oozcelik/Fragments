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
            user_decay_file = cms.FileInPath('GeneratorInterface/ExternalDecays/data/Dstar_D0_Kpi.dec'),
            list_forced_decays = cms.vstring('MyD*+','MyD*-'),        # will force one at the time
            operates_on_particles = cms.vint32(0),                  # we care just about our signal particles
            convertPythiaCodes = cms.untracked.bool(False),
            parameterSets = cms.vstring('EvtGen130')
        ),
        PythiaParameters = cms.PSet(
              pythia8CommonSettingsBlock,
	            pythia8CP5SettingsBlock,
              processParameters = cms.vstring('Charmonium:all = on'),
              parameterSets = cms.vstring('pythia8CommonSettings',
		                                      'pythia8CP5Settings',
                                          'processParameters',
                                         )
      )
)

DstarFilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(100.), # Mother Max_Eta = 100
    MinEta = cms.untracked.double(-100.), # Mother Min_Eta = -100
    MinPt = cms.untracked.double(3.9), # Mother Min_Pt = 3.9 GeV 
    ParticleID = cms.untracked.int32(413) # D0*
)

decayfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(413), # Mother is D0*
    ParticleID = cms.untracked.int32(421), # Daughter is D0
    NumberDaughters = cms.untracked.int32(2),  
    DaughterIDs = cms.untracked.vint32(-321,211), # Daughter of D0 are K- and pi+
    MinPt = cms.untracked.vdouble(-9999., -9999.), # No kinematic cuts on descendants
    MaxEta = cms.untracked.vdouble(9999., 9999.), # No kinematic cuts on descendants
    MinEta = cms.untracked.vdouble(-9999., -9999.), # No kinematic cuts on descendants
)

ProductionFilterSequence = cms.Sequence(
                         generator
                        *DstarFilter                       
)

