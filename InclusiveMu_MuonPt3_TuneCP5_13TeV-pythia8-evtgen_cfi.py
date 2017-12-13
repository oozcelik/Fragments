import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter(
    "Pythia8GeneratorFilter", 
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.0),
    maxEventsToPrint = cms.untracked.int32(0),
    filterEfficiency = cms.untracked.double(1.0e-4),
    crossSection = cms.untracked.double(540000000.),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            operates_on_particles = cms.vint32( 0 ), # 0 (zero) means default list (hardcoded)
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'SoftQCD:nonDiffractive = on',            
        ),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'processParameters',
        )
    )
)


configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.1 $'),
    name = cms.untracked.string('$Source: Configuration/Generator/python/PYTHIA8_InclMu_Pythia8_CUEP8M1_13TeV_cff.py $'),
    annotation = cms.untracked.string('Pythia8+EvtGen130 generation, pT(mu) > 3GeV, 13TeV, Tune CUEP8M1')
)

# -- Filters
muFilter = cms.EDFilter("MCSmartSingleParticleFilter",
                           MinPt = cms.untracked.vdouble(2.0,2.0),
                           MinEta = cms.untracked.vdouble(-3.0,-3.0),
                           MaxEta = cms.untracked.vdouble(3.0,3.0),
                           ParticleID = cms.untracked.vint32(13,-13),
                           Status = cms.untracked.vint32(1,1),                        
                           )

ProductionFilterSequence = cms.Sequence(generator*muFilter)
