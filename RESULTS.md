# Results

Run 2026-08-18. Honest status of all five channels, including what was not done.

## Summary

| Channel | Data acquired | Test run | Positive control | Verdict |
|---|---|---|---|---|
| C1 cytometry | ✅ 107M particles, 12 cruises | ✅ | ✅ passed 6/11 | **KILLED** by pre-registered criterion |
| C2 racemization | ✅ 1,380 samples, 10 datasets | ✅ | ✅ rho=+0.80 | **KILLED** (underpowered: 10 informative samples) |
| C3 metabolomics | ⬜ 4 of 8 APIs broken | ⬜ | — | Blocked |
| C4 Raman | ⬜ no public D₂O archive found | ⬜ | — | Blocked |
| C5 single-cell XRF | ⬜ sources audited | ⬜ | — | Not run |
| C6a generalization | ✅ 141 py-GC-MS runs | ✅ | ✅ baseline 0.827 | **GENERALIZES** (9.3 pp; first run said the opposite) |
| C6c residual mining | ✅ same archive | ✅ | ❌ fails by 2 pp | **INCONCLUSIVE** — archive too small |
| C7 amino-acid alphabet | ⬜ | ⬜ | — | Not run |
| C8 electrochemical | ⬜ | ⬜ | — | Not run |

**No channel has produced a shadow-life candidate.**

Running tally of first-pass results that did not survive their controls: **three
of three.** C1's clean null (broken by ship-motion variance), C6a's MEMORIZATION
verdict (broken by class imbalance — the corrected answer was the opposite), and
C6c's perfect AUC=1.000 novelty detector (broken by covariance degeneracy). Every
one looked like a finding. None was.

---

## C1 — KILLED

Full write-up: [results/C1_RESULT.md](results/C1_RESULT.md). Machine-readable:
[results/c1_cytometry.json](results/c1_cytometry.json).

Pre-registered threshold was 24 h periodicity at FAP < 1e-3 in ≥ 3 independent
cruises. **Observed in 1 of 11.** The single positive (DeepDOM) sits at 5.6 h
local solar time against Prochlorococcus at 17.1 h — essentially antiphase, which
is exactly the gate-leakage signature named in advance as the artifact control.

Two things are worth keeping from this channel regardless of the verdict:

**A quantified filter width.** 19,303,354 of 107,133,941 particles (18.0%) carry
`pop = unknown`, and *none* of them survive into the curated SeaFlow v1.6 product.
The aperture is now measured at one stage instead of asserted.

**A caught error.** The first implementation nulled everything, Prochlorococcus
included. That is impossible, and only the mandatory positive control revealed it.
Documented in [AMENDMENTS.md](AMENDMENTS.md).

**Scope narrowing, recorded honestly:** SeaFlow is *unstained*. It classifies by
pigment autofluorescence, so its `unknown` gate is scatter-positive /
pigment-negative — dominated by heterotrophic bacteria and detritus. The test as
designed needs DNA-stained benchtop cytometry. BATS, the natural source, returned
HTTP 522 for the whole run. **C1 as executed is a weaker test than C1 as
designed, and the designed version remains open.**

## C2 — KILLED (underpowered)

Full write-up: [results/C2_RESULT.md](results/C2_RESULT.md).

1,380 samples across 10 datasets. Positive control passed at median rho = +0.80,
and 100% of samples in the two widest-suite datasets follow racemization
kinetics. **Zero qualifying violations.**

The kill is weak and the reason is the finding. The pre-registration restricted
qualifying violations to D-Leu, D-Val, D-Ile and D-Phe, because D-Ala and D-Glu
come from peptidoglycan and D-Asp and D-Ser have canonical racemases. **Only 10
of 1,380 samples carry two or more of those informative amino acids.** The
1,370-sample dataset reports only canonically-producible D forms, so it cannot
support a shadow reading whatever it shows; its 35 rate-ordering violations were
excluded by the pre-registered restriction rather than by judgement.

**Second measured aperture.** AAR archives are structurally near-blind to this
test. The field measures Asx and Glx because they are good Quaternary clocks, and
those are exactly the amino acids whose D forms canonical life already makes. The
slow racemizers that would carry an unambiguous signal are rarely reported
because they are poor clocks. The archive is optimized against the measurement
this channel needs.

## C3 — blocked

MassIVE PROXI returns 400 on documented parameters, GNPS2's API path 404s,
Metabolomics Workbench times out on the all-studies query, BioCyc needs a
subscription. MetaboLights, PubChem and EPA CompTox all work, so the *kill
filters* are ready before the *search corpus* is. Needs API repair plus large
downloads.

## C4 — blocked

No public archive of D₂O-labelled single-cell Raman was found at usable scale.
Nine Zenodo records and ten figshare records for related queries, none of them a
labelled spectral corpus. This is the highest-specificity channel and the most
data-starved. Realistically needs direct request to the groups that generated it.

## C5 — not run

PANGAEA returns 7 nanoSIMS single-cell hits. BCO-DMO surfaced *Single-cell
Synechococcus WH8102 XRMA elemental data*, which is a culture experiment and
therefore useful as a **canonical-P reference distribution** rather than as an
environmental search set. Acquisition path is clear; the run was not done.

---

## Meta-finding

The lineage-free measurement channels are exactly the ones with the weakest
public data infrastructure. The homology-based channels — sequence archives — are
enormous, indexed, API-first and free. The physics-aperture channels that could
in principle see a second origin are scattered, unindexed, or private.

If the goal were to make a shadow-biosphere search actually possible, the highest
-leverage action is not a new instrument. It is persuading cytometry, Raman and
single-cell elemental programmes to publish their **discarded** categories.

## Controls

Both planted controls behaved as intended and were correctly separated from the
live channels: arsenic-substituted biomolecules (believed false) and
deeply-branching 16S lineages (believed already known, and structurally incapable
of detecting a second origin because it is homology-based). The ranking
machinery is not obviously broken.
