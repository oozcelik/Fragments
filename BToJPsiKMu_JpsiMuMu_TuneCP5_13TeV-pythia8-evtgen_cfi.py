import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.0),
                         crossSection = cms.untracked.double(54000000000), # Given by PYTHIA after running
                         filterEfficiency = cms.untracked.double(1.), # Given by PYTHIA after running
                         maxEventsToPrint = cms.untracked.int32(0),
                         ExternalDecays = cms.PSet(
            EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),  
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            user_decay_file = cms.vstring('GeneratorInterface/ExternalDecays/data/Bu_JpsiK.dec'),
            list_forced_decays = cms.vstring('MyB+','MyB-'),
            operates_on_particles = cms.vint32()
            ),
        parameterSets = cms.vstring('EvtGen130')
        ),


                         PythiaParameters = cms.PSet(pythia8CommonSettingsBlock,
                                                     pythia8CP5SettingsBlock,
                                                     ## check this (need extra parameters?)
                                                     processParameters = cms.vstring('SoftQCD:nonDiffractive = on',
                                                                                      'PTFilter:filter = on', # this turn on the filter                                                                                
                                                                                     'PTFilter:quarkToFilter = 5', # PDG id of q quark
                                                                                     'PTFilter:scaleToFilter = 1.0'),
                                                     parameterSets = cms.vstring('pythia8CommonSettings',
                                                                                 'pythia8CP5Settings',
                                                                                 'processParameters',
                                                                                 )
                                                     )
                         )


configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.1 $'),
    name = cms.untracked.string('$Source: Configuration/Generator/python/PYTHIA8_Bu2MuMuK_EtaPtFilter_CUEP8M1_13TeV_cff.py $'),
    annotation = cms.untracked.string('Summer16: Pythia8+EvtGen130 generation of Bu --> Jpsi(mu+ mu-) K+ mu, 13TeV, Tune CUETP8M1')
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
    MinPt           = cms.untracked.vdouble(2., 2.), 
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

multiFilter = cms.EDFilter("MCMultiParticleFilter",
            src = cms.untracked.InputTag("generator", "unsmeared"),   
            Status = cms.vint32(1),
            ParticleID = cms.vint32(13),
            PtMin = cms.vdouble(2.),
            NumRequired = cms.int32(3),
            EtaMax = cms.vdouble(3.),
            AcceptMore = cms.bool(True)
            )

ProductionFilterSequence = cms.Sequence(generator*bufilter*jpsifilter*decayfilter*multiFilter)
