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
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            user_decay_file = cms.vstring('GeneratorInterface/ExternalDecays/data/Bd_JpsiKstar_mumuKpi.dec'),
            list_forced_decays = cms.vstring('MyB0','Myanti-B0'),
            operates_on_particles = cms.vint32()
            ),
        parameterSets = cms.vstring('EvtGen130')
        ),


                         PythiaParameters = cms.PSet(pythia8CommonSettingsBlock,
                                                     pythia8CUEP8M1SettingsBlock,
                                                     ## check this (need extra parameters?)
                                                     processParameters = cms.vstring("SoftQCD:nonDiffractive = on",
                                                                                      'PTFilter:filter = on',
                                                                                      'PTFilter:quarkToFilter = 5',
                                                                                      'PTFilter:scaleToFilter = 1.0',                                                    
                                                                                     ),
                                                     parameterSets = cms.vstring('pythia8CommonSettings',
                                                                                 'pythia8CUEP8M1Settings',
                                                                                 'processParameters',
                                                                                 )
                                                     )
                         )

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.1 $'),
    name = cms.untracked.string('$Source: Configuration/Generator/python/PYTHIA8_Bd2JpsiKstar_EtaPtFilter_CUEP8M1_13TeV_cff.py  $'),
    annotation = cms.untracked.string('Summer16: Pythia8+EvtGen130 generation of Bd --> Jpsi(-> mu+ mu-) K*(892)(-> K+ pi-) , 13TeV, Tune CUETP8M1')
    )

###########
# Filters #
###########

bfilter = cms.EDFilter(
    "PythiaFilter", 
    MaxEta = cms.untracked.double(9999.),
    MinEta = cms.untracked.double(-9999.),
    ParticleID = cms.untracked.int32(511)  ## Bd
    )

jpsifilter = cms.EDFilter(
    "PythiaDauVFilter",
    MotherID = cms.untracked.int32(511),
    ParticleID = cms.untracked.int32(443),
    NumberDaughters = cms.untracked.int32(2),
    DaughterIDs = cms.untracked.vint32(13, -13),
    MinPt = cms.untracked.vdouble(-99., -99.),
    MinEta = cms.untracked.vdouble(-9999., -9999.),
    MaxEta = cms.untracked.vdouble(9999., 9999.),
    verbose = cms.untracked.int32(1)
)

kstarfilter = cms.EDFilter(
    "PythiaDauVFilter",
    MotherID = cms.untracked.int32(511),
    ParticleID = cms.untracked.int32(313),
    NumberDaughters = cms.untracked.int32(2),
    DaughterIDs = cms.untracked.vint32(321, -211),
    MinPt = cms.untracked.vdouble(-99., -99.),
    MinEta = cms.untracked.vdouble(-9999., -9999.),
    MaxEta = cms.untracked.vdouble(9999., 9999.),
    verbose = cms.untracked.int32(1)
)



ProductionFilterSequence = cms.Sequence(generator*bfilter*jpsifilter*kstarfilter)
