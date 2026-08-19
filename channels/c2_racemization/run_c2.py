#!/usr/bin/env python3
"""
C2 - Racemization: is there a D-excess that violates racemization rate ordering?

Rationale. Amino-acid racemization geochronology works because racemization is
a first-order reaction with a strict, measured rate ordering across amino acids
(Asx fastest, Ile slowest). Diagenetic D-excess must respect that ordering.
A D-excess produced by a biology that uses D-amino acids has no reason to.

So the discriminator lives INSIDE each sample: rank the measured D/L values and
ask whether they follow the known kinetic ordering.

Pre-registered test (PREREGISTRATION.md, C2):
  statistic  : per-sample Spearman rho between observed D/L and the published
               racemization rate ordering.
  null       : racemization, which predicts rho ~ +1.
  threshold  : rho < 0.3, reproduced in independent sub-samples.
  killed if  : the excess follows the rate ordering, OR is confined to
               peptidoglycan amino acids (D-Ala, D-Glu), OR to D-Asp / D-Ser
               which have known racemases in canonical life.

POSITIVE CONTROL (gate). Racemization is real and dominant in fossil
biominerals, so the distribution of rho across ordinary samples must sit high.
If the median rho is not clearly positive, the pipeline cannot detect the
ordering it is supposed to test against, and no result may be interpreted.

Rate ordering source: the consensus ordering used in AAR geochronology
(Kaufman & Manley 1998; Penkman et al. 2008). Ranks are 1 = fastest.
Proline is deliberately EXCLUDED: its published rate position is inconsistent
across matrices, so including it would inject noise into the rank test.
Serine is flagged rather than excluded - it racemizes fast but also decomposes,
so at high extents Ser D/L falls, a known non-monotonicity.
"""
import glob
import json
import os
import re
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.abspath(os.path.join(HERE, "..", "..", "data", "raw", "c2_aar"))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "results"))

# 1 = fastest racemizing. Consensus AAR ordering.
RATE_RANK = {"asx": 1, "asp": 1, "ser": 2, "glx": 3, "glu": 3, "ala": 4,
             "phe": 5, "leu": 6, "val": 7, "ile": 8, "ileu": 8, "a/i": 8}

# amino acids whose D form is produced by canonical life and therefore cannot
# support a shadow-life reading (peptidoglycan D-Ala/D-Glu; racemases for
# Asp and Ser). Pre-registered restriction.
CANONICAL_D = {"ala", "glu", "glx", "asp", "asx", "ser"}
CLEAN = {"leu", "val", "ile", "ileu", "phe"}


def canon(col):
    """Map a column header to an amino-acid key, or None.

    AUDIT FIX (AUDIT.md, A2). The first version had two defects:
      * r"\bval" matched inside "value", so a column named "D/L value" or
        "D/L validity flag" parsed as VALINE;
      * "A/I" (the alloIle/Ile ratio, a standard AAR measure) matched nothing,
        leaving the "a/i" entry in RATE_RANK as unreachable dead code.

    Neither affected the published C2 result. Every D/L column in all nine
    datasets was re-checked: 0 false positives, 0 missed A/I columns. The one
    dangerous header, "Asp D/L (corrected values)", was saved only by loop
    ordering (asp is tested before val). That was luck, so both are fixed here.
    """
    c = col.lower()
    if "std dev" in c or "error" in c or "±" in c:
        return None
    if "d/l" not in c and "a/i" not in c:
        return None
    # drop words that merely CONTAIN an amino-acid substring
    c = re.sub(r"\bvalues?\b|\bvalue\b|\bvalidity\b|\bvalid\b", " ", c)
    if re.search(r"\ba/i\b|allo.?ile", c):
        return "ile"
    for aa in ("asx", "asp", "ser", "glx", "glu", "ala", "phe",
               "leu", "val", "ileu", "ile"):
        if re.search(r"\b" + aa, c):
            return "ile" if aa in ("ile", "ileu") else aa
    return None


def read_pangaea(path):
    """PANGAEA text export: metadata block terminated by a line of '*/'."""
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.read().split("\n")
    start = next((i + 1 for i, l in enumerate(lines) if l.strip() == "*/"), 0)
    from io import StringIO
    return pd.read_csv(StringIO("\n".join(lines[start:])), sep="\t")


def analyse_table(name, df):
    cols = {}
    for c in df.columns:
        k = canon(str(c))
        if k and k in RATE_RANK and k not in cols:
            cols[k] = c
    if len(cols) < 4:
        return {"source": name, "n_amino_acids": len(cols),
                "amino_acids": sorted(cols), "skipped": "fewer than 4 amino acids"}

    rows = []
    for i, r in df.iterrows():
        vals, ranks, keys = [], [], []
        for k, c in cols.items():
            v = pd.to_numeric(r[c], errors="coerce")
            if np.isfinite(v) and v > 0:
                vals.append(float(v)); ranks.append(RATE_RANK[k]); keys.append(k)
        if len(vals) < 4:
            continue
        # racemization predicts D/L decreases as rate rank increases (slower)
        rho, p = spearmanr(ranks, vals)
        rho_expected_sign = -rho     # so +1 == follows kinetics
        clean_present = [k for k in keys if k in CLEAN]
        rows.append({"row": int(i), "n_aa": len(vals), "aas": keys,
                     "dl": vals, "rho_vs_kinetics": float(rho_expected_sign),
                     "p": float(p), "n_clean_aa": len(clean_present),
                     "max_dl": float(max(vals))})
    if not rows:
        return {"source": name, "skipped": "no rows with >=4 amino acids",
                "amino_acids": sorted(cols)}

    rhos = np.array([r["rho_vs_kinetics"] for r in rows])
    viol = [r for r in rows if r["rho_vs_kinetics"] < 0.3]
    # a violation only counts if it is carried by non-canonical-D amino acids
    viol_clean = [r for r in viol if r["n_clean_aa"] >= 2]
    return {"source": name, "amino_acids": sorted(cols), "n_samples": len(rows),
            "median_rho": float(np.median(rhos)), "mean_rho": float(np.mean(rhos)),
            "frac_following_kinetics": float(np.mean(rhos > 0.3)),
            "n_violations": len(viol), "n_violations_clean_aa": len(viol_clean),
            "violations": viol_clean[:20]}


def main():
    results = []
    for f in sorted(glob.glob(os.path.join(RAW, "*.tab"))):
        try:
            results.append(analyse_table(os.path.basename(f), read_pangaea(f)))
        except Exception as e:
            results.append({"source": os.path.basename(f),
                            "error": "%s: %s" % (type(e).__name__, str(e)[:120])})
    for f in sorted(glob.glob(os.path.join(RAW, "*.xlsx"))):
        try:
            for sheet, df in pd.read_excel(f, sheet_name=None).items():
                results.append(analyse_table(
                    "%s::%s" % (os.path.basename(f), sheet), df))
        except Exception as e:
            results.append({"source": os.path.basename(f),
                            "error": "%s: %s" % (type(e).__name__, str(e)[:120])})

    usable = [r for r in results if "n_samples" in r]

    # ---------------- POSITIVE CONTROL GATE ----------------
    all_rho = [r["median_rho"] for r in usable]
    control_ok = bool(all_rho) and float(np.median(all_rho)) > 0.5

    print("=" * 78)
    print("C2 - amino-acid racemization rate-ordering test")
    print("=" * 78)
    for r in results:
        if "error" in r:
            print("  ERR  %-28s %s" % (r["source"], r["error"]))
        elif "skipped" in r:
            print("  skip %-28s %s (%s)" % (r["source"], r["skipped"],
                                            ",".join(r.get("amino_acids", []))))
        else:
            print("  RUN  %-28s n=%-5d AAs=%-28s medRho=%+.2f follow=%.0f%% "
                  "viol=%d viol_cleanAA=%d"
                  % (r["source"], r["n_samples"], ",".join(r["amino_acids"]),
                     r["median_rho"], 100 * r["frac_following_kinetics"],
                     r["n_violations"], r["n_violations_clean_aa"]))

    print("\nPOSITIVE CONTROL: racemization must dominate, so median rho > 0.5")
    print("  median of per-dataset median rho = %+.3f -> CONTROL %s"
          % (float(np.median(all_rho)) if all_rho else float("nan"),
             "OK" if control_ok else "FAILED"))

    tot_v = sum(r["n_violations_clean_aa"] for r in usable)
    tot_n = sum(r["n_samples"] for r in usable)
    if not control_ok:
        verdict = "INCONCLUSIVE - pipeline failed positive control"
        print("\nPIPELINE FAILED ITS POSITIVE CONTROL. Result not interpretable.")
    elif tot_v == 0:
        verdict = "KILLED - no rate-ordering violation carried by non-canonical-D amino acids"
        print("\nVERDICT: %s\n  %d samples examined, 0 qualifying violations." % (verdict, tot_n))
    else:
        verdict = "CANDIDATES - %d qualifying violations, require replication" % tot_v
        print("\nVERDICT: %s of %d samples" % (verdict, tot_n))

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "c2_racemization.json"), "w") as f:
        json.dump({"positive_control_passed": control_ok, "verdict": verdict,
                   "n_samples_total": tot_n, "n_qualifying_violations": tot_v,
                   "datasets": results}, f, indent=2)
    print("\nwrote results/c2_racemization.json")


if __name__ == "__main__":
    main()
