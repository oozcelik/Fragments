import FWCore.ParameterSet.Config as cms
from Configuration.Generator.PythiaUEZ2starSettings_cfi import *

generator = cms.EDFilter(
    "Pythia6GeneratorFilter",
    comEnergy = cms.double(8000.0),
    crossSection = cms.untracked.double(48440000000),
    filterEfficiency = cms.untracked.double(5.2e-5),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    ExternalDecays = cms.PSet(
        EvtGen = cms.untracked.PSet(
             operates_on_particles = cms.vint32(511,521,531,5122), # you can put here the list of particles (PDG IDs)
                                                                   # that you want decayed by EvtGen
		                                                   # here is B0, B+/- , B_s0 and Lambda_b0 
             use_default_decay = cms.untracked.bool(False),  # to generate a specific signal mode.
             decay_table = cms.FileInPath('GeneratorInterface/ExternalDecays/data/DECAY_NOLONGLIFE.DEC'),
             particle_property_file = cms.FileInPath('GeneratorInterface/ExternalDecays/data/evt.pdl'),
	     user_decay_embedded= cms.vstring(
	     """
Decay B0
# ------------- semileptonically ----------------------------
0.050100000 D*-     mu+     nu_mu                           PHOTOS HQET 0.77 1.33 0.92;
0.021700000 D-      mu+     nu_mu                           PHOTOS ISGW2;
0.0054   D_1-   mu+  nu_mu           PHOTOS ISGW2;
0.0020   D_0*-   mu+  nu_mu          PHOTOS  ISGW2;
0.0050   D'_1-   mu+  nu_mu          PHOTOS  ISGW2;
0.0022   D_2*-   mu+  nu_mu          PHOTOS  ISGW2;
0.0003   D*-  pi0   mu+  nu_mu       PHOTOS GOITY_ROBERTS;
0.004900000 anti-D*0 pi-     mu+     nu_mu                  PHOTOS     GOITY_ROBERTS;
0.0010   D-   pi0   mu+  nu_mu       PHOTOS GOITY_ROBERTS;
0.0000   anti-D0  pi-   mu+  nu_mu    PHOTOS    GOITY_ROBERTS;
0.000134000 pi-     mu+     nu_mu                           PHOTOS  ISGW2;
0.000247000 rho-    mu+     nu_mu                           PHOTOS  ISGW2;
0.000000   D(2S)- mu+  nu_mu       PHOTOS  ISGW2;
0.000000   D*(2S)- mu+  nu_mu      PHOTOS  ISGW2;
0.001892   Xu-  mu+  nu_mu             VUB 4.8 1.29 0.22 20 0.30 0.55 1.20 0.61 1.26 0.85 1.34 1.08 1.41 1.21 1.48 1.30 1.55 1.30 1.61 1.33 1.67 1.36 1.73 1.39 1.79 1.33 1.84 1.42 1.90 1.39 1.95 1.39 2.00 1.37 2.50 1.30 3.00 0.74 3.50 0.99 4.00 1.09 4.50 1.00;
0.000000450 K0      mu+     mu-                             PHOTOS BTOSLLBALL;
0.000001050 K*0     mu+     mu-                             PHOTOS BTOSLLBALL;
#  ------------- J/psi + X ----------------------------
0.000435500 J/psi   K_S0                                    SVS;
0.000435500 J/psi   K_L0                                    SVS;
0.001330000 J/psi   K*0                                     SVV_HELAMP PKHplus PKphHplus PKHzero PKphHzero PKHminus PKphHminus;
0.000017600 J/psi   pi0                                     SVS;
0.000027000 J/psi   rho0                                    SVV_HELAMP PKHplus PKphHplus PKHzero PKphHzero PKHminus PKphHminus;
0.00003     J/psi  omega            SVV_HELAMP PKHplus PKphHplus PKHzero PKphHzero PKHminus PKphHminus;
0.000000000 J/psi   K+      pi-                             PHSP;
0.0001     J/psi  K0  pi0           PHSP;
0.001300000 J/psi   K_10                                    SVV_HELAMP 0.5 0.0 1.0 0.0 0.5 0.0;
0.0001     J/psi  K'_10             SVV_HELAMP 0.5 0.0 1.0 0.0 0.5 0.0;
0.0005     J/psi  K_2*0              PHSP;
0.000094000 J/psi   phi     K0                              PHSP;
0.000871000 J/psi   K0                                      PHSP;
0.000310000 J/psi   omega   K0                              PHSP;
0.000009500 J/psi   eta                                     PHSP;
0.000019000 J/psi   pi+     pi-                             PHSP;
0.000460000 J/psi   K0      pi+     pi-                     PHSP;
0.000540000 J/psi   K0      rho0                            PHSP;
0.000800000 J/psi   K*+     pi-                             PHSP;
0.000660000 J/psi   K*0     pi+     pi-                     PHSP;
Enddecay
CDecay anti-B0
# 
Decay B-
# --------- semileptonically ----------------
0.056800000 D*0     mu-     anti-nu_mu                      PHOTOS   HQET 0.77 1.33 0.92;
0.022300000 D0      mu-     anti-nu_mu                      PHOTOS   ISGW2;
0.0040   D_10  mu-  anti-nu_mu         PHOTOS   ISGW2;
0.0024   D_0*0  mu-  anti-nu_mu        PHOTOS    ISGW2;
0.0007   D'_10  mu-  anti-nu_mu        PHOTOS    ISGW2;
0.0018   D_2*0  mu-  anti-nu_mu        PHOTOS    ISGW2;
0.006100000 D*+     pi-     mu-     anti-nu_mu              PHOTOS   GOITY_ROBERTS;
0.0003   D*0   pi0   mu-   anti-nu_mu  PHOTOS   GOITY_ROBERTS;
0.0000   D+    pi-   mu-   anti-nu_mu  PHOTOS   GOITY_ROBERTS;
0.0010   D0    pi0   mu-   anti-nu_mu  PHOTOS   GOITY_ROBERTS;
0.000077000 pi0     mu-     anti-nu_mu                      PHOTOS   ISGW2;
0.000037000 eta     mu-     anti-nu_mu                      PHOTOS   ISGW2;
0.000128000 rho0    mu-     anti-nu_mu                      PHOTOS   ISGW2;
0.000115000 omega   mu-     anti-nu_mu                      PHOTOS   ISGW2;
0.000270   eta'   mu-  anti-nu_mu       PHOTOS   ISGW2;
0.000000   D(2S)0 mu-  anti-nu_mu       PHOTOS   ISGW2;
0.000000   D*(2S)0 mu-  anti-nu_mu      PHOTOS   ISGW2;
0.001948   Xu0   mu-  anti-nu_mu         VUB 4.8 1.29 0.22 20 0.30 0.54 1.20 0.95 1.26 0.78 1.34 0.98 1.41 0.91 1.48 1.23 1.55 1.36 1.61 1.39 1.67 1.38 1.73 1.43 1.79 1.41 1.84 1.42 1.90 1.45 1.95 1.40 2.00 1.42 2.50 1.31 3.00 1.36 3.50 1.15 4.00 1.01 4.50 1.51;
0.000000520 K-      mu+     mu-                             PHOTOS BTOSLLBALL;
0.000001160 K*-     mu+     mu-                             PHOTOS BTOSLLBALL;
0.000000   mu-  anti-nu_mu               PHOTOS   SLN;
#  --------- J/psi + X ---------------------
0.001014000 J/psi   K-                                      SVS;
0.001430000 J/psi   K*-                                     SVV_HELAMP PKHminus PKphHminus PKHzero PKphHzero PKHplus PKphHplus;
0.000049000 J/psi   pi-                                     SVS;
0.000050000 J/psi   rho-                                    SVV_HELAMP PKHminus PKphHminus PKHzero PKphHzero PKHplus PKphHplus;
0.0002   J/psi anti-K0   pi-                    PHSP;
0.0001   J/psi K-  pi0                    PHSP;
0.0001   J/psi K'_1-                       SVV_HELAMP 0.5 0.0 1.0 0.0 0.5 0.0;
0.0005   J/psi K_2*-                       PHSP;
0.001800000 J/psi   K_1-                                    SVV_HELAMP 0.5 0.0 1.0 0.0 0.5 0.0;
0.000052000 J/psi   phi     K-                              PHSP;
0.001070000 J/psi   K-      pi-     pi+                     PHSP;
0.000108000 J/psi   eta     K-                              PHSP;
0.000350000 J/psi   omega   K-                              PHSP;
0.000011800 J/psi   anti-p- Lambda0                         PHSP;
Enddecay
CDecay B+
#
Decay B_s0
# --------- semileptonically ----------------
0.0210   D_s-     mu+    nu_mu        PHOTOS  ISGW2;
0.0490   D_s*-    mu+    nu_mu        PHOTOS  ISGW2;
0.0040   D_s1-    mu+    nu_mu        PHOTOS  ISGW2;
0.0040   D_s0*-   mu+    nu_mu        PHOTOS  ISGW2;
0.0070   D'_s1-   mu+    nu_mu        PHOTOS  ISGW2;
0.0070   D_s2*-   mu+    nu_mu        PHOTOS  ISGW2;
0.000200    K-          mu+        nu_mu        PHOTOS  ISGW2;
0.000300    K*-         mu+        nu_mu        PHOTOS  ISGW2;
0.000300    K_1-        mu+        nu_mu        PHOTOS  ISGW2;
0.000200    K'_1-       mu+        nu_mu        PHOTOS  ISGW2;
0.0000000035 mu+        mu-                                PHSP;
0.0000023   phi    mu+    mu-                  BTOSLLALI;
# ------------- J/psi + X -------------------
0.00064     J/psi       eta'                           SVS;
0.00032     J/psi       eta                               SVS;
0.001300000 J/psi   phi                                     SVV_HELAMP  1.0 0.0 1.0 0.0 1.0 0.0;
0.00008     J/psi       K0                           SVS;
0.00070     J/psi       K-          K+                     PHSP;
0.00070     J/psi       anti-K0     K0                     PHSP;
0.00070     J/psi       K0          K-         pi+         PHSP;
0.00070     J/psi       anti-K0     K0         pi0         PHSP;
0.00070     J/psi       K-          K+         pi0         PHSP;
0.00039   J/psi   phi      pi+  pi-  PHSP;
0.00039   J/psi   phi      pi0  pi0  PHSP;
0.0002    J/psi   eta      pi+  pi-  PHSP;
0.0002    J/psi   eta      pi0  pi0  PHSP;
0.0004    J/psi   eta'     pi+  pi-  PHSP;
0.0004    J/psi   eta'     pi0  pi0  PHSP;
0.0002    J/psi   pi+      pi-       PHSP;
0.0002    J/psi   pi0      pi0       PHSP;
Enddecay
CDecay anti-B_s0
#
Decay Lambda_b0
# --------- semileptonically ----------------
0.050000000 Lambda_c+ mu-     anti-nu_mu                    PHSP;
0.006300000 Lambda_c(2593)+ mu-     anti-nu_mu              PHSP;
0.011000000 Lambda_c(2625)+ mu-     anti-nu_mu              PHSP;
  0.00000    Sigma_c0    pi+  mu-  anti-nu_mu             PHSP;
  0.00000    Sigma_c+    pi0  mu-  anti-nu_mu             PHSP;
  0.00000    Sigma_c++   pi-  mu-  anti-nu_mu             PHSP;
  0.00000    Sigma_c*0   pi+  mu-  anti-nu_mu             PHSP;
  0.00000    Sigma_c*+   pi0  mu-  anti-nu_mu             PHSP;
  0.00000    Sigma_c*++  pi-  mu-  anti-nu_mu             PHSP;
0.056000000 Lambda_c+ pi+     pi-     mu-     anti-nu_mu    PHSP;
# ------------ J/psi + X -------------------
  0.00047    Lambda0         J/psi                        PHSP;
Enddecay
CDecay anti-Lambda_b0
#  --------- J/psi --> mu+ mu- wrt to the original BR ----------------
Decay J/psi
0.059300000 mu+     mu-                                     PHOTOS   VLL;
Enddecay
End
	     """
	     ),
             list_forced_decays = cms.vstring() #notice we are actually replacing the decay table to force hadrons decaying to muons.
        ),
        parameterSets = cms.vstring('EvtGen')
    ),
    PythiaParameters = cms.PSet(
    pythiaUESettingsBlock,
        bbbarSettings = cms.vstring('MSEL = 5'), # for b-bbar 
        parameterSets = cms.vstring(
             'pythiaUESettings',
             'bbbarSettings')

    )
    )

FourMuonFilter = cms.EDFilter("FourLepFilter", # require 4-mu in the final state
    MinPt = cms.untracked.double(2.0),
    MaxPt = cms.untracked.double(4000.0),
    MaxEta = cms.untracked.double(2.5),
    MinEta = cms.untracked.double(0.),
    ParticleID = cms.untracked.int32(13)
)

TwoMuonFilter = cms.EDFilter("MCParticlePairFilter",  # require 2-mu mass to be 8.5 - 11.5 GeV
    Status = cms.untracked.vint32(1,1),
    MinPt = cms.untracked.vdouble(2.0,2.0),
    MaxPt = cms.untracked.vdouble(4000.0,4000.0),
    MaxEta = cms.untracked.vdouble( 2.5,2.5),
    MinEta = cms.untracked.vdouble(-2.5,-2.5),
    ParticleID1 = cms.untracked.vint32(13),
    ParticleID2 = cms.untracked.vint32(-13),
    MinInvMass = cms.untracked.double(8.5),
    MaxInvMass = cms.untracked.double(11.5),
)

ProductionFilterSequence = cms.Sequence(generator*FourMuonFilter*TwoMuonFilter)
