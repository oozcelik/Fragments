import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.0),
                         ##crossSection = cms.untracked.double(54000000000), # Given by PYTHIA after running
                         ##filterEfficiency = cms.untracked.double(0.004), # Given by PYTHIA after running
                         maxEventsToPrint = cms.untracked.int32(0),


                         ExternalDecays = cms.PSet(
            EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2010_NOLONGLIFE.DEC'),  
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt.pdl'),
            user_decay_file = cms.vstring('GeneratorInterface/ExternalDecays/data/Bu_JpsiK.dec'),
            list_forced_decays = cms.vstring('MyB+','MyB-'),
            operates_on_particles = cms.vint32()
            ),
        parameterSets = cms.vstring('EvtGen130')
        ),


                         PythiaParameters = cms.PSet(pythia8CommonSettingsBlock,
                                                     pythia8CUEP8M1SettingsBlock,
                                                     ## check this (need extra parameters?)
                                                     processParameters = cms.vstring('SoftQCD:nonDiffractive = on',
                                                                                     'SoftQCD:singleDiffractive = on',
                                                                                     'SoftQCD:doubleDiffractive = on',),
                                                     parameterSets = cms.vstring('pythia8CommonSettings',
                                                                                 'pythia8CUEP8M1Settings',
                                                                                 'processParameters',
                                                                                 )
                                                     )
                         )

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.1 $'),
    name = cms.untracked.string('$Source: Configuration/Generator/python/PYTHIA8_Bu2MuMuK_EtaPtFilter_CUEP8M1_13TeV_cff.py $'),
    annotation = cms.untracked.string('Summer16: Pythia8+EvtGen130 generation of Bu --> mu+ mu- K+ , 13TeV, Tune CUETP8M1')
    )

###########
# Filters #
###########
# Filter only pp events which produce a B+:

bufilter = cms.EDFilter(
    "PythiaFilter", 
    MaxEta = cms.untracked.double(9999.),
    MinEta = cms.untracked.double(-9999.),
    ParticleID = cms.untracked.int32(521) ## Bu
    )

jpsifilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1), 
    NumberDaughters = cms.untracked.int32(2), 
    MotherID        = cms.untracked.int32(521),  
    ParticleID      = cms.untracked.int32(443),  # J/psi
    DaughterIDs     = cms.untracked.vint32(13, -13), # mu+ mu-
    MinPt           = cms.untracked.vdouble(3., 3.), 
    MinEta          = cms.untracked.vdouble(-3., -3.), 
    MaxEta          = cms.untracked.vdouble( 3., 3.)
    )

decayfilter = cms.EDFilter(  # you may apply cuts on J/psi and K+ here.
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1), 
    NumberDaughters = cms.untracked.int32(2), 
    ParticleID      = cms.untracked.int32(521),  ## Bu  
    DaughterIDs     = cms.untracked.vint32(443, 321), ## J/psi, K+
    MinPt           = cms.untracked.vdouble(0., 0.), 
    MinEta          = cms.untracked.vdouble(-9999., -9999.), 
    MaxEta          = cms.untracked.vdouble( 9999., 9999.)

    )

multiFilter = cms.EDFilter("MCMultiParticleFilter", # apply cuts on additional muon
    Status = cms.vint32(1, 1, 1),
    src = cms.InputTag('generator'),
    ParticleID = cms.vint32(13, 13, 13),
    EtaMax = cms.untracked.double(3., 3., 3.),
    PtMin = cms.untracked.double(3., 3., 3.),
    NumRequired = cms.int32(1),
    AcceptMore = cms.bool(True)
    )

ProductionFilterSequence = cms.Sequence(generator*bufilter*jpsifilter*decayfilter*multiFilter)
