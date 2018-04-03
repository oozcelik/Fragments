import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring('MyB0','Myanti-B0'),
            operates_on_particles = cms.vint32(),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
# B0_muDstar_D0pi_Kpi.dec
#
# This is the decay file for the decay B0->mu-D*+ -> mu-D0(K-pi+) pi+
#
Alias      MyB0   B0
Alias      Myanti-B0   anti-B0
ChargeConj Myanti-B0   MyB0
Alias      MyD0   D0
Alias      Myanti-D0   anti-D0
ChargeConj Myanti-D0   MyD0
Alias      MyD*+  D*+
Alias      MyD*-  D*-
ChargeConj MyD*-  MyD*+
#
Decay MyB0
1.000    MyD*+ mu-       PHSP;
Enddecay
CDecay Myanti-B0
#
Decay MyD*+
1.000    MyD0  pi+       VSS;
Enddecay
CDecay MyD*-
#
Decay MyD0
1.000   K-  pi+         PHSP;
Enddecay
CDecay Myanti-D0
#
End
"""
            )
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring('SoftQCD:nonDiffractive = on'
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)

###### Filters ##########
bfilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(9999.),
    MinEta = cms.untracked.double(-9999.),
    MinPt = cms.untracked.double(0.),
    ParticleID = cms.untracked.int32(511) # B0
)

decayfilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1),
    NumberDaughters = cms.untracked.int32(2),
    ParticleID      = cms.untracked.int32(511),  ## B0
    DaughterIDs     = cms.untracked.vint32(413, 13), ## D∗(2010)+ mu-
    MinPt           = cms.untracked.vdouble(-1., -1.),
    MinEta          = cms.untracked.vdouble(-9999., -9999.),
    MaxEta          = cms.untracked.vdouble( 9999.,  9999.)
)

dstarfilter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(421, 211), # D0 pi
    MaxEta = cms.untracked.vdouble(9999.0, 9999.0),
    MinEta = cms.untracked.vdouble(-9999.0, -9999.0),
    MinPt = cms.untracked.vdouble(-1.,-1.),
    MotherID = cms.untracked.int32(511), ## B0
    NumberDaughters = cms.untracked.int32(2),
    ParticleID = cms.untracked.int32(413), ##  D∗(2010)+
    verbose = cms.untracked.int32(1)
)
d0filter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(-321, 211), # K- pi+
    MaxEta = cms.untracked.vdouble(9999.0, 9999.0),
    MinEta = cms.untracked.vdouble(-9999.0, -9999.0),
    MinPt = cms.untracked.vdouble(-1.,-1.),
    MotherID = cms.untracked.int32(413),
    NumberDaughters = cms.untracked.int32(2),
    ParticleID = cms.untracked.int32(421), # D0
    verbose = cms.untracked.int32(1)
)

muFilter = cms.EDFilter("MCMultiParticleFilter",
            src = cms.untracked.InputTag("generator","unsmeared"),
            Status = cms.vint32(1),
            ParticleID = cms.vint32(13),
            PtMin = cms.vdouble(0.),
            NumRequired = cms.int32(2),
            EtaMax = cms.vdouble(999.),
            AcceptMore = cms.bool(True)
            )

ProductionFilterSequence = cms.Sequence(generator*bfilter*decayfilter*dstarfilter*d0filter*muFilter)
