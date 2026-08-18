#!/usr/bin/env python3
"""Fetch the SeaFlow archives for C1. Raw data is never committed; this is how
anyone reproduces it from the DOIs."""
import os
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.abspath(os.path.join(HERE, "..", "..", "data", "raw"))

FILES = [
    # per-particle optical data, 10% subsample, CC-BY-4.0 — the analysis input
    ("https://zenodo.org/api/records/4682238/files/SeaFlow_data_10percent.zip/content",
     "SeaFlow_data_10percent.zip"),
    # curated product, used only to demonstrate that 'unknown' is dropped from it
    ("https://zenodo.org/api/records/10896099/files/SeaFlow_dataset_v1.6.xlsx/content",
     "SeaFlow_dataset_v1.6.xlsx"),
]

if __name__ == "__main__":
    os.makedirs(RAW, exist_ok=True)
    for url, name in FILES:
        dest = os.path.join(RAW, name)
        if os.path.exists(dest):
            print("have", name)
            continue
        print("fetching", name)
        urllib.request.urlretrieve(url, dest)
    z = os.path.join(RAW, "SeaFlow_data_10percent.zip")
    if not os.path.isdir(os.path.join(RAW, "SeaFlow_data_10percent")):
        zipfile.ZipFile(z).extractall(RAW)
        print("extracted")
    print("done ->", RAW)
