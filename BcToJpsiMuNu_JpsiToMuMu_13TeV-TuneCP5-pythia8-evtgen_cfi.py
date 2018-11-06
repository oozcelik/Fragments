import FWCore.ParameterSet.Config as cms

from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(True),
                         comEnergy = cms.double(13000.),
                         ExternalDecays = cms.PSet(
                           EvtGen130 = cms.untracked.PSet(
                             decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
                             particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_Bc_2014.pdl'),
                             convertPythiaCodes = cms.untracked.bool(False),
                             user_decay_embedded= cms.vstring(
"""
# EventType: 14543010 
#
# Descriptor: [B_c+ => (J/psi(1S) => mu+ mu-) mu+ nu_mu]CC
#
# NickName: Bc_JpsiMuNu,mm=BcVegPy,ffEbert
#
# Production: BcVegPy
#
# Documentation: Bc+ to J/psi mu, J/psi -> mumu. Form factor model by Ebert et al., doi:10.1103/PhysRevD.82.034032. Radiative mode included. BcDaughtersInLHCb.
# EndDocumentation
#
Alias      B_c+sig  B_c+
ChargeConj B_c-sig  B_c-
Alias      MyJ/psi  J/psi
ChargeConj MyJ/psi  MyJ/psi
#
Decay MyJ/psi
  1.00000  mu+        mu-                               PHOTOS VLL ;
Enddecay
#
Decay B_c+sig
  1.00000  MyJ/psi    mu+            nu_mu              PHOTOS BC_VMN 2;
Enddecay
CDecay B_c-sig
#
End
"""
                             ),
                             operates_on_particles = cms.vint32(541, -541), 
                            # list_forced_decays = cms.vstring('MyBc+','MyBc-'),  
                           ),
                           parameterSets = cms.vstring('EvtGen130')
                         ),
                         PythiaParameters = cms.PSet(
                           pythia8CommonSettingsBlock,
                           pythia8CP5SettingsBlock,
                           processParameters = cms.vstring( '541:onMode = off',
                                                           '541:addChannel = 1 1.0 0 443 -13 14',
                                                          ),
                           parameterSets = cms.vstring('pythia8CommonSettings',
                                                       'pythia8CP5Settings',
                                                       'processParameters'
                           )
                        )
)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

bcgenfilter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(443, -13, 14), #J/psi mu+ nu_mu
    MaxEta = cms.untracked.vdouble(999., 999., 999.),
    MinEta = cms.untracked.vdouble(-999., -999., -999.),
    MinPt = cms.untracked.vdouble(0., 0., 0.),
    NumberDaughters = cms.untracked.int32(3),
    ParticleID = cms.untracked.int32(541), # Bc+
    verbose = cms.untracked.int32(0)
)

mumugenfilter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(-13, 13),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
    MinPt = cms.untracked.vdouble(3.5, 3.5),
    MotherID = cms.untracked.int32(541),
    NumberDaughters = cms.untracked.int32(2),
    ParticleID = cms.untracked.int32(443),
    verbose = cms.untracked.int32(0)
)

ProductionFilterSequence = cms.Sequence(generator*bcgenfilter*mumugenfilter)
