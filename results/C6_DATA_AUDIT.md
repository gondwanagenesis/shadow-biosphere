# C6b / C6d — BLOCKED, with a quantified reason

**The agnostic-biosignature classifier literature publishes its labels and its
code, but there is no public crosswalk from either to the deposited raw data.**
Audit run 2026-08-18.

## The numbers

| | |
|---|---|
| Labelled samples in the public ST01 table | **406** |
| Unique raw py-GC-MS files publicly downloadable | **229** |
| Samples with **both** a public label and public raw data | **11 (3%)** |

Deep time, which C6d needs:

| | in label table | with public raw data |
|---|---|---|
| > 541 Ma | 141 | **2** |
| > 2500 Ma (Archean) | 82 | **1** |

Per class, labelled vs. actually usable: Living 153→4, Plant 106→3,
Microbial 87→1, Fossil 131→3, Meteorite 42→1, Synthetic 36→5, Animal 32→**0**.

## What is and isn't public

Everything below is public and was retrieved successfully:

- **Labels**: `PrabhuLab/PyGCMS-Biosign-ML` → `AttributeData/…ST01…xlsx`, 406 rows
  with nine class indicators plus **AGE (Ma)**.
- **Code**: same repo, the R model scripts.
- **Raw data, in three disconnected subsets**: Cleaves 2023 (OSF `EMBH8`, 141
  files), Hystad 16 new files, Slaughter 2025 (79 files), G93CS (10 files).

The gap is the **crosswalk**. The label table indexes samples as `CW001`,
`LIV020`, `RMH0004`, `MET026`. The largest public raw archive — the 141 Cleaves
files — uses descriptive names (`Ecoli13d.txt`, `Allende3d.txt`, `barley3d.txt`).
The table carries a `Cleaves (2023) #` column, but that is an integer index into
the 2023 paper's own SI numbering, and no public file maps those integers to the
descriptive filenames.

Of the 79 Slaughter files, 61 are `MIX-*` — the biotic/abiotic *mixture* samples
from the 2026 Frontiers study, not training samples.

## Being fair about the claim

This is **not** evidence that data was withheld. Many of the 141 Cleaves files
are very likely among the 406 labelled samples, under their older names. The
accurate statement is narrower and still consequential:

> No public artifact links the deposited raw spectra to the published labels, so
> the published models cannot be independently reproduced or audited from public
> data alone.

Resolving it needs one crosswalk file, or a request to the authors.

## Consequence for this project

- **C6b** (shadow conjunction: called BIOTIC, no canonical biomarkers, no
  sequence) — **blocked**. Needs reliable class labels on samples whose raw data
  is in hand. n=11 cannot support it.
- **C6d** (deep time) — **blocked, and worse**. The reframe holds: an *extinct*
  shadow biosphere has a materially higher prior than an extant one, since the
  standard argument against extant life is 4 Gyr of competition, which says
  nothing about a lineage that existed and died on an Earth with no incumbent.
  The label table has 82 Archean samples. **One** has public raw data.
- **C6a** stands, on the 52 filename-reconstructed labels. Its verdict
  (generalizes, 9.3 pp) is unaffected, but its label caveat cannot be removed
  from public data.

## The fourth quantified aperture

C1 measured 18.0% of particles discarded at curation. C2 found AAR archives
report exactly the amino acids that cannot discriminate. C6c found a novelty
metric that hits AUC 1.000 on pure covariance degeneracy.

This is the fourth, and it is the sharpest: **the tool the field trusts most for
biochemistry-independent life detection cannot currently be audited by an
outsider using public data.** For a method whose entire selling point is that it
does not presuppose our biochemistry, whether it has quietly memorized our
biochemistry is exactly the question outsiders should be able to check.
