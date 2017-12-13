import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *


generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         maxEventsToPrint = cms.untracked.int32(0),
                         filterEfficiency = cms.untracked.double(1.0),
                         comEnergy = cms.double(13000.0),
                         crossSection = cms.untracked.double(540000000.),
          ExternalDecays = cms.PSet(
            EvtGen130 = cms.untracked.PSet(
            operates_on_particles = cms.vint32( 0 ), # 0 (zero) means default list (hardcoded)
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            convertPythiaCodes = cms.untracked.bool(False),

             ),
            parameterSets = cms.vstring('EvtGen130')
          ),
        PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'HardQCD:hardbbbar = on', # b-bbar decays
         ),  
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters'
                                    )
                  )
         )

mumugenfilter = cms.EDFilter("MCParticlePairFilter", 
    Status = cms.untracked.vint32(1, 1),
    MinPt = cms.untracked.vdouble(2., 2.),
    MaxEta = cms.untracked.vdouble(3., 3.),
    MinEta = cms.untracked.vdouble(-3., -3.),
    ParticleID1 = cms.untracked.vint32(13),
    ParticleID2 = cms.untracked.vint32(-13)
)

ProductionFilterSequence = cms.Sequence(generator*mumugenfilter)
