import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(1),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.0),
    crossSection = cms.untracked.double(108800000),
    filterEfficiency = cms.untracked.double(1.),
    maxEventsToPrint = cms.untracked.int32(0),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters = cms.vstring(
             #'Charmonium:all = on',                       # Quarkonia, MSEL=61, including feed-down as well                                                          
                 'Onia:all(3S1) = on',
                      #'Charmonium:states(3S1)'   (default = 443,100443; minimum = 0) # it looks like this line needs to match the following lines                    
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
             'ParticleDecays:allowPhotonRadiation = off,on',  # Turn on/off QED FSR, see pythia8CommonSettings                                                        
             '100443:m0 = 4.140', # Psi(2S) assigned as Y(4140) 4.5060 
             '100443:mWidth = 0.092',
             '100443:mMin = 4.116', # 4.116 = m(J/psi) + m(phi)                                                                                                       
             '100443:mMax = 5.886', # 4.568 = 4.506 +15*mWidth                                                                                                        
             '100443:spinType = 0',                                                                                                                                                       
                      #id:addChannel = onMode bRatio meMode products                                                                                                  
                      #meMode(): the mode of processing this channel, possibly with matrix-element information; 0 gives isotropic phase space.  
                       '100443:addChannel = on 1 0 443 333',
             '100443:onMode = off',        # turn off Y(4500) decays inherited from psi(2S)                                                                           
             '100443:onIfMatch = 443 333', # just let Y(4500) -> J/psi phi                                                                                            
             '443:onMode = off',           # Turn off J/psi decays                                                                                                    
             '443:onIfMatch = 13 -13',     # just let J/psi -> mu+ mu-                                                                                                
             '333:onMode = off',           # Turn off phi decays                                                                                                      
             '333:onIfMatch = 321 -321',     # just let phi -> K+ K-                                                                                                  
             ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                        'pythia8CUEP8M1Settings',
                                        'processParameters',
                                    #'bbbarSettings'                                                                                                                  
                                       )
    )
)


#####Filter efficiency is 7.6e-2 ######################

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
    MinPt           = cms.untracked.vdouble(-1.0, -1.0),
    MinEta          = cms.untracked.vdouble(-9999, -9999),
    MaxEta          = cms.untracked.vdouble( 9999,  9999)
    )

phifilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(4*1),
    NumberDaughters = cms.untracked.int32(2),
    MotherID        = cms.untracked.int32(100443),
    ParticleID      = cms.untracked.int32(333),
    DaughterIDs     = cms.untracked.vint32(321, -321),
    MinPt           = cms.untracked.vdouble(-1.0, -1.0),
    MinEta          = cms.untracked.vdouble(-9999, -9999),
    MaxEta          = cms.untracked.vdouble( 9999,  9999)
    )


ProductionFilterSequence = cms.Sequence(generator
                                        *motherFilter
                                        *decayfilter
                                        *psifilter
                                        *phifilter
                                        )

configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.1 $'),
    #name = cms.untracked.string('$Source: /local/reps/CMSSW/CMSSW/Configuration/GenProduction/python/EightTeV/PYTHIA6_Bd2Psi2SKpi_TuneZ2star_8TeV_cff.py,v $'),      
    name = cms.untracked.string('$Source:/afs/cern.ch/user/s/stoyan/public/PYTHIA8_Y4500ToJpsiPhi_mumuKpKm_TuneZ2star_13TeV_noPtEtaCuts_cff.py,v $'),
    annotation = cms.untracked.string('Y4500 -> J/psi Phi -> mumu K+K- at 13TeV')
    )
