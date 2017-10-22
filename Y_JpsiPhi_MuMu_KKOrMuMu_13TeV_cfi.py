import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(8000.0),
    crossSection = cms.untracked.double(0.0),
    maxEventsToPrint = cms.untracked.int32(0),
    PythiaParameters = cms.PSet(
        pythia8CommonSettings = cms.vstring('Main:timesAllowErrors = 10000', 
            'Check:epTolErr = 0.01', 
            'Beams:setProductionScalesFromLHEF = off', 
            'SLHA:keepSM = on', 
            'SLHA:minMassSM = 1000.', 
            'ParticleDecays:limitTau0 = on', 
            'ParticleDecays:tau0Max = 10', 
            'ParticleDecays:allowPhotonRadiation = on'),
        pythia8CUEP8M1Settings = cms.vstring('Tune:pp 14', 
            'Tune:ee 7', 
            'MultipartonInteractions:pT0Ref=2.4024', 
            'MultipartonInteractions:ecmPow=0.25208', 
            'MultipartonInteractions:expPow=1.6'),
        processParameters = cms.vstring('Onia:all(3S1) = on', 
            'Charmonium:gg2ccbar(3S1)[3S1(1)]g = off,on', 
            'Charmonium:gg2ccbar(3S1)[3S1(8)]g = off,on', 
            'Charmonium:qg2ccbar(3S1)[3S1(8)]q = off,on', 
            'Charmonium:qqbar2ccbar(3S1)[3S1(8)]g = off,on', 
            'Charmonium:gg2ccbar(3S1)[1S0(8)]g = off,on', 
            'Charmonium:qg2ccbar(3S1)[1S0(8)]q = off,on', 
            'Charmonium:qqbar2ccbar(3S1)[1S0(8)]g = off,on', 
            'Charmonium:gg2ccbar(3S1)[3PJ(8)]g = off,on', 
            'Charmonium:qg2ccbar(3S1)[3PJ(8)]q = off,on', 
            'Charmonium:qqbar2ccbar(3S1)[3PJ(8)]g = off,on', 
            'ParticleDecays:allowPhotonRadiation = off,on', 
            '100443:m0 = 4.5060', 
            '100443:mWidth = 0.092', 
            '100443:mMin = 4.116', 
            '100443:mMax = 5.886', 
            '100443:spinType = 1', 
            '100443:addChannel = on 1 0 443 333', 
            '100443:onMode = off', 
            '100443:onIfMatch = 443 333', 
            '443:onMode = off',
            '443:onIfMatch = 13 -13',
            '333:onMode = off',
            '333:0:onMode = on', # channel 0 = 321 -321
            '333:0:bRatio = 0.5',
            '333:9:onMode = on', # channel 9 = 13 -13
            '333:9:bRatio = 0.5',
 ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
 )
 
 #pythia.particleData.listChangedd() #To list only the data of the particles that have been changed

motherFilter = cms.EDFilter(
    "PythiaFilter",
    MaxEta = cms.untracked.double(9999.),
    MinEta = cms.untracked.double(-9999.),
    ParticleID = cms.untracked.int32(100443)
    )

# verbose threshold for "PythiaDauVFilter" are 2,5,10
decayfilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(4*3),
    NumberDaughters = cms.untracked.int32(2),
    ParticleID      = cms.untracked.int32(100443),
    DaughterIDs     = cms.untracked.vint32(443, 333),
    MinPt           = cms.untracked.vdouble(-1.0, -1.0),
    MinEta          = cms.untracked.vdouble(-9999., -9999.),
    MaxEta          = cms.untracked.vdouble( 9999.,  9999.)
    )

psifilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(4*1),
    NumberDaughters = cms.untracked.int32(2),
    MotherID        = cms.untracked.int32(100443),
    ParticleID      = cms.untracked.int32(443),
    DaughterIDs     = cms.untracked.vint32(13, -13),
    MinPt           = cms.untracked.vdouble(0.5, 0.5),
    MinEta          = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta          = cms.untracked.vdouble( 2.5,  2.5)
    )

phiToMuMufilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(4*1),
    NumberDaughters = cms.untracked.int32(2),
    MotherID        = cms.untracked.int32(100443),
    ParticleID      = cms.untracked.int32(333),
    NumberDaughters = cms.untracked.int32(1),
    DaughterIDs     = cms.untracked.vint32(13, -13),
    MinPt           = cms.untracked.vdouble(0.5, 0.5),
    MinEta          = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta          = cms.untracked.vdouble( 2.5,  2.5)
    )

phiToKKfilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(4*1),
    NumberDaughters = cms.untracked.int32(2),
    MotherID        = cms.untracked.int32(100443),
    ParticleID      = cms.untracked.int32(333),
    NumberDaughters = cms.untracked.int32(1),
    DaughterIDs     = cms.untracked.vint32(321, -321),
    MinPt           = cms.untracked.vdouble(0.5, 0.5),
    MinEta          = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta          = cms.untracked.vdouble( 2.5,  2.5)
    )


ProductionFilterSequence = cms.Sequence(generator
					*motherFilter
					*decayfilter
					*psifilter
					*phiToMuMufilter
					*phiToKKfilter
					)
          
configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.1 $'),
    #name = cms.untracked.string('$Source: /local/reps/CMSSW/CMSSW/Configuration/GenProduction/python/EightTeV/PYTHIA6_Bd2Psi2SKpi_TuneZ2star_8TeV_cff.py,v $'),
    name = cms.untracked.string('$Source: /afs/cern.ch/user/l/lecriste/sanjay_code/CMSSW_5_3_22/src/Configuration/GenProduction/python/PYTHIA8_Y4500ToJpsiPhi_mumumumu_TuneZ2star_13TeV_noPtEtaCuts_cff.py,v $'),
    annotation = cms.untracked.string('Y4500 -> J/psi Phi -> mumu mumu at 13TeV')
    )
