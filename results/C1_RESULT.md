# C1 — Cytometry: the discarded `unknown` gate

**Verdict: KILLED by its own pre-registered criterion.**
Run 2026-08-18. Data: SeaFlow per-particle optical archive, Zenodo
[4682238](https://doi.org/10.5281/zenodo.4682238), CC-BY-4.0.

---

## What the archive actually contains

| | |
|---|---|
| Cruises | 12 |
| Particles (10% published subsample) | 107,133,941 |
| `pop = unknown` particles | **19,303,354 (18.0%)** |
| `unknown` retained in curated SeaFlow v1.6 product | **none** |

The curated product ([Zenodo 10896099](https://doi.org/10.5281/zenodo.10896099))
publishes abundance, diameter, carbon quota and biomass for exactly four named
populations: *Prochlorococcus*, *Synechococcus*, picoeukaryotes, *Crocosphaera*.
There is no unclassified, unknown, detrital or bead variable in it.

So the filter-stack thesis is confirmed as a matter of fact, independent of
whether shadow life exists: **18% of detected particles are discarded at the
curation step**, and a user of the standard product cannot recover them. That
is a real, citable measurement of one stage of the aperture.

## Positive control (gate on interpretability)

Prochlorococcus mean forward scatter must show 24 h power, since its cell-size
diel cycle is large and repeatedly published from this instrument.

**6 of 11 cruises pass at FAP < 1e-3.** DeepDOM: FAP = 1.0e-54, peak period
24.0 h, phase 17.1 h local solar time — a late-afternoon size maximum ahead of
dusk division, which is the expected phase. The pipeline has real sensitivity.

The five failing cruises are short (169–302 usable hours) or coastal, where
water-mass variance dominates. They are reported, not dropped.

> **Method correction, logged.** The first implementation returned FAP = 1.0 for
> *every* population including Prochlorococcus. That was a broken analysis, not a
> null result. SeaFlow is an underway instrument on a moving ship, so the record
> is a space series as much as a time series, and low-frequency water-mass
> variance buried the diel band. Fixed with a 49 h high-pass and a regular hourly
> grid. **The first version's apparent null would have been reported as a
> negative result had the positive control not caught it.** This is the single
> most important methodological lesson from the run.

## Result for the `unknown` population

Pre-registered threshold: FAP < 1e-3 at 24 h, **reproduced in ≥ 3 independent
cruises**.

**Observed: 1 of 11 cruises.** Only DeepDOM (abundance FAP = 2.3e-05,
forward-scatter FAP = 1.2e-07, peak period 23.9 h). Every other cruise fails,
most at FAP = 1.0.

The threshold is not met. **C1 is killed.**

## The single positive is explained by the pre-registered artifact control

On DeepDOM, the `unknown` diel phase is **5.6 h** local solar time against
Prochlorococcus at **17.1 h** — 11.5 h apart, essentially antiphase.

That is precisely the gate-leakage signature specified in advance. Prochlorococcus
cells are largest in late afternoon and smallest after dusk division; when they
are smallest, a fraction falls below the classification boundary and lands in
`unknown`. So `unknown` should peak when prochloro size is at minimum — early
morning. It does, at 5.6 h.

The one cruise showing a signal shows it with the exact phase the artifact
hypothesis predicts. This is a clean kill, not an ambiguous one.

## AUDIT ADDENDUM (2026-08-19) — control asymmetry, and a measured detection limit

Two things surfaced in the post-hoc audit (`AUDIT.md`, A3 and A4).

**Problem found.** The pre-registered gate validates the *mean forward scatter*
channel (6/11 cruises). But the headline result above is carried by the
*abundance-fraction* channel, and Prochlorococcus abundance passes that same gate
in only **2 of 11 cruises** — below the pre-registered threshold of 3. The channel
carrying the reported null did not meet the project's own validation bar, and
that was not noticed when this file was first written.

**Resolved by injection recovery, not by argument.** A synthetic 24 h signal of
known amplitude and phase was injected into the real unknown-fraction series
(`channels/c1_cytometry/audit_injection.py`):

| injected amplitude | recovered at 24.0 h, FAP < 1e-3 |
|---|---|
| 0.50 x series sd | **6 / 6 cruises** |
| 0.25 x series sd | **5 / 6 cruises** |
| 0.10 x series sd | 2 / 6 cruises |

Phase error < 2 h in every recovered case. The abundance channel has real
sensitivity. This is a stronger validation than the original gate because it
tests the exact channel and statistic used for the reported result.

**The null is therefore quantified, not assumed:**

> C1 found no diel signal in the discarded gate **above about 0.25 x the series
> standard deviation**. It is not sensitive to signals at 0.10 x sd.

## What this does and does not establish

It establishes that the discarded SeaFlow gate does not behave like an
independent population with its own division rhythm, across 12 cruises and 19.3
million particles.

It does **not** test the assay described in the original design. SeaFlow is an
**unstained** instrument: it classifies by pigment autofluorescence (chlorophyll,
phycoerythrin), not by a DNA stain. Its `unknown` gate is therefore
scatter-positive / *pigment*-negative, a category dominated by heterotrophic
bacteria and detritus. The intended test — scatter-positive / *DNA-stain*-negative
— requires stained cytometry (BATS, HOT, or Tara benchtop FCM). BATS was
unreachable during this run (HTTP 522). See `data_sources/SOURCES.md`.

This distinction was not in the original plan and is a genuine narrowing of what
C1 covers. It is recorded here rather than glossed.

## Reproduce

```bash
python channels/c1_cytometry/fetch_c1.py
python channels/c1_cytometry/run_c1.py
```
