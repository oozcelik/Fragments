import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/jhugen/V714/JHUGen_sig4b_0p_slc6_amd64_gcc481_CMSSW_7_1_32.tgz'),
    nEvents = cms.untracked.uint32(1000000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)


from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
    processParameters = cms.vstring(
            'SpaceShower:pTmaxMatch = 1',
            'TimeShower:pTmaxMatch = 1',
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'processParameters',
                                    )
    )
)

lhefilter = cms.EDFilter("LHEGenericFilter",
    src = cms.InputTag("externalLHEProducer"),
    NumRequired = cms.int32(4),
    AcceptLogic = cms.string("LT"),
    ParticleID = cms.vint32(13),
)

ProductionFilterSequence = cms.Sequence(generator*lhefilter)
