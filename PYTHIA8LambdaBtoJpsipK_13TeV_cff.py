import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    filterEfficiency = cms.untracked.double(1.38e-3),
    crossSection = cms.untracked.double(540000000.),
    comEnergy = cms.double(13000.0),
    
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2010_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt.pdl'), ##evtLbJpsipK.pdl
            user_decay_file = cms.vstring('GeneratorInterface/EvtGenInterface/data/LambdaB_JPsipK.dec'),
            list_forced_decays = cms.vstring('MyLambda_b0','Myanti-Lambda_b0'),
            operates_on_particles = cms.vint32(),
            ),
        parameterSets = cms.vstring('EvtGen130')
        ),
                         
    PythiaParameters = cms.PSet(pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters = cms.vstring("SoftQCD:nonDiffractive = on"),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'processParameters',
                                    )
        )
    )

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

bfilter = cms.EDFilter("PythiaFilter",
        ParticleID = cms.untracked.int32(5122)
        )

jpsiDaufilter = cms.EDFilter( "PythiaDauVFilter",
        verbose = cms.untracked.int32(0),
        NumberDaughters = cms.untracked.int32(2),
        MotherID = cms.untracked.int32(5122),
        ParticleID = cms.untracked.int32(443),
        DaughterIDs = cms.untracked.vint32(13, -13),
        MinPt = cms.untracked.vdouble(2.9,2.9),
        MinEta = cms.untracked.vdouble(-2.6, -2.6),
        MaxEta = cms.untracked.vdouble( 2.6,2.6)
        )

bDaufilter = cms.EDFilter("PythiaDauVFilter",
        verbose = cms.untracked.int32(0),
        NumberDaughters = cms.untracked.int32(3),
        MotherID = cms.untracked.int32(0),
        ParticleID = cms.untracked.int32(5122),
        DaughterIDs = cms.untracked.vint32(443,2212,-321),
        MinPt = cms.untracked.vdouble(6.8,0.9,0.9),
        MinEta = cms.untracked.vdouble(-19.9,-3.5,-3.5),
        MaxEta = cms.untracked.vdouble(19.9,3.5,3.5)
        )

ProductionFilterSequence = cms.Sequence(generator*bfilter*bDaufilter*jpsiDaufilter)
