# Pre-registration — locked before any search was run

**Committed 2026-08-18, before any channel produced a result.** Git history is the
proof. Nothing in this file may be edited after the first result lands; corrections
go in `AMENDMENTS.md` with a reason and a timestamp.

The purpose is to make this search falsifiable in advance. Shadow-biosphere claims
have historically failed by choosing the interpretation after seeing the anomaly
(GFAJ-1, nanobes). Every channel below states what would kill it *first*.

---

## Global decision rule

A channel produces a **candidate** only on a **conjunction**: positive in a
physics-aperture measurement AND null in a biology-aperture measurement on the
*same physical sample*. Single-channel anomalies are logged and explicitly not
counted as evidence.

No channel is permitted to report a positive without first passing its own
negative control on canonical organisms.

---

## C1 — Cytometry: periodicity in the discarded gate

**Claim under test:** the scatter-positive / biology-aperture-negative particle
population in ocean cytometry archives behaves like a population rather than a
particle load.

- **Test statistic:** Lomb-Scargle power at 24 h in the unclassified-particle
  time series, after regressing out measured physical forcing (solar irradiance,
  mixed-layer depth, wind stress, salinity, temperature, underway backscatter).
- **Null model:** the residual is white / red noise with no significant 24 h peak.
  Null distribution built by block-bootstrap of the residual series (1000 draws),
  preserving autocorrelation.
- **Threshold:** false-alarm probability < 1e-3 at 24 h, reproduced independently
  in ≥ 3 separate cruises.
- **KILLED IF:** residual 24 h power is not significant, OR the unclassified
  series variance decomposes onto physical forcing at R² > 0.8, OR the same
  diel signal appears in the instrument-bead reference channel (which would
  indicate an instrument artifact, not a population).
- **Known confounds accepted in advance:** sinking/mixing diel cycles, bubble
  injection at wind speed, day-night ship operations, detrital resuspension.

## C2 — Racemization: rate-ordering violation

**Claim under test:** some archived D/L measurements carry a D-excess that does
not follow first-order racemization kinetics.

- **Test statistic:** per-sample, regress observed D/L across amino acids against
  the published Arrhenius rate ordering (Asp > Glu > Ala > Val > Ile). Report the
  residual and the rank correlation between observed excess and known k.
- **Null model:** D-excess is monotonic in k. Racemization predicts rank
  correlation ≈ 1.
- **Threshold:** Spearman rho < 0.3 between excess and rate constant, with the
  anomaly reproduced in independent sub-samples of the same horizon.
- **KILLED IF:** the excess follows the rate ordering, OR the excess is confined
  to peptidoglycan amino acids (D-Ala, D-Glu), OR it is confined to D-Asp and
  D-Ser, which have known biological racemases in canonical life.
- **Restriction stated in advance:** only D-Leu, D-Phe, D-Val, D-alloIle count.

## C3 — Metabolomics: selectivity in vacant formula space

**Claim under test:** untargeted MS archives contain reproducible, high-selectivity
molecular features in a region of formula space vacant for known biochemistry.

- **Test statistic:** for unannotated features, (a) exact-mass formula assignment
  within 3 ppm, (b) position in van Krevelen (H/C, O/C) and Kendrick mass-defect
  space relative to the known-metabolite envelope, (c) isomer count and
  chromatographic peak width as a selectivity proxy, (d) MS2 fragmentation depth
  as an assembly-index proxy.
- **Null model:** unannotated features are drawn from the abiotic degradation
  continuum, which is high-isomer, broad-peak, and smoothly distributed in
  van Krevelen space.
- **Threshold:** a feature cluster that is single-isomer, sharp-peaked, above
  the abundance median, outside the known envelope, and present in ≥ 5 samples
  from ≥ 2 independent studies.
- **KILLED IF:** the feature matches PubChem, CAS, or EPA CompTox (anthropogenic),
  OR maps to any MetaCyc/KEGG pathway, OR fails to reproduce across studies, OR
  its isomer count is consistent with the abiotic continuum.
- **Stated in advance:** anthropogenic contamination is expected to dominate.
  Restriction to pristine matrices (deep subsurface, deep sediment, ice) is part
  of the design, not a post-hoc filter.

## C4 — Raman: activity without canonical bands

**Claim under test:** archived single-cell Raman contains spectra with a C-D
activity band but no phenylalanine and no phosphodiester band.

- **Test statistic:** presence of 2040-2300 cm-1 (C-D) above baseline, with
  absence of 1004 cm-1 (Phe ring breathing) and 1095 cm-1 (PO2- symmetric
  stretch) at matched SNR.
- **Null model:** every metabolically active cell in the archive shows Phe and
  phosphate.
- **Threshold:** band-absence significant at matched signal-to-noise, so that a
  weak-signal spectrum cannot masquerade as a band-absent one.
- **KILLED IF:** any cultured canonical isolate in the same archive scores
  positive under the identical criterion. That would mean the criterion detects
  low SNR, not biochemistry.

## C5 — XRF: phosphorus-free cells

**Claim under test:** archived single-cell elemental datasets contain
carbon/nitrogen-rich, morphologically organized particles with zero phosphorus.

- **Test statistic:** per-cell P quota relative to detection limit, conditioned
  on C and N being present at cellular levels.
- **Null model:** all cells have P above detection because ribosomes require it.
- **Threshold:** P below instrumental detection limit with C and N above the
  25th percentile of the canonical population.
- **KILLED IF:** P-limited oligotrophic populations (SAR11-type sulfolipid
  substitution) reach the same threshold. Low P is known and expected; only
  *zero* P with normal C and N counts.

---

## Controls, also locked in advance

Two deliberately planted, to test whether the ranking machinery works:

1. **Believed false:** arsenic-substituted biomolecules in ICP-MS archives.
   As-O esters hydrolyze in water in seconds; GFAJ-1 collapsed. If this ranks
   competitively with the live channels, the ranking is broken.
2. **Believed already known:** deeply-branching lineages in 16S archives. This is
   microbial dark matter, exhaustively worked since Rinke 2013, and it is
   homology-based, therefore structurally incapable of detecting a second origin.

If the pipeline cannot separate these two from the five live channels, the
pipeline is reported as broken rather than as having found something.

## Prior, stated in advance

We estimate P(extant shadow biosphere) well below 1%. The expected outcome of
this project is a set of negative results and a measured detection limit. That
is the deliverable. A positive would require independent replication before
being described as anything other than an unexplained anomaly.
