import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         maxEventsToPrint = cms.untracked.int32(0),
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         filterEfficiency = cms.untracked.double(1.38e-3),
                         crossSection = cms.untracked.double(540000000.),
                         comEnergy = cms.double(13000.0),

                         ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/ExternalDecays/data/evt_2014.pdl'),
            user_decay_embedded= cms.vstring("""
            Decay B+
            0.000000550 K+      e+      e-     PHOTOS BTOSLLBALL; #[Reconstructed PDG2011];
            0.000000520 K+      mu+     mu-    PHOTOS BTOSLLBALL; #[Reconstructed PDG2011];
            Enddecay             
            """
            list_forced_decays = cms.vstring('MyB+',
                                             'Myanti-B+'),
            ),
        operates_on_particles = cms.vint32(),
        parameterSets = cms.vstring('EvtGen130')
        ),
                         
                         PythiaParameters = cms.PSet(pythia8CommonSettingsBlock,
                                                     pythia8CUEP8M1SettingsBlock,
                                                     processParameters = cms.vstring('SoftQCD:nonDiffractive = on'                                                                                   
                                                                                    ),
                                                     parameterSets = cms.vstring('pythia8CommonSettings',
                                                                                 'pythia8CUEP8M1Settings',
                                                                                 'processParameters',
                                                                                 )
                                                     )
                         )

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

bfilter = cms.EDFilter(
    "PythiaFilter",
    MaxEta = cms.untracked.double(9999.),
    MinEta = cms.untracked.double(-9999.),
    ParticleID = cms.untracked.int32(531)
    )

jpsifilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1), 
    NumberDaughters = cms.untracked.int32(2), 
    MotherID        = cms.untracked.int32(531),  
    ParticleID      = cms.untracked.int32(443),  
    DaughterIDs     = cms.untracked.vint32(13, -13),
    MinPt           = cms.untracked.vdouble(2.5, 2.5), 
    MinEta          = cms.untracked.vdouble(-2.5, -2.5), 
    MaxEta          = cms.untracked.vdouble( 2.5,  2.5)
    )

phifilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1), 
    NumberDaughters = cms.untracked.int32(2), 
    MotherID        = cms.untracked.int32(531),  
    ParticleID      = cms.untracked.int32(333),  
    DaughterIDs     = cms.untracked.vint32(321, -321),
    MinPt           = cms.untracked.vdouble(0.4, 0.4), 
    MinEta          = cms.untracked.vdouble(-2.5, -2.5), 
    MaxEta          = cms.untracked.vdouble( 2.5,  2.5)
    )

ProductionFilterSequence = cms.Sequence(generator*bfilter*jpsifilter*phifilter)