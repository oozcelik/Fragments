import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         maxEventsToPrint = cms.untracked.int32(0),
                         filterEfficiency = cms.untracked.double(1.0),
                         comEnergy = cms.double(13000.0),
                         crossSection = cms.untracked.double(540000000.),
          ExternalDecays = cms.PSet(
            EvtGen130 = cms.untracked.PSet(
            operates_on_particles = cms.vint32( 0 ), # 0 (zero) means default list (hardcoded)
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2010_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt.pdl'),
             ),
            parameterSets = cms.vstring('EvtGen130')
          ),
        PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters = cms.vstring(
            'SoftQCD:nonDiffractive = on',            
         ),  
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'processParameters'
                                    )
                  )
         )

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.1 $'),
    name = cms.untracked.string('$Source: Configuration/Generator/python/PHYTIA8_bbbarToMuMu_1.cff_py $'),
    annotation = cms.untracked.string('Spring 2015: Pythia8 generation enriched with b-bbar -> mumu, 13TeV, Tune CUEP8M1')
    )

bbbarfilter = cms.EDFilter("MCParticlePairFilter",
    Status = cms.untracked.vint32(1, 1),
    MinPt = cms.untracked.vdouble(0., 0.),
    MaxEta = cms.untracked.vdouble(9999., 9999.),
    MinEta = cms.untracked.vdouble(-9999., -9999.),
    ParticleID1 = cms.untracked.vint32(5),
    ParticleID2 = cms.untracked.vint32(-5)
)


mumugenfilter  = cms.EDFilter("MCMultiParticleFilter",
    src = cms.InputTag('generator'),   
    Status = cms.vint32(1),
    ParticleID = cms.vint32(13),
    PtMin = cms.vdouble(3.),
    NumRequired = cms.int32(2),
    EtaMax = cms.vdouble(3.),
    AcceptMore = cms.bool(True)
            )
ProductionFilterSequence = cms.Sequence(generator*bbbarfilter*mumugenfilter)
