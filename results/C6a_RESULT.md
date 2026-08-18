# C6a — Does "agnostic" generalize?

**Verdict: GENERALIZES across canonical diversity — no domain effect beyond class
imbalance. Underpowered (n=52).** Run 2026-08-18.

Data: Cleaves et al. 2023, OSF `EMBH8`. 141 py-GC-MS scan × m/z matrices,
52 confidently labelled, 18 fossil organic held out, 71 excluded as ambiguous.

## Why this test exists

Every published agnostic biotic/abiotic classifier trains its biotic class
entirely on canonical Earth life, so the learned boundary is "canonical-life-like
vs abiotic," not "life vs non-life." The two possibilities predict **opposite**
shadow searches:

- generalizes → shadow life reads BIOTIC → filed as unremarkable
- memorized → shadow life reads ABIOTIC → **actively discarded as geology**

## Result

| Domain held out | n | class | domain recall | matched-random | delta | pctile |
|---|---|---|---|---|---|---|
| animal | 5 | biotic | 0.400 | 0.680 | −0.280 | 0.12 |
| microbial | 8 | biotic | 0.500 | 0.670 | −0.170 | 0.18 |
| plant | 11 | biotic | 0.818 | 0.647 | **+0.171** | 1.00 |
| synthetic | 26 | abiotic | 0.000 | 0.001 | −0.001 | 0.98 |

Baseline random 5-fold accuracy 0.827 (positive control passed).
Mean delta on held-out biotic domains **−0.093**, i.e. **9.3 pp**, below the
pre-registered 15 pp memorization threshold.

## The correction that changed the answer

**Run 1 reported a 40.6 pp drop and the verdict MEMORIZATION.** That was an
artifact and the conclusion was backwards.

Holding out an entire domain makes the test set single-class *and* skews training
balance. Holding out the 26 synthetic abiotic samples leaves 24 biotic against 2
abiotic, so the model predicts biotic for everything and scores 0.000 on an
all-abiotic test set. That measures imbalance, not domain generalisation.

The fix compares each domain holdout against **size- and class-matched random
holdouts** — same size, same class, same induced imbalance, no domain structure.
Only the gap is a domain effect. Under that control the synthetic holdout's
catastrophic 0.000 has a matched-random value of 0.001: delta ≈ 0, no domain
effect whatsoever.

This is the **second** time in this project a striking result dissolved under a
proper control, after C1's false null. Both would have been reported as findings.

## What it means for the shadow search

The C6b premise holds: the classifier does not collapse on unseen canonical
domains, so a shadow biosphere would most likely classify **BIOTIC** and be filed
as unremarkable rather than discarded. The conjunction search — called BIOTIC,
no canonical biomarkers, no amplifiable sequence — is the right next move.

## Limitations, stated plainly

- **n = 52 labelled (24 biotic).** Very small. `animal` (pctile 0.12) and
  `microbial` (0.18) sit in the lower tail; a larger sample could move this.
- **Labels are reconstructed from filenames.** The OSF deposit ships no label
  file. 71 samples were excluded rather than guessed.
- The featurization is my own (normalized m/z spectrum + 8 retention-time-binned
  spectra + chromatogram shape), not the paper's exact pipeline. Baseline 0.827
  is close to their reported ~0.90 but not identical.
