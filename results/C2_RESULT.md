# C2 — Racemization: rate-ordering violation

**Verdict: KILLED — but underpowered, and the reason it is underpowered is itself
the finding.** Run 2026-08-18.

Data: 9 PANGAEA amino-acid racemization datasets + 1 Zenodo dataset.
Machine-readable output: [results/c2_racemization.json](c2_racemization.json).

---

## The test

Racemization is first-order with a strict measured rate ordering across amino
acids (Asx fastest → Ile slowest). Diagenetic D-excess must respect that
ordering. A D-excess from a biology that uses D-amino acids has no reason to.
So the discriminator sits *inside each sample*: rank the measured D/L values and
ask whether they follow kinetics.

## Positive control — PASSED

Racemization is real and dominant in fossil biominerals, so the pipeline must
recover the ordering in ordinary samples.

**Median per-dataset rho = +0.80.** In the two datasets carrying the widest
amino-acid suites, **100% of samples follow kinetics**. The pipeline detects the
ordering it is testing against.

## Result

| Dataset | n | Amino acids | median rho | follow kinetics | violations on clean AAs |
|---|---|---|---|---|---|
| pangaea_808545 | 4 | ala, asp, leu, val | +0.80 | 100% | 0 |
| pangaea_888699 | 6 | ala, asp, glu, ile, leu, val | +0.85 | 100% | 0 |
| pangaea_901651 | 1370 | ala, asp, glu, ser | +0.60 | 97% | 0 |

1,380 samples examined. **Zero qualifying violations.** C2 is killed.

## Why the kill is weak, and why that matters more

The pre-registration restricted qualifying violations to **D-Leu, D-Val, D-Ile,
D-Phe** — the amino acids canonical life does *not* routinely produce in D form.
D-Ala and D-Glu come from peptidoglycan; D-Asp and D-Ser have known racemases in
canonical life. A D-excess in those four proves nothing.

**Only 10 of the 1,380 samples carry two or more of the informative amino
acids.** The 1,370-sample dataset reports Asx, Glx, Ser and Ala — every one of
them canonically producible — so it cannot support a shadow-life reading no
matter what it shows. Its 35 rate-ordering violations were correctly excluded by
the pre-registered restriction, not by post-hoc judgement.

So the honest statement is: *no violation was found, in a search with very little
power.*

## The actual finding: another measured aperture

**Amino-acid racemization archives are structurally near-blind to this test.**
The field measures Asx and Glx because they racemize fast enough to be useful
geochronometers on Quaternary timescales. Those are precisely the amino acids
whose D forms canonical life already makes. The slow racemizers that would carry
an unambiguous signal — Leu, Val, Ile, Phe — are rarely reported because they are
poor clocks.

The archive is optimized against the very measurement this channel needs. That is
a second quantified instance of the filter-stack thesis, after C1's 18%.

## What would give this channel real power

1. Datasets reporting the **full amino-acid suite** including Leu/Val/Ile/Phe.
   These exist in the analytical literature but are not the geochronology
   mainstream.
2. The **rejected-sample archive**: AAR labs routinely flag anomalous D/L as
   "contaminated" or "diagenetically altered" and set it aside. That is a
   pre-built archive of exactly the anomalies this test wants, and it is largely
   in lab notebooks. Needs direct contact with the Amino Acid Geochronology
   Laboratory (NAU) and equivalents.

## Reproduce

```bash
python channels/c2_racemization/fetch_c2.py
python channels/c2_racemization/run_c2.py
```
