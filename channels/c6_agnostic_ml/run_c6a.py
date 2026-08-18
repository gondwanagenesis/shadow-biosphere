#!/usr/bin/env python3
"""
C6a - Does "agnostic" actually generalize, or has the classifier memorized
canonical biochemistry?

This is the load-bearing test of the whole C6 channel, and it is a methodological
result independent of shadow life.

THE PROBLEM. Every published agnostic biotic/abiotic classifier trains its biotic
class entirely on canonical Earth life. The learned boundary is therefore
"canonical-life-like vs abiotic", not "life vs non-life". Whether those coincide
has never been tested. The two possibilities predict OPPOSITE shadow searches:

  learned real substrate-independent selectivity
      -> shadow life classifies BIOTIC, filed as unremarkable
  memorized canonical biochemistry
      -> shadow life classifies ABIOTIC, actively discarded as geology

TEST (pre-registered, PREREGISTRATION_C6_C8.md C6a): leave-one-domain-out.

METHOD CORRECTION (logged in AMENDMENTS.md). The first version of this test
compared domain-holdout accuracy directly against random-fold accuracy and
reported a 40.6 pp drop. That number was an artifact. Holding out an entire
domain makes the test set single-class AND skews the training class balance -
holding out the 26 synthetic abiotic samples leaves 24 biotic against 2 abiotic,
so the model predicts biotic for everything and scores 0.000 on an all-abiotic
test set. That measures imbalance, not domain generalisation.

The corrected test compares each domain holdout against SIZE- AND CLASS-MATCHED
RANDOM HOLDOUTS: random subsets of the same size drawn from the same class, which
carry the identical imbalance but no domain structure. Only the gap between the
two is a domain effect, and only that gap is interpreted. Classifier also uses
balanced class weights.

Data: Cleaves et al. 2023, OSF EMBH8. Files are scan x m/z intensity matrices
(~6400 scans x 651 m/z channels), the same relational representation the paper
uses - no compound identification anywhere in this pipeline.

LABEL CAVEAT, stated plainly: the OSF deposit ships no label file; labels live in
the paper's SI. The map below is reconstructed from sample filenames. Only
confidently-assignable samples are used; everything ambiguous is EXCLUDED rather
than guessed, and the excluded list is reported. Geologically processed fossil
organic matter is held out of the binary because its class is genuinely contested
(biotic origin, abiotic-like processing).
"""
import json
import os
import re
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "..", "data", "raw", "c6_pygcms"))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "results"))
CACHE = os.path.join(DATA, "_features.npz")
RT_BINS = 8
N_MATCHED = 50

LABELS = {
    "ecoli1": ("microbial", "biotic"), "bsubtil": ("microbial", "biotic"),
    "bcereus": ("microbial", "biotic"), "staepi": ("microbial", "biotic"),
    "scerev": ("microbial", "biotic"), "cyanob": ("microbial", "biotic"),
    "cyanob2": ("microbial", "biotic"), "entaer": ("microbial", "biotic"),
    "barley": ("plant", "biotic"), "basmati": ("plant", "biotic"),
    "bulgur": ("plant", "biotic"), "brnrice": ("plant", "biotic"),
    "oat": ("plant", "biotic"), "okra": ("plant", "biotic"),
    "pumpkin": ("plant", "biotic"), "chiles": ("plant", "biotic"),
    "citron": ("plant", "biotic"), "rdlent": ("plant", "biotic"),
    "grass": ("plant", "biotic"), "oakleaf": ("plant", "biotic"),
    "moss": ("plant", "biotic"), "beet": ("plant", "biotic"),
    "cabbage": ("plant", "biotic"),
    "hair": ("animal", "biotic"), "collagen": ("animal", "biotic"),
    "gelatin": ("animal", "biotic"), "cobweb": ("animal", "biotic"),
    "dna": ("animal", "biotic"), "rna": ("animal", "biotic"),
    "alanine": ("synthetic", "abiotic"), "ala3": ("synthetic", "abiotic"),
    "glycine": ("synthetic", "abiotic"), "lasp": ("synthetic", "abiotic"),
    "lcys": ("synthetic", "abiotic"), "lgln": ("synthetic", "abiotic"),
    "lglu": ("synthetic", "abiotic"), "lhis": ("synthetic", "abiotic"),
    "lleu": ("synthetic", "abiotic"), "llys": ("synthetic", "abiotic"),
    "lmet": ("synthetic", "abiotic"), "lphe": ("synthetic", "abiotic"),
    "lpro": ("synthetic", "abiotic"), "lser": ("synthetic", "abiotic"),
    "ltyr": ("synthetic", "abiotic"), "dglucose": ("synthetic", "abiotic"),
    "malic": ("synthetic", "abiotic"), "glyoxaci": ("synthetic", "abiotic"),
    "hmt": ("synthetic", "abiotic"), "hcn53172": ("synthetic", "abiotic"),
    "nylon": ("synthetic", "abiotic"), "kraton": ("synthetic", "abiotic"),
    "kraton2": ("synthetic", "abiotic"), "sodpyr": ("synthetic", "abiotic"),
    "akg": ("synthetic", "abiotic"), "carnos": ("synthetic", "abiotic"),
    "allende": ("meteorite", "abiotic"), "allende2": ("meteorite", "abiotic"),
}
FOSSIL = {"albertit", "asphltmm", "aspmr", "shungite", "torbanit", "pitt8coa",
          "peat", "grnrivs", "devons", "elaterit", "jetwhtby", "humica",
          "cannak", "cannelco", "westflds", "bonnetf", "cedarto", "ferron"}


def sample_key(fname):
    k = re.sub(r"3d(\.txt)?$", "", fname, flags=re.I)
    return re.sub(r"\.txt$", "", k, flags=re.I).replace(".3d", "").lower().strip()


def featurize(path):
    df = pd.read_csv(path, skiprows=1, header=None, low_memory=False)
    a = df.iloc[:, 1:].apply(pd.to_numeric, errors="coerce").fillna(0).values
    if a.size == 0 or a.sum() <= 0:
        return None
    a = a.astype(np.float64)
    feats = [a.sum(axis=0) / a.sum()]
    edges = np.linspace(0, a.shape[0], RT_BINS + 1).astype(int)
    for i in range(RT_BINS):
        blk = a[edges[i]:edges[i + 1]]
        s = blk.sum()
        feats.append(blk.sum(axis=0) / s if s > 0 else np.zeros(a.shape[1]))
    tic = a.sum(axis=1)
    tic = tic / (tic.sum() or 1)
    feats.append(np.array([tic.std(), (tic > tic.mean()).mean(),
                           -(tic[tic > 0] * np.log(tic[tic > 0])).sum()]))
    return np.concatenate(feats)


def build():
    if os.path.exists(CACHE):
        z = np.load(CACHE, allow_pickle=True)
        return z["X"], list(z["names"])
    X, names = [], []
    for root, _, files in os.walk(DATA):
        for f in sorted(files):
            if not (f.endswith(".txt") or f.endswith(".3d")) or f.startswith("_"):
                continue
            try:
                v = featurize(os.path.join(root, f))
            except Exception:
                v = None
            if v is not None:
                X.append(v); names.append(sample_key(f))
    n = min(len(x) for x in X)
    X = np.array([x[:n] for x in X])
    np.savez_compressed(CACHE, X=X, names=np.array(names))
    return X, names


def rf(seed=0):
    return RandomForestClassifier(n_estimators=500, random_state=seed,
                                  n_jobs=-1, class_weight="balanced")


def main():
    X, names = build()
    print("featurized %d samples, %d features each" % X.shape)

    keep = [i for i, k in enumerate(names) if k in LABELS]
    excluded = sorted({k for k in names if k not in LABELS and k not in FOSSIL})
    Xl = X[keep]
    dom = np.array([LABELS[names[i]][0] for i in keep])
    y = np.array([1 if LABELS[names[i]][1] == "biotic" else 0 for i in keep])
    print("labelled %d (biotic=%d abiotic=%d) | fossil held out %d | excluded %d"
          % (len(y), y.sum(), (1 - y).sum(),
             sum(1 for k in names if k in FOSSIL), len(excluded)))

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    base = float(cross_val_score(rf(), Xl, y, cv=cv).mean())
    control_ok = base > 0.80
    print("\nBASELINE random 5-fold accuracy : %.3f" % base)
    print("POSITIVE CONTROL (>0.80)        : %s" % ("OK" if control_ok else "FAILED"))

    rng = np.random.default_rng(0)
    print("\nDOMAIN HOLDOUT vs SIZE/CLASS-MATCHED RANDOM HOLDOUT")
    print("(matched control carries the same class imbalance but no domain structure;")
    print(" only the delta between them is a domain effect)\n")
    print("   %-11s %4s %-8s %9s %9s %9s %8s" %
          ("domain", "n", "class", "domainR", "randR", "delta", "pctile"))
    lodo = {}
    for d in sorted(set(dom)):
        te = dom == d
        cls = int(y[te][0])
        if len(set(y[~te])) < 2 or te.sum() < 3:
            continue
        dom_r = float((rf().fit(Xl[~te], y[~te]).predict(Xl[te]) == y[te]).mean())
        pool = np.where(y == cls)[0]
        if len(pool) <= te.sum():
            continue
        rand = []
        for _ in range(N_MATCHED):
            sel = rng.choice(pool, size=int(te.sum()), replace=False)
            mask = np.zeros(len(y), bool); mask[sel] = True
            if len(set(y[~mask])) < 2:
                continue
            rand.append(float((rf().fit(Xl[~mask], y[~mask]).predict(Xl[mask])
                               == y[mask]).mean()))
        if not rand:
            continue
        rand = np.array(rand)
        lodo[d] = {"class": "biotic" if cls else "abiotic", "n": int(te.sum()),
                   "domain_recall": dom_r, "matched_mean": float(rand.mean()),
                   "matched_sd": float(rand.std()),
                   "delta": dom_r - float(rand.mean()),
                   "percentile": float((rand <= dom_r).mean())}
        print("   %-11s %4d %-8s %9.3f %9.3f %+9.3f %8.2f" %
              (d, te.sum(), lodo[d]["class"], dom_r, rand.mean(),
               lodo[d]["delta"], lodo[d]["percentile"]))

    bio = {d: v for d, v in lodo.items() if v["class"] == "biotic"}
    deltas = [v["delta"] for v in bio.values()]
    drop = -float(np.mean(deltas)) if deltas else float("nan")
    print("\nmean matched-control delta, held-out BIOTIC domains : %+.3f"
          % (float(np.mean(deltas)) if deltas else float("nan")))
    print("drop attributable to DOMAIN rather than imbalance   : %.1f pp"
          % (100 * drop))
    print("n labelled = %d (biotic=%d) - small-n caveat applies." % (len(y), int(y.sum())))

    if not control_ok:
        verdict = "INCONCLUSIVE - failed positive control"
    elif not deltas:
        verdict = "INCONCLUSIVE - matched control could not be constructed"
    elif drop > 0.15:
        verdict = ("MEMORIZATION - agnosticism overstated; shadow life would "
                   "likely classify ABIOTIC and be discarded")
    else:
        verdict = ("GENERALIZES across canonical diversity - no domain effect "
                   "beyond class imbalance")
    print("\nVERDICT: %s" % verdict)

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "c6a_generalization.json"), "w") as f:
        json.dump({"positive_control_passed": bool(control_ok),
                   "baseline_random_fold_accuracy": base,
                   "domain_vs_matched_control": lodo,
                   "mean_delta_biotic": float(np.mean(deltas)) if deltas else None,
                   "domain_drop_pp": float(100 * drop) if deltas else None,
                   "verdict": verdict, "n_labelled": int(len(y)),
                   "n_biotic": int(y.sum()), "excluded_ambiguous": excluded},
                  f, indent=2)
    print("wrote results/c6a_generalization.json")


if __name__ == "__main__":
    main()
