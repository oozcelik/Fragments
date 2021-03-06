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
                             particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
                             list_forced_decays = cms.vstring('B_c+sig','B_c-sig'),  
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
Alias      B_c-sig  B_c-
ChargeConj B_c-sig  B_c+sig
Alias      MyJ/psi  J/psi
ChargeConj MyJ/psi  MyJ/psi
#
Decay MyJ/psi
  1.00000  mu+        mu-                               PHOTOS VLL ;
Enddecay
#
Decay B_c+sig
  1.00000  MyJ/psi    mu+            nu_mu              PHOTOS BC_VMN 1;
Enddecay
CDecay B_c-sig
#
End
"""
                             ),
                             operates_on_particles = cms.vint32(541, -541), 
                           ),
                           parameterSets = cms.vstring('EvtGen130')
                         ),
                         PythiaParameters = cms.PSet(
                           pythia8CommonSettingsBlock,
                           pythia8CP5SettingsBlock,
                           processParameters = cms.vstring( 'ProcessLevel:all = off', 
                                                          )
                           parameterSets = cms.vstring('pythia8CommonSettings',
                                                       'pythia8CP5Settings',
                                                       'processParameters'
                           )
                        )
)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

bfilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(9999.0),
    MinEta = cms.untracked.double(-9999.0),
    ParticleID = cms.untracked.int32(541)
)

bcgenfilter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(443, -13, 14), #J/psi mu+ nu_mu
    MaxEta = cms.untracked.vdouble(999., 2.5, 999.),
    MinEta = cms.untracked.vdouble(-999., -2.5, -999.),
    MinPt = cms.untracked.vdouble(-99., 3.5, -99.),
    NumberDaughters = cms.untracked.int32(3),
    ParticleID = cms.untracked.int32(541), # Bc+
    verbose = cms.untracked.int32(0)
)

mumugenfilter = cms.EDFilter("PythiaDauVFilter", # technically, j/psi -> mu+ mu- filter.
    DaughterIDs = cms.untracked.vint32(-13, 13),
    MaxEta = cms.untracked.vdouble(9999., 9999.),
    MinEta = cms.untracked.vdouble(-9999., -9999.),
    MinPt = cms.untracked.vdouble(-99, -99.),
    MotherID = cms.untracked.int32(541),
    NumberDaughters = cms.untracked.int32(2),
    ParticleID = cms.untracked.int32(443),
    verbose = cms.untracked.int32(0)
)

ProductionFilterSequence = cms.Sequence(generator*bfilter*bcgenfilter*mumugenfilter)
