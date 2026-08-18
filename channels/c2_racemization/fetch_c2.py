#!/usr/bin/env python3
"""Fetch amino-acid racemization (D/L) datasets for C2.

The rate-ordering test needs MULTIPLE amino acids measured per sample, so a
dataset reporting only Asx D/L is useless here and is recorded as such.
"""
import json
import os
import ssl
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.abspath(os.path.join(HERE, "..", "..", "data", "raw", "c2_aar"))
CTX = ssl.create_default_context()
UA = {"User-Agent": "Mozilla/5.0 ShadowBiosphereAudit/0.1"}

# PANGAEA datasets surfaced by the source audit. Tabular text is served at
# doi.pangaea.de/<doi>?format=textfile
PANGAEA_DOIS = [
    "10.1594/PANGAEA.832121", "10.1594/PANGAEA.757460", "10.1594/PANGAEA.900879",
    "10.1594/PANGAEA.901651", "10.1594/PANGAEA.746780", "10.1594/PANGAEA.808545",
    "10.1594/PANGAEA.838976", "10.1594/PANGAEA.901675", "10.1594/PANGAEA.810152",
    "10.1594/PANGAEA.888699", "10.1594/PANGAEA.832120", "10.1594/PANGAEA.54730",
    "10.1594/PANGAEA.838975",
]

ZENODO_FILES = [
    ("https://zenodo.org/api/records/17583785/files/Dataset 1_AAR.xlsx/content",
     "zenodo_17583785_AAR.xlsx"),
]


def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return "have"
    try:
        req = urllib.request.Request(url.replace(" ", "%20"), headers=UA)
        body = urllib.request.urlopen(req, timeout=90, context=CTX).read()
        with open(dest, "wb") as f:
            f.write(body)
        return "ok %d B" % len(body)
    except Exception as e:
        return "ERR %s: %s" % (type(e).__name__, str(e)[:90])


if __name__ == "__main__":
    os.makedirs(RAW, exist_ok=True)
    log = {}
    for doi in PANGAEA_DOIS:
        name = "pangaea_%s.tab" % doi.split(".")[-1]
        url = "https://doi.pangaea.de/%s?format=textfile" % doi
        log[name] = fetch(url, os.path.join(RAW, name))
        print("%-26s %s" % (name, log[name]))
    for url, name in ZENODO_FILES:
        log[name] = fetch(url, os.path.join(RAW, name))
        print("%-26s %s" % (name, log[name]))
    with open(os.path.join(RAW, "_fetch_log.json"), "w") as f:
        json.dump(log, f, indent=2)
    print("\n->", RAW)
