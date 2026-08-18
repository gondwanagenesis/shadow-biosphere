#!/usr/bin/env python3
"""
Probe every candidate archive for the shadow-biosphere search.

Records, for each source: reachability, API shape, whether a targeted query
returns records, and whether bulk download is possible without credentials.

This is the aperture audit. A channel is only runnable if its source is
machine-accessible; anything requiring a data request is logged as BLOCKED
instead of being silently dropped.
"""
import json
import ssl
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ShadowBiosphereAudit/0.1"
CTX = ssl.create_default_context()

# (channel, source name, url, what this source would supply)
SOURCES = [
    # ---------------- cross-cutting generic repositories ----------------
    ("*", "Zenodo API", "https://zenodo.org/api/records?q=%22flow+cytometry%22+ocean&size=3", "generic repo search"),
    ("*", "figshare API", "https://api.figshare.com/v2/articles?search_for=single%20cell%20Raman&page_size=3", "generic repo search"),
    ("*", "Dryad API", "https://datadryad.org/api/v2/search?q=amino%20acid%20racemization&per_page=3", "generic repo search"),
    ("*", "OSF API", "https://api.osf.io/v2/nodes/?page[size]=3", "generic repo search"),
    ("*", "PANGAEA search", "https://www.pangaea.de/advanced/search.php?q=amino+acid+racemization&count=3", "earth/marine data"),
    ("*", "DataCite DOI metadata", "https://api.datacite.org/dois?query=seaflow&page[size]=3", "DOI discovery"),
    ("*", "OpenAlex", "https://api.openalex.org/works?search=shadow%20biosphere&per_page=3", "literature discovery"),
    ("*", "Europe PMC", "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22shadow%20biosphere%22&format=json&pageSize=3", "literature discovery"),

    # ---------------- C1 cytometry ----------------
    ("C1", "Simons CMAP catalog", "https://simonscmap.com/api/data/catalog", "SeaFlow + ocean timeseries host"),
    ("C1", "SeaFlow Zenodo", "https://zenodo.org/api/records?q=seaflow&size=10", "SeaFlow cruise archives"),
    ("C1", "seaflow-uw GitHub", "https://api.github.com/orgs/seaflow-uw/repos?per_page=10", "SeaFlow code + SFL metadata"),
    ("C1", "BCO-DMO datasets", "https://www.bco-dmo.org/api/dataset?name=flow%20cytometry", "US ocean biogeochem archive"),
    ("C1", "HOT-DOGS Hawaii TS", "https://hahana.soest.hawaii.edu/hot/hot-dogs/", "HOT time series"),
    ("C1", "BATS BIOS", "https://bats.bios.asu.edu/bats-data/", "Bermuda time series"),
    ("C1", "Tara Oceans PANGAEA", "https://www.pangaea.de/advanced/search.php?q=Tara+Oceans+flow+cytometry&count=3", "Tara co-registered channels"),

    # ---------------- C2 amino acid racemization ----------------
    ("C2", "NCEI paleo dataTypeId", "https://www.ncei.noaa.gov/access/paleo-search/study/search.json?dataTypeId=16&limit=5", "AAR geochronology archive"),
    ("C2", "NCEI paleo keyword", "https://www.ncei.noaa.gov/access/paleo-search/study/search.json?searchText=amino%20acid%20racemization&limit=5", "AAR geochronology archive"),
    ("C2", "Neotoma DB", "https://api.neotomadb.org/v2.0/data/datasets?limit=5", "paleo database"),
    ("C2", "Dryad AAR", "https://datadryad.org/api/v2/search?q=amino%20acid%20racemization&per_page=5", "supplementary D/L tables"),
    ("C2", "Zenodo AAR", "https://zenodo.org/api/records?q=%22amino+acid+racemization%22&size=10", "supplementary D/L tables"),
    ("C2", "EarthChem", "https://ecl.earthchem.org/api/datasets/search?keyword=amino%20acid", "geochem archive"),

    # ---------------- C3 metabolomics ----------------
    ("C3", "MassIVE PROXI datasets", "https://massive.ucsd.edu/ProteoSAFe/proxi/v0.1/datasets?pageSize=5", "raw MS repository"),
    ("C3", "GNPS2 API", "https://gnps2.org/api/datasets", "MS2 spectral library"),
    ("C3", "GNPS library index", "https://external.gnps2.org/gnpslibrary", "MS2 spectral library"),
    ("C3", "MetaboLights WS", "https://www.ebi.ac.uk/metabolights/ws/studies", "curated metabolomics"),
    ("C3", "Metabolomics Workbench", "https://www.metabolomicsworkbench.org/rest/study/study_id/ST/summary", "curated metabolomics"),
    ("C3", "PubChem formula lookup", "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/formula/C6H12O6/cids/JSON?MaxRecords=3", "known-compound kill filter"),
    ("C3", "EPA CompTox", "https://comptox.epa.gov/dashboard-api/ccdapp1/search/chemical/start-with/caffeine", "anthropogenic kill filter"),
    ("C3", "BioCyc websvc", "https://websvc.biocyc.org/META/search?query=glucose", "known-biosynthesis filter"),

    # ---------------- C4 Raman ----------------
    ("C4", "Zenodo single-cell Raman", "https://zenodo.org/api/records?q=%22single-cell+Raman%22&size=10", "RACS spectral archives"),
    ("C4", "Zenodo D2O Raman", "https://zenodo.org/api/records?q=Raman+D2O+deuterium+single+cell&size=10", "activity-labelled Raman"),
    ("C4", "figshare Raman bacteria", "https://api.figshare.com/v2/articles?search_for=Raman%20spectra%20bacteria&page_size=10", "spectral archives"),
    ("C4", "RRUFF mineral Raman", "https://rruff.info/zipped_data_files/raman/", "negative reference library"),

    # ---------------- C5 single-cell elemental ----------------
    ("C5", "BCO-DMO XRF", "https://www.bco-dmo.org/api/dataset?name=single%20cell%20elemental", "Twining-style XRF quotas"),
    ("C5", "PANGAEA nanoSIMS", "https://www.pangaea.de/advanced/search.php?q=nanoSIMS+single+cell&count=3", "single-cell isotope/element"),
    ("C5", "Zenodo XRF plankton", "https://zenodo.org/api/records?q=synchrotron+XRF+plankton+elemental&size=10", "element quota archives"),
]


def extract_count(j):
    """Best-effort record count across the many API conventions."""
    if isinstance(j, list):
        return len(j)
    for k in ("total", "totalCount", "total_count", "count", "numFound", "hitCount"):
        if k in j:
            v = j[k]
            if isinstance(v, int):
                return v
            if isinstance(v, dict):
                for kk in ("total", "count", "total_count"):
                    if kk in v:
                        return v[kk]
    for k in ("hits", "records", "data", "results", "resultList", "studies"):
        if k in j:
            v = j[k]
            if isinstance(v, list):
                return len(v)
            if isinstance(v, dict):
                if "total" in v:
                    return v["total"]
                for kk in ("hits", "result", "records"):
                    if kk in v and isinstance(v[kk], list):
                        return len(v[kk])
    return "?"


def probe(rec):
    channel, name, url, purpose = rec
    out = {"channel": channel, "source": name, "url": url, "purpose": purpose}
    t0 = time.time()
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": UA, "Accept": "application/json,*/*"}
        )
        r = urllib.request.urlopen(req, timeout=45, context=CTX)
        body = r.read()
        out["status"] = r.status
        out["bytes"] = len(body)
        out["content_type"] = r.headers.get("Content-Type", "")
        try:
            j = json.loads(body)
            out["json"] = True
            out["hits"] = extract_count(j)
            out["sample_keys"] = (
                list(j.keys())[:12] if isinstance(j, dict) else "list[%d]" % len(j)
            )
        except Exception:
            out["json"] = False
            txt = body.decode("utf-8", "replace")
            out["snippet"] = " ".join(txt.split())[:200]
    except Exception as e:
        out["status"] = "ERR"
        out["error"] = "%s: %s" % (type(e).__name__, str(e)[:160])
    out["secs"] = round(time.time() - t0, 1)
    return out


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=10) as ex:
        results = list(ex.map(probe, SOURCES))
    with open("probe_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    for r in results:
        flag = "OK  " if r.get("status") == 200 else "FAIL"
        print(
            "%s [%s] %-28s status=%-5s hits=%-8s json=%-5s %s"
            % (
                flag,
                r["channel"],
                r["source"],
                r.get("status"),
                r.get("hits", "-"),
                r.get("json", "-"),
                r.get("error", ""),
            )
        )
