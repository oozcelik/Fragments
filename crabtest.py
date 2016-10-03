from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

#config.General.requestName = 'tutorial_May2015_MC_generation'
#config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = './BPH-Summer12-00228_1_cfg.py'
config.Data.outputPrimaryDataset = 'MinBias'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 10
NJOBS = 10  # This is not a configuration parameter, but an auxiliary variable that we use in the next line.
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.outLFNDirBase = '/store/user/oozcelik/CRAB_AOUTPUT/X5568TestJobsfromMcM/'
config.Data.publication = True
config.Data.outputDatasetTag = 'CRAB3_tutorial_May2015_MC_generation'
config.Site.storageSite = 'T2_CH_CERN'
