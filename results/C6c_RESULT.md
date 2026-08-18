# C6c — Residual mining: can a third class be detected at all?

**Verdict: INCONCLUSIVE — marginal power, fails its pre-registered gate by 2 pp.**
Run 2026-08-18.

## Design

A third class would not show up as accuracy loss. It shows up as samples
classified **confidently** that sit **far from everything the model was trained
on** — the model extrapolating. That is exactly what shadow life looks like to a
classifier trained only on our lineage.

**Positive control:** the archive contains a *real* third class — 18 geologically
processed fossil organic samples, biotic in origin but abiotic-like in
processing, deliberately excluded from the binary. If the method cannot recover
those, it has no power to recover an unknown third class.

## Result

| Gate | Threshold | Observed | |
|---|---|---|---|
| novelty AUC, fossil vs labelled | > 0.75 | **0.781** | pass |
| real-novelty gap vs degeneracy | > 0.15 | **0.247** | pass |
| fossils flagged confident+novel | > 0.30 | **0.28** | **fail** |

Two of three gates pass. The flag rate misses by 2 percentage points. The
threshold was set before the run, so it stands. **Nothing is interpreted and no
ambiguous sample is reported as a candidate.**

## The methodological finding: a novelty-detection trap

Sweeping novelty metrics against the fossil control produced an apparently
perfect result — **Mahalanobis distance at 40 principal components, AUC = 1.000.**

It was degeneracy. With 52 labelled samples, a covariance matrix estimated in 40
dimensions is near-singular, so *any* point outside the fit gets a huge distance.
The tell was that AUC rose monotonically with dimension (0.781 → 0.749 → 0.821 →
0.886 → 1.000) exactly as p approached n.

The check: does the same metric separate **random held-out labelled samples**,
which are not novel at all?

| n PCs | AUC fossil vs labelled | AUC *random labelled* holdout |
|---|---|---|
| 5 | 0.781 | **0.534** |
| 15 | 0.821 | 0.667 |
| 25 | 0.886 | 0.888 |
| 40 | **1.000** | **0.956** |

At 40 PCs it separates random labelled samples nearly as well as fossils. It was
detecting "not in the covariance fit," not "novel." Only 5 PCs shows a real gap
(0.247), so that is the operating point, and the degeneracy check is now a
permanent second gate in the code.

**Anyone applying novelty detection to agnostic biosignature work can hit this,
and it presents as a spectacular positive.**

## What limits this

`n = 52` labelled samples, throughout. Fossil organics are chemically *very*
distinct from both fresh biomass and pure synthetics, and the method still only
reaches AUC 0.781 on them. A shadow biosphere would presumably be subtler. The
honest read is that this archive is too small for residual mining, not that
residual mining is a bad idea.
