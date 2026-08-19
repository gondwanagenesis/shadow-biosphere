# Audit of all tests

Adversarial self-audit run 2026-08-19, after all eight channels were resolved.
Five specific failure modes probed by running checks, not by re-reasoning.
Two real problems found, one latent bug, one verdict strengthened.

---

## A1 — C6a feature truncation. **PASS**

`featurize()` truncates every sample's feature vector to the minimum length
across samples (`n = min(len(x) for x in X)`). If the py-GC-MS files had
different m/z ranges, that would silently **misalign features across samples** —
a serious, invisible bug.

Checked all 141 files: every one has exactly **653 columns**, identical m/z range.
Truncation drops zero channels. No misalignment. C6a's features are sound.

## A2 — C2 amino-acid column parser. **LATENT BUG, did not fire**

The parser looks for amino-acid names in any column containing `D/L`. Two defects:

- **False positive:** `"D/L value"` and `"D/L validity flag"` parse as **valine**,
  because `\bval` matches inside "value".
- **False negative:** `"A/I D/L"` — the alloIle/Ile ratio, a standard AAR
  measure — parses as nothing. `RATE_RANK` contains an `"a/i"` entry that
  `canon()` can never return, so it is dead code.

**Did it affect the result? No.** Every `D/L` column in the actual 9 datasets was
checked: **0 false positives, 0 missed A/I columns.** The one dangerous column,
`"Asp D/L (corrected values)"`, was saved by loop ordering — `asp` is tested
before `val`. That is luck, not design.

C2's verdict stands. The parser is fragile and would misparse other archives.
Fixed in the code; the pre-fix behaviour is recorded here.

## A3 — C1 positive-control asymmetry. **REAL PROBLEM**

The pre-registered gate validates the **mean forward scatter** channel:
Prochlorococcus size diel, 6/11 cruises at FAP < 1e-3. It passed.

But C1's headline result is carried by the **abundance-fraction** channel, and
Prochlorococcus abundance passes that same gate in only **2 of 11 cruises**:

| | cruises passing FAP < 1e-3 |
|---|---|
| prochloro `mean_fsc` | **6** |
| prochloro `abundance_fraction` | **2** |

The pre-registered threshold was ≥ 3. **So the channel carrying the headline
result did not meet the project's own validation bar**, and the rule is that an
unvalidated pipeline may not report a null. This was not noticed when C1 was
written up.

Physically it is unsurprising — Prochlorococcus cell *size* has a far larger and
more robust diel cycle than its *abundance*, which advection and mixing smear.
But that is a post-hoc explanation, and the project does not accept those in
place of a control. Resolved by A4.

## A4 — C1 injection recovery. **RESOLVES A3, and yields a detection limit**

Rather than argue, inject a synthetic 24 h signal of known amplitude and phase
into the **real** unknown-fraction series and check the pipeline recovers it.
(`channels/c1_cytometry/audit_injection.py`)

| injected amplitude | recovered (24.0 h, FAP < 1e-3) |
|---|---|
| 0.50 × series sd | **6 / 6 cruises** |
| 0.25 × series sd | **5 / 6 cruises** |
| 0.10 × series sd | 2 / 6 cruises |

Phase error < 2 h in every recovered case. The abundance channel therefore has
genuine sensitivity despite the weak natural Prochlorococcus abundance control.

**This upgrades C1 from an unquantified null to a measured one:**

> C1 found no diel signal in the discarded gate **above ≈ 0.25 × the series
> standard deviation**. It is not sensitive to signals at 0.10 × sd.

That is a stated detection limit, which is what this project claimed to be for.
It is a stronger validation than the original prochloro gate, because it tests
the exact channel and the exact statistic used for the reported result.

## A5 — C6a domain definitions. **VERDICT STRENGTHENED**

The `animal` domain contains `dna`, `rna`, `collagen`, `gelatin`, `hair`,
`cobweb` — purified biomolecules and animal products, not a coherent taxonomic
domain. Ill-defined groups can inflate apparent domain effects.

| domain | n | delta |
|---|---|---|
| animal | 5 | −0.280 |
| microbial | 8 | −0.170 |
| plant | 11 | +0.171 |

| | mean delta | drop |
|---|---|---|
| all biotic domains | −0.0930 | 9.3 pp |
| excluding ill-defined `animal` | **+0.0005** | **−0.0 pp** |

Pre-registered memorization threshold: 15 pp. **The verdict is GENERALIZES either
way, and gets stronger when the incoherent domain is removed** — the drop goes to
essentially zero. C6a's conclusion is robust to this labelling defect.

---

## Summary

| Audit | Target | Outcome |
|---|---|---|
| A1 | C6a feature alignment | Pass, no misalignment |
| A2 | C2 column parser | Latent bug, did not fire, now fixed |
| A3 | C1 control asymmetry | **Real problem** — headline channel under-validated |
| A4 | C1 injection recovery | A3 resolved; **detection limit ≈ 0.25 sd** |
| A5 | C6a domain coherence | Verdict robust, in fact strengthened |

No channel's verdict is reversed by this audit. One (C1) is materially better
supported than it was, and now carries a quantified sensitivity floor instead of
an assumed one. One latent bug is fixed before it could affect future data.

**What this audit did not do:** it cannot check C7 or C8, which were killed on
design from published biochemistry and thermodynamics rather than by running
code. Those arguments need an adversarial reader, not a script. Likewise the
three failure modes in `CONCLUSIONS.md` are my synthesis and have not been
independently checked.
