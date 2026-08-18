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
