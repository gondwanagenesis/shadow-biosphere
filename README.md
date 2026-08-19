# Shadow Biosphere — an archive-only search

Can a second, independent origin of life on Earth be detected in data that has
already been collected? No new experiments, no new samples. Only archives.

This repository is the search, its pre-registered kill tests, its source audit,
and its results — including the negative ones and one caught methodological
failure.

**Status: all 8 channels resolved — 4 killed, 1 inconclusive, 3 blocked with
specific reasons. Zero shadow-life candidates, as expected. The result is an
account of why archive-based detection fails, in three distinct modes.**
Read [CONCLUSIONS.md](CONCLUSIONS.md) first. See [RESULTS.md](RESULTS.md) and
the adversarial self-audit in [AUDIT.md](AUDIT.md).

---

## The organizing idea

Every assay has an **aperture** (what it physically responds to) and a **filter**
(what it structurally excludes). Split the archives in two:

- **Physics-aperture channels** respond to matter itself — mass and mass defect,
  light scattering, vibrational modes, isotope ratios, elemental composition,
  chirality, heat. These see anything.
- **Biology-aperture channels** respond to homology — PCR, sequencing,
  hybridization, antibodies, culture, nucleic-acid stains. These see only our
  own lineage.

A shadow biosphere is invisible in the second set by construction. So the generic
signature is not "an anomaly" but a **conjunction**: physics-channel positive with
biology-channel null, on the same physical sample, in two or more orthogonal
physics channels. Any single channel has thousands of false positives; orthogonal
ones intersect at nearly zero.

Full reasoning in [METHOD.md](METHOD.md).

## The eight channels

| | Channel | Test | Status |
|---|---|---|---|
| C1 | Cytometry | Does the discarded unclassified particle gate have its own division rhythm? | **KILLED** |
| C2 | Racemization | Is there a D-excess that violates racemization rate ordering? | **KILLED** (underpowered) |
| C3 | Metabolomics | Reproducible high-selectivity molecules in vacant formula space | Blocked on API repair |
| C4 | Raman | Metabolically active cells lacking Phe-1004 and phosphate-1095 bands | Blocked, data not public |
| C5 | Single-cell XRF | Phosphorus-free but C/N-rich cells | **BLOCKED** — the last discriminator standing |
| C6 | Agnostic ML classifier | Called BIOTIC by a validated classifier, but no canonical biomarkers and no sequence | a: generalizes · c: inconclusive · b/d: blocked |
| C7 | Amino-acid alphabet | Selected but on a non-canonical alphabet | **KILLED ON DESIGN** |
| C8 | Electrochemical disequilibrium | Redox inconsistent with abiotic electrochemistry | **KILLED ON DESIGN** |

Channels C6–C8 were added after a literature sweep found the original five missed
a mature body of validated agnostic-biosignature work. See [GAPS.md](GAPS.md).

## Rules this project runs under

1. **Kill tests are written before the search.** [PREREGISTRATION.md](PREREGISTRATION.md)
   was committed before any channel produced a result; git history is the proof.
   Every deviation is logged in [AMENDMENTS.md](AMENDMENTS.md).
2. **Positive controls are gates in code, not claims in prose.** A channel that
   cannot detect a known signal is not allowed to report a null. This caught a
   real error — see below.
3. **Planted controls.** One idea believed false (arsenic biomolecules) and one
   believed already known (deeply-branching 16S) are carried through the ranking.
   If they rank competitively with live channels, the ranking is reported broken.
4. **The prior is low and stated up front.** P(extant shadow biosphere) well
   below 1%. The expected deliverable is negative results plus a measured
   detection limit. A positive would need independent replication before being
   called anything but an unexplained anomaly.

## The most useful thing found so far

Not a shadow-life signal. Two things:

**A measured filter width.** The curated SeaFlow product discards **18.0% of
detected particles** (19,303,354 of 107,133,941) at the curation step, and a user
of the standard product cannot recover them. That is one stage of the aperture,
quantified.

**A near-miss.** The first C1 implementation returned a clean-looking null for
every population. It was wrong — it also nulled *Prochlorococcus*, whose diel
cycle is well established from this very instrument. The cause was that an
underway instrument on a moving ship produces a space series as much as a time
series, and water-mass variance buries the diel band. Only the mandatory positive
control caught it. Without that gate this repository would today contain a
confident, wrong negative result.

## Layout

```
PREREGISTRATION.md      kill tests, locked before any result
AMENDMENTS.md           every deviation, with reasons
METHOD.md               aperture/filter framework, conjunction operator
RESULTS.md              status of all eight channels
GAPS.md                 literature sweep: what the original design missed
AUDIT.md                adversarial self-audit of every test
data_sources/           probe_sources.py + SOURCES.md (36 endpoints audited)
channels/cN_*/          fetch + run scripts per channel
results/                committed derived results
data/raw/               gitignored; re-fetch with the fetch scripts
```

## Reproduce

```bash
pip install numpy pandas scipy duckdb pyarrow astropy openpyxl
python data_sources/probe_sources.py
python channels/c1_cytometry/fetch_c1.py
python channels/c1_cytometry/run_c1.py
```

## Data and credit

All inputs are other people's data, used under their licences and never
vendored here. SeaFlow: Ribalet, Armbrust et al., University of Washington,
CC-BY-4.0, Zenodo [4682238](https://doi.org/10.5281/zenodo.4682238) and
[10896099](https://doi.org/10.5281/zenodo.10896099).

Framing owes to Cleland & Copley (2005) and Davies et al. (2009),
*Signatures of a Shadow Biosphere*, Astrobiology 9:241.
