# C6b / C6d — blocked, with a CORRECTED reason

> **This file was rewritten on 2026-08-18 after its first version was checked and
> found wrong.** The original claimed "only 11 of 406 labelled samples (3%) have
> public raw data" and that "no public artifact links deposited spectra to
> published labels." Both statements were overstated. Corrected figures below;
> the error is logged in `AMENDMENTS.md`.

## What the first version got wrong

The 3% figure came from **automated exact-filename matching** between the label
table and the downloaded files. That measures whether the two join *without
human effort*. It does not measure whether the data is available.

Two things it missed:

1. **A partial crosswalk IS derivable from public data.** The label table has a
   `Description` column, and the Cleaves deposit uses descriptive filenames.
   `asphltmm`→asphaltum, `metseqah`→metasequoia, `torbanit`→torbanite,
   `cannelco`→cannel coal are unambiguous. About 17 match at a strict automated
   threshold.
2. **The `Source` column exists and is more complete** than the
   `Cleaves (2023) #` column I keyed on. It shows **135 of 406** samples come
   from the Cleaves collection, not 54.

## Corrected numbers

| | |
|---|---|
| Labelled samples in the public ST01 table | 406 |
| From the **Cleaves** collection (141 raw files public) | **135 (33%)** |
| From other collections (Cody 47, Summons 38, Hazen 32, Knoll 29, Alexander 19, Saul 18, Boyce 16, …) | **271 (67%)** |
| Public raw spectra for those other collections | **~28** (10 in OSF G93CS + 18 non-MIX Slaughter files) |
| **Best-case obtainable with manual name reconciliation** | **~160 of 406 (~40%)** |

Deep time, which C6d needs:

| | |
|---|---|
| Archean samples (>2500 Ma) in the label table | 82 |
| Of those, from the Cleaves collection | **6** |

## The corrected finding

The reproducibility gap is real but narrower and differently located than first
stated:

> Roughly **two-thirds of the training set's raw spectra are not publicly
> deposited**, concentrated in the newer non-Cleaves collections. The Archean
> subset — the part most relevant to a deep-time search — is almost entirely in
> that undeposited majority (6 of 82 from the collection whose data is public).

And a softer, still-true point about the part that *is* public: linking it to the
labels requires name reconciliation through the `Description` column, which is
error-prone. Fuzzy matching produces confident false pairs — `ecoli1`→coal,
`citron`→chitin, `collagen`→coal slag, `hair`→haircap moss. Anyone reconstructing
this crosswalk automatically will introduce label noise without noticing.

## What is not claimed

Not that data was withheld. Not that the papers are wrong. Not that the models
are unreliable. The deposits that exist are real, public, and were retrieved
successfully here. This is an observation about how much of a 406-sample training
set an outsider can reassemble, and the answer is roughly 40% with effort rather
than the 3% first reported.

## Consequence for this project

- **C6b** — still blocked. ~160 reconstructable samples with noisy labels is not
  a sound basis for a conjunction search, though it is far better than 11.
- **C6d** — still blocked, and this is the firmer half of the finding. 6 of 82
  Archean samples have public raw data.
- **C6a** — unaffected.

## Reproduce this audit

```
gh repo clone PrabhuLab/PyGCMS-Biosign-ML
# AttributeData/2025-WongPrabhu-SupllementaryTable-ST01-07MAY.xlsx  -> 406 rows
# Source column: Cleaves 135, Cody 47, Summons 38, Hazen 32, Knoll 29, ...
# OSF EMBH8 -> 141 raw files;  OSF G93CS -> 10 raw files
```
