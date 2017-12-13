import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         comEnergy = cms.double(13000.0),
                         crossSection = cms.untracked.double(54000000000),
                         filterEfficiency = cms.untracked.double(3.0e-4),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         maxEventsToPrint = cms.untracked.int32(0),
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            #user_decay_file = cms.vstring('GeneratorInterface/ExternalDecays/data/Bs_Jpsiphi.dec'),
            user_decay_embedded= cms.vstring(
'# This is the decay file for the decay BS0 -> PSI(-> MU+ MU-) PHI(-> K+ K-)',
'# EventType: 13144001',
'# Descriptor: [B_s0 -> (J/psi(1S) -> mu+ mu- {,gamma} {,gamma}) (phi(1020) -> K+ K-)]cc',
'# NickName: Bs_Jpsiphi,mm=CPV',
'# Physics: Includes radiative mode, CP violation, different lifetimes',
'#',
'# Tested: Yes',
'# By: Gerhard Raven / Tristan du Pree',
'# Date: 10 Oct 2006',
'#',
'Define Hp 0.49',
'Define Hz 0.775',
'Define Hm 0.4',
'Define pHp 2.50',
'Define pHz 0.0',
'Define pHm -0.17',
'# Overriding dgammas to zero for Giacomo Fedis analysis',
'Define dgammas 0',
'#yesIncoherentBsMixing dms dgammas',
'#',
'Alias      MyB_s0   B_s0',
'Alias      Myanti-B_s0   anti-B_s0',
'ChargeConj Myanti-B_s0   MyB_s0', 
'Alias      MyJ/psi  J/psi',
'Alias      MyPhi    phi',
'ChargeConj MyJ/psi  MyJ/psi',
'ChargeConj MyPhi    MyPhi',
'#',
'Decay MyB_s0',
  '1.000         MyJ/psi     MyPhi        PVV_CPLH 0.02 1 Hp pHp Hz pHz Hm pHm;',
'#',
'Enddecay',
'Decay Myanti-B_s0',
  '1.000         MyJ/psi     MyPhi        PVV_CPLH 0.02 1 Hp pHp Hz pHz Hm pHm;',
'Enddecay',
'#',
'Decay MyJ/psi',
  '1.000         mu+         mu-          PHOTOS VLL;',
'Enddecay',
'#',
'Decay MyPhi',
  '1.000         K+          K-           VSS;',
'Enddecay',
'End'),
            list_forced_decays = cms.vstring('MyB_s0','Myanti-B_s0'),
            operates_on_particles = cms.vint32()
            ),
        parameterSets = cms.vstring('EvtGen130')
        ),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(             
            'HardQCD:all = on',
            'PhaseSpace:pTHatMin = 8.', 
             ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
        )
                         )

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)


#ProductionFilterSequence = cms.Sequence(generator*MuMuFilter*MuFilter)

###########
# Filters #
###########
# Filter only pp events which produce a Bs:
bsfilter = cms.EDFilter("PythiaFilter", ParticleID = cms.untracked.int32(531))

jpsifilter = cms.EDFilter("PythiaDauVFilter",
        verbose         = cms.untracked.int32(0), 
        NumberDaughters = cms.untracked.int32(2), 
        MotherID        = cms.untracked.int32(531),  
        ParticleID      = cms.untracked.int32(443),  
        DaughterIDs     = cms.untracked.vint32(13, -13),
        MinPt           = cms.untracked.vdouble(2.8, 2.8), 
        MinEta          = cms.untracked.vdouble(-2.4, -2.4), 
        MaxEta          = cms.untracked.vdouble( 2.4,  2.4)
        )


ProductionFilterSequence = cms.Sequence(generator*bsfilter*jpsifilter)                     

    
