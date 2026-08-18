#!/usr/bin/env python3
"""
C6c - Residual mining: can a THIRD class be detected at all?

Every agnostic-classifier paper reports accuracy and treats the ~10% error as
noise. But a third class - something neither canonical-biotic nor abiotic - would
not appear as accuracy loss. It would appear as samples that are classified
CONFIDENTLY yet sit far from everything the model was trained on.

  confident + familiar  -> ordinary member of a known class
  unconfident + familiar -> genuine boundary case
  confident + NOVEL      -> the model is extrapolating. THIS is the third-class
                            signature, and it is exactly what shadow life would
                            look like to a classifier trained only on our lineage.

POSITIVE CONTROL (the point of this script). The archive contains a real third
class: 18 geologically processed fossil organic samples, biotic in origin but
abiotic-like in processing, deliberately excluded from the binary. If this method
cannot recover fossils as a distinct, novel group, it has no power to recover a
shadow third class and nothing else may be interpreted.

Pre-registered (PREREGISTRATION_C6_C8.md C6c). Killed if persistent
misclassifications do not cluster, or cluster by a known nuisance variable.
"""
import json
import os
import numpy as np
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.neighbors import NearestNeighbors
from sklearn.covariance import EmpiricalCovariance

from run_c6a import build, LABELS, FOSSIL

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "results"))
N_PC = 5    # p<<n REQUIRED: Mahalanobis degenerates as p->n (see gate 2)
N_REPEATS = 20


def rf(seed=0):
    return RandomForestClassifier(n_estimators=400, random_state=seed,
                                  n_jobs=-1, class_weight="balanced")


def main():
    X, names = build()
    # 5871 features on 52 training samples makes distances meaningless.
    # Reduce on ALL samples first, so the space is defined by the archive.
    Z = PCA(n_components=N_PC, random_state=0).fit_transform(
        (X - X.mean(0)) / (X.std(0) + 1e-12))

    lab = [i for i, k in enumerate(names) if k in LABELS]
    fos = [i for i, k in enumerate(names) if k in FOSSIL]
    amb = [i for i in range(len(names)) if i not in lab and i not in fos]
    y = np.array([1 if LABELS[names[i]][1] == "biotic" else 0 for i in lab])
    print("labelled=%d  fossil(third-class control)=%d  ambiguous=%d"
          % (len(lab), len(fos), len(amb)))

    # ---- persistent misclassification over repeated CV ----
    miss = np.zeros(len(lab))
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=N_REPEATS, random_state=0)
    n_iter = 0
    for tr, te in cv.split(Z[lab], y):
        p = rf(n_iter).fit(Z[lab][tr], y[tr]).predict(Z[lab][te])
        miss[te] += (p != y[te])
        n_iter += 1
    miss /= N_REPEATS
    persistent = [(names[lab[i]], float(miss[i])) for i in np.argsort(-miss)[:8]]
    print("\npersistently misclassified (frac of %d repeats):" % N_REPEATS)
    for n, f in persistent:
        if f > 0:
            print("   %-12s %.2f" % (n, f))

    # ---- novelty: distance to nearest LABELLED training sample ----
    cov = EmpiricalCovariance().fit(Z[lab])
    novelty = lambda idx: cov.mahalanobis(Z[idx])
    d_lab, d_fos, d_amb = novelty(lab), novelty(fos), novelty(amb)

    # ---- confidence from a model trained on the labelled binary ----
    m = rf().fit(Z[lab], y)
    conf = lambda idx: m.predict_proba(Z[idx]).max(axis=1)
    c_fos, c_amb = conf(fos), conf(amb)

    thresh_nov = float(np.percentile(d_lab, 90))
    thresh_conf = 0.70

    # ---- POSITIVE CONTROL: are fossils recoverable as a distinct class? ----
    yy = np.r_[np.zeros(len(lab)), np.ones(len(fos))]
    auc = float(roc_auc_score(yy, np.r_[d_lab, d_fos]))
    fos_flagged = float(((d_fos > thresh_nov) & (c_fos > thresh_conf)).mean())
    # ---- GATE 2: degeneracy. A Mahalanobis metric with p approaching n
    # separates ANY held-out point, not just genuinely novel ones. Verify the
    # metric does not separate random held-out LABELLED samples.
    rng2 = np.random.default_rng(0)
    deg = []
    for _ in range(30):
        idx = rng2.permutation(len(lab))
        ho, keep = idx[:len(fos)], idx[len(fos):]
        c2 = EmpiricalCovariance().fit(Z[np.array(lab)[keep]])
        deg.append(roc_auc_score(
            np.r_[np.zeros(len(keep)), np.ones(len(ho))],
            np.r_[c2.mahalanobis(Z[np.array(lab)[keep]]),
                  c2.mahalanobis(Z[np.array(lab)[ho]])]))
    deg_auc = float(np.mean(deg))
    gap = auc - deg_auc
    control_ok = auc > 0.75 and fos_flagged > 0.30 and gap > 0.15

    print("\nPOSITIVE CONTROL - recover fossil organics as a novel third class")
    print("   novelty AUC (fossil vs labelled)      : %.3f" % auc)
    print("   median novelty  labelled=%.2f fossil=%.2f" %
          (np.median(d_lab), np.median(d_fos)))
    print("   fossils flagged confident+novel        : %.0f%%" % (100 * fos_flagged))
    print("   degeneracy control (random labelled holdout): %.3f" % deg_auc)
    print("   real novelty gap (fossil - degenerate)      : %.3f" % gap)
    print("   -> CONTROL %s" % ("OK" if control_ok else "FAILED"))

    result = {"positive_control_passed": bool(control_ok),
              "novelty_auc_fossil_vs_labelled": auc,
              "fossil_flag_rate": fos_flagged,
              "persistent_misclassified": persistent,
              "novelty_threshold_p90": thresh_nov,
              "degeneracy_auc_random_labelled_holdout": deg_auc,
              "real_novelty_gap": gap, "n_pcs": N_PC}

    if not control_ok:
        result["verdict"] = ("INCONCLUSIVE - cannot recover a KNOWN third class, "
                             "so no power to detect an unknown one")
        print("\nCannot recover a known third class. No power. Nothing interpreted.")
    else:
        flag = [(names[amb[i]], float(d_amb[i]), float(c_amb[i]))
                for i in range(len(amb))
                if d_amb[i] > thresh_nov and c_amb[i] > thresh_conf]
        flag.sort(key=lambda t: -t[1])
        print("\nAMBIGUOUS samples flagged confident+novel: %d of %d"
              % (len(flag), len(amb)))
        for n, d, c in flag[:15]:
            print("   %-12s novelty=%.2f conf=%.2f" % (n, d, c))
        result["flagged_ambiguous"] = flag
        result["n_flagged"] = len(flag)
        result["verdict"] = (
            "METHOD HAS POWER - %d ambiguous samples are confident+novel. These are "
            "NOT shadow candidates: the ambiguous set is dominated by unlabelled "
            "standards, soils and lab materials, and every one needs identification "
            "before it means anything." % len(flag))
        print("\nNOTE: flagged != candidate. The ambiguous set is unlabelled "
              "standards, soils and lab materials. Identification required.")

    print("\nVERDICT: %s" % result["verdict"])
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "c6c_residuals.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("wrote results/c6c_residuals.json")


if __name__ == "__main__":
    main()
