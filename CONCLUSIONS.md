# Conclusions

Eight channels. Zero shadow-life candidates. That was the expected outcome and it
was stated in advance.

What the search actually produced is an account of **why archive-based
shadow-life detection is hard**, and it resolves into three distinct failure
modes. None of them is "we looked and it wasn't there."

## 1. Marker failure — canonical life already does it

| Channel | Proposed shadow marker | Canonical source |
|---|---|---|
| C2 | D-amino acids | peptidoglycan (D-Ala, D-Glu); racemases (D-Asp, D-Ser) |
| C7 | non-protein amino acids | fungal peptaibols (AIB, isovaline) |
| C8 | redox disequilibrium | every microbe on Earth |

The "canonical life" null hypothesis is far wider than shadow-biosphere schemes
assume. They are built against a caricature — twenty protein amino acids, L-only,
phosphate backbone — and the real biosphere routinely operates outside it.

**The prediction this makes:** name a chemical shadow marker, and the first
question is which corner of the known biosphere already produces it. Purely
chemical markers will keep having far less discriminating power than they appear
to.

## 2. Aperture failure — the anomaly is discarded before the archive exists

| Channel | Selection step | Cost |
|---|---|---|
| C1 | cytometry gating | **18.0%** of detected particles (19,303,354 of 107,133,941) dropped from the curated product |
| C5 | SXRF needs an analyst to optically identify a cell before measuring it | a non-cell-shaped particle is never measured; a zero-P cell may be logged as a failed measurement |
| C2 | AAR reports Asx/Glx because they are good clocks | those are exactly the D-forms canonical life already makes |

Every physics-aperture channel examined has a human or algorithmic selection step
upstream of the archive, and it removes precisely the anomalous objects the
channel was chosen to detect. **The discard happens before the dataset exists**,
so no amount of reanalysis recovers it. That is stronger than "the data is
filtered": these archives are structurally incapable of containing the evidence.

## 3. Reference-class failure — the tools separate the wrong things

Every validated agnostic biosignature method separates **biotic from abiotic**.
None separates **our biotic from another biotic**. A shadow biosphere classifies
as "biotic," high confidence, and is filed as unremarkable.

C6a tested whether the flagship classifier had instead memorised canonical
biochemistry, which would mean shadow life gets discarded as geology. It has not:
it generalises across canonical diversity (9.3 pp drop, under the pre-registered
15 pp threshold), so the "filed as unremarkable" branch is the live one.

C8 reaches the same conclusion from thermodynamics. These methods were built for
Mars and Enceladus, where the background hypothesis is *no life* and any positive
is a discovery. Earth's background is *abundant life*.

> **Agnostic biosignatures are agnostic about biochemistry, but not about
> lineage.** On a sterile world that is enough. On Earth, lineage is the whole
> question.

## The one discriminator still standing

**C5's zero-phosphorus test.** Sulfolipid substitution under P limitation
replaces phospholipids, not nucleic acids, so a zero-P cell with normal C and N
has no canonical route. Its null is *structural* rather than chemical, which by
failure mode 1 is exactly the property to select for. It is blocked on data
access, not on logic.

Highest-leverage next action in the whole project: obtain field SXRF per-cell
elemental tables from GEOTRACES EPZT / GeoMICS / IRNBRU. One request, not a
research programme.

## Methodological record

Four of this project's first-pass results did not survive their own controls, and
the controls are the only reason that is known:

1. **C1** — a clean null that also nulled *Prochlorococcus*, whose diel cycle is
   published from that same instrument. Cause: an underway instrument on a moving
   ship yields a space series as much as a time series.
2. **C6a** — a 40.6 pp "MEMORIZATION" verdict that reversed to 9.3 pp
   "generalizes" once domain holdouts were compared against class-matched random
   holdouts instead of raw accuracy.
3. **C6c** — a novelty detector at AUC = 1.000, which was covariance degeneracy;
   the same metric "detected" random held-out labelled samples at 0.956.
4. **The data audit** — a published "3%" figure that counted the wrong quantity
   (exact-filename joinability, not availability). Corrected to ~40%.

The fourth is the instructive one. It was argued to be safer than the others
*because* it was a count rather than an inference. Verifiable is not the same as
verified.

## Honest scope

This does not show that a shadow biosphere is absent. It shows that the archives
searched cannot answer the question, and it identifies what a channel needs to be
worth running: a **structural** null rather than a chemical one, and an archive
whose **selection step does not pre-discard** the target.
