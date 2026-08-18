# Data source audit

Machine-probed 2026-08-18. Raw output: `probe_results.json`. Re-run with
`python probe_sources.py`.

**27 of 36 endpoints reachable.** The point of this audit is that a channel is
only runnable if its source is machine-accessible. Anything needing a data
request is marked BLOCKED rather than quietly dropped, so the coverage gaps in
`RESULTS.md` are auditable.

## Cross-cutting repositories

| Source | Status | Notes |
|---|---|---|
| Zenodo API | OK | Primary. Open, DOI-addressable, bulk file download. Licences exposed in metadata. |
| figshare API | OK | Open search, per-article file listing. |
| Dryad API | OK | Journal supplementary data. Small result counts for our queries. |
| OSF API | OK | Reachable; low relevance so far. |
| PANGAEA | OK | Earth/marine. 23 hits for amino-acid racemization, 7 for nanoSIMS single-cell. |
| DataCite | OK | DOI discovery across repositories. |
| OpenAlex | OK | Literature discovery, used to find datasets behind papers. |
| Europe PMC | OK | 19 hits for "shadow biosphere". Used for prior-art and for locating supplementary tables. |

## C1 — cytometry

| Source | Status | Notes |
|---|---|---|
| SeaFlow (Zenodo) | **OK — USED** | 6 records. Per-particle archive 4682238 (556 MB, CC-BY-4.0) is the analysis input. Curated product 10896099 (49 MB, CC-BY-4.0) used to show `unknown` is dropped. |
| seaflow-uw GitHub | OK | 22 repos. `popcycle` documents the gating that produces the `unknown` class. |
| BCO-DMO | OK | API responds, but `name=` does fuzzy matching and returns largely irrelevant hits. Needs the GeoJSON/ERDDAP path instead. |
| HOT-DOGS | OK (HTML) | Reachable but form-driven, no JSON API. Scriptable extraction needed. |
| **BATS / BIOS** | **BLOCKED** | HTTP 522 (origin down) throughout this run. **This is the archive C1 actually needs** — BATS runs DNA-stained benchtop cytometry, where the intended scatter-positive / stain-negative test is possible. SeaFlow is unstained. |
| Tara Oceans (PANGAEA) | OK | 5 hits. Co-registered channels make Tara the best candidate for the conjunction test. |

## C2 — amino-acid racemization

| Source | Status | Notes |
|---|---|---|
| NOAA NCEI paleo | OK | JSON search responds. Needs the correct `dataTypeId` for AAR; keyword search works. |
| Zenodo "amino acid racemization" | OK | 26 records. Best open route to D/L tables. |
| Dryad | OK | 4 records. |
| Neotoma | BLOCKED | Read timeout at 45 s. Retry with longer timeout; likely transient. |
| EarthChem | BLOCKED | 404 on the documented API path. Endpoint has moved. |

Structural caveat: most historical D/L data lives in **supplementary tables of
papers**, not in APIs. The richest target — samples that AAR labs *rejected* as
diagenetically altered — is largely in lab notebooks and will need direct
contact with the Amino Acid Geochronology Laboratory (NAU) and equivalents.

## C3 — metabolomics

| Source | Status | Notes |
|---|---|---|
| MetaboLights (EBI) | OK | Public study listing, per-study raw files. |
| GNPS library index | OK (HTML) | Library downloadable, but not via the JSON path tried. |
| EPA CompTox | OK | 15 hits on test query. Works as the anthropogenic kill-filter. |
| PubChem | OK (202) | Async job pattern, not an error. Works as the known-compound kill-filter. |
| MassIVE PROXI | BLOCKED | HTTP 400 on documented params. Needs the ProteoSAFe query API instead. |
| GNPS2 API | BLOCKED | 404. Endpoint moved from the documented path. |
| Metabolomics Workbench | PARTIAL | Single-study REST works; the all-studies query times out. Page it. |
| BioCyc | BLOCKED | 404, requires a subscription for web services. Use KEGG/MetaCyc alternatives. |

## C4 — Raman

| Source | Status | Notes |
|---|---|---|
| Zenodo single-cell Raman | OK | 9 records on the exact-phrase query. Small. |
| figshare Raman bacteria | OK | 10 records. |
| RRUFF | OK | Mineral Raman reference library, bulk-downloadable. Needed as the negative reference. |

Structural caveat: no public archive of **D₂O-labelled** single-cell Raman was
found at scale. This is the highest-specificity channel and the most
data-starved. Realistically needs direct request to the Huang (Xiamen) and
Wagner (Vienna) groups.

## C5 — single-cell elemental

| Source | Status | Notes |
|---|---|---|
| PANGAEA nanoSIMS | OK | 7 hits. |
| Zenodo XRF plankton | OK | Broad query; needs tightening. |
| BCO-DMO | OK | Surfaced "Single-cell Synechococcus WH8102 XRMA elemental data" — a culture experiment, so useful as a **canonical-P reference distribution**, not as an environmental search set. |

## Honest summary of coverage

Only **C1** had an open, bulk-downloadable, machine-readable archive sufficient
to run the pre-registered test end to end. C2 and C5 have partial open data and
a clear acquisition path. C3 needs API repair plus large downloads. C4 is
effectively blocked on data that is not publicly archived.

This is itself a finding: the lineage-free measurement channels are exactly the
ones with the weakest public data infrastructure.
