import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring('myY4140'),
	    operates_on_particles = cms.vint32(100443), # we care just about our signal particles
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded = cms.vstring(
            """ 
################################################################################
#
Alias      myY4140      psi(2S)   ## Psi(2S) for scalar particle assumption.
Particle   myY4140      4.140 0.092
#
Alias      myJpsi J/psi
ChargeConj myJpsi myJpsi
#
Alias      myPhi  phi
ChargeConj myPhi  myPhi
#
Decay myY4140
1.000      myJpsi myPhi PHSP;
Enddecay
#
Decay myAnti-Y4140
1.000      myJpsi myPhi PHSP;
Enddecay
#
Decay myJpsi
1.000      mu+    mu-   PHOTOS VLL;
Enddecay
#
Decay MyPhi
0.5   K+ K- VSS;
0.5   mu+ mu- PHOTOS VLL;
Enddecay
#
End"""
        )
    
     ),
        parameterSets = cms.vstring('EvtGen130')
  ),
     PythiaParameters = cms.PSet(pythia8CommonSettingsBlock,
                                 pythia8CUEP8M1SettingsBlock,
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
	    '100443= off'						 
                                                               ),
                                 parameterSets = cms.vstring('pythia8CommonSettings',
                                                             'pythia8CUEP8M1Settings',
                                                             'processParameters',
                                                             )
                                  )
 )
 ###########
# Filters #
###########
                         
yfilter = cms.EDFilter(
    "PythiaFilter", 
    MaxEta = cms.untracked.double(9999.),
    MinEta = cms.untracked.double(-9999.),
    ParticleID = cms.untracked.int32(100443) ## Psi(2S) as Y4140
    )

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
                         
jpsifilter = cms.EDFilter(
        "PythiaDauVFilter",
	verbose         = cms.untracked.int32(4*1), 
	NumberDaughters = cms.untracked.int32(2), 
	MotherID        = cms.untracked.int32(100443),  
	ParticleID      = cms.untracked.int32(443),  
        DaughterIDs     = cms.untracked.vint32(13, -13),
	MinPt           = cms.untracked.vdouble(2.5, 2.5), 
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
    DaughterIDs     = cms.untracked.vint32(321, -321),
    MinPt           = cms.untracked.vdouble(-1.0, -1.0),
    MinEta          = cms.untracked.vdouble(-9999, -9999),
    MaxEta          = cms.untracked.vdouble( 9999,  9999)
    )
    
 phiToMuMufilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(4*1),
    NumberDaughters = cms.untracked.int32(2),
    MotherID        = cms.untracked.int32(100443),
    ParticleID      = cms.untracked.int32(333),
    NumberDaughters = cms.untracked.int32(1),
    DaughterIDs     = cms.untracked.vint32(13, -13),
    MinPt           = cms.untracked.vdouble(-1.0, -1.0),
    MinEta          = cms.untracked.vdouble(-9999, -9999),
    MaxEta          = cms.untracked.vdouble( 9999,  9999)
    )
 
                         
ProductionFilterSequence = cms.Sequence(generator
                                        *yfilter
                                        *decayfilter
                                        *jpsifilter
                                        *phiToMuMufilter
                                        *phiToKKfilter
                                        )                       
