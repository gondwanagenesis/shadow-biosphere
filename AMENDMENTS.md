# Amendments to the pre-registration

Every deviation from `PREREGISTRATION.md` is logged here with a reason and a
date. The pre-registration itself is never edited.

---

## 2026-08-18 — C1 artifact control substituted

**Pre-registered:** "KILLED IF ... the same diel signal appears in the
instrument-bead reference channel."

**Problem:** the published SeaFlow archive has already removed calibration beads.
The named control does not exist in the data.

**Substitute:** phase relationship to the classified populations. Gate leakage
from *Prochlorococcus* — whose cell size has a large diel cycle — would place the
`unknown` population at a phase locked to (specifically, antiphase with)
prochloro size. An independent population has no reason to share that phase.

**Effect on the result:** this made the test *stricter*, not weaker. The one
cruise that passed the periodicity threshold was then killed by this control.

---

## 2026-08-18 — C1 scope narrowed: SeaFlow is unstained

**Pre-registered assumption:** the target population is "scatter-positive,
DNA-stain-negative."

**Problem:** SeaFlow is an underway instrument that classifies by pigment
autofluorescence, not by a DNA stain. Its `unknown` gate is scatter-positive /
*pigment*-negative, which is dominated by heterotrophic bacteria and detritus.

**Effect:** C1 as run tests a weaker proposition than designed. The designed test
needs stained benchtop cytometry (BATS / HOT / Tara). BATS was unreachable
(HTTP 522) during this run. This is recorded as an open gap, not as completed
coverage.

---

## 2026-08-18 — C1 analysis method corrected mid-run

**What happened:** the first implementation ran the periodogram on the raw hourly
series and returned FAP = 1.0 for every population, including *Prochlorococcus*,
whose diel cycle is well established from this very instrument.

**Diagnosis:** SeaFlow is underway on a moving ship, so the series is a space
series as much as a time series. Water-mass variance sits at low frequency,
dominates the periodogram normalisation, and buries the diel band.

**Fix:** regular hourly grid, 49 h centred rolling-median high-pass, and a
mandatory positive-control gate that refuses to interpret any result unless
Prochlorococcus forward scatter shows 24 h power in ≥ 3 cruises.

**Why this is logged prominently:** version 1 would have been written up as a
clean null result. It was wrong. The positive control is the only reason that
was caught, which is the strongest argument in this whole project for keeping
mandatory controls inside the code rather than in the write-up.

---

## 2026-08-18 — three channels ADDED after a literature sweep

**What happened:** a sweep of the shadow-biosphere and agnostic-biosignature
literature (see `GAPS.md`) found that the original five channels missed a mature
body of validated work, including biotic/abiotic classifiers with publicly
deposited training data.

**Added:**

- **C6** — agnostic ML classifier inverted for the shadow conjunction. Every
  published agnostic classifier separates biotic from abiotic; none separates our
  biotic from another biotic. The shadow query is: called BIOTIC with high
  confidence, no canonical biomarkers, no amplifiable sequence.
- **C7** — non-protein amino-acid alphabet. Named explicitly by Davies et al.
  (2009) and runs on the same archived GC-MS data C2 already used.
- **C8** — electrochemical disequilibrium / energy transfer, closing the two
  Laboratory for Agnostic Biosignatures pillars the original design left open.

**Why this is an amendment and not a rewrite:** the original five pre-registered
kill tests stand unchanged and their verdicts are unaffected. C6–C8 get their own
pre-registered kill tests in `PREREGISTRATION_C6_C8.md`, to be committed before
any of them is run, under the same rule as the original.

**Honest note:** C6 is a stronger channel than anything in the original set,
because it inherits a validated classifier and a published positive control
instead of requiring both to be built and defended here. The original design's
contribution is the conjunction operator, not the individual channels.

---

## 2026-08-18 — C6a method corrected mid-run, verdict reversed

**What happened:** the first implementation compared domain-holdout accuracy
directly against random-fold accuracy, found a 40.6 pp drop, and returned the
verdict MEMORIZATION — that published agnostic classifiers have memorized
canonical biochemistry and would discard shadow life as geology.

**Diagnosis:** artifact. Holding out an entire domain makes the test set
single-class and skews training class balance. Holding out 26 synthetic abiotic
samples leaves 24 biotic vs 2 abiotic, so the model predicts biotic for
everything and scores 0.000 on an all-abiotic test set. The metric was measuring
class imbalance, not domain generalisation.

**Fix:** each domain holdout is now compared against size- and class-matched
random holdouts, which carry the identical induced imbalance but no domain
structure. Only the delta is interpreted. Classifier uses balanced class weights.

**Effect:** verdict REVERSED, from MEMORIZATION (40.6 pp) to GENERALIZES
(9.3 pp, under the pre-registered 15 pp threshold). The synthetic holdout's
0.000 has a matched-random value of 0.001 — delta ~0, no domain effect at all.

**Note:** the pre-registered positive control (baseline > 0.80) PASSED in both
versions and did not catch this. That is a real limitation of that gate: it
verifies sensitivity, not metric validity. Second instance in this project of a
striking result dissolving under a proper control.
