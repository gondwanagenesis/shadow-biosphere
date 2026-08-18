#!/usr/bin/env python3
"""
C1 - Cytometry: does the discarded 'unknown' particle gate behave like a
population or like a particle load?

Data: SeaFlow per-particle optical archive (Zenodo 4682238, CC-BY-4.0),
12 cruises, 107 million particles, of which 19.3 million carry pop='unknown'.
The curated SeaFlow v1.6 product (Zenodo 10896099) drops every one of them.

Pre-registered test (PREREGISTRATION.md, C1):
  statistic  : Lomb-Scargle power at 24 h in the unknown-particle series,
               before and after regressing out physical forcing.
  null       : residual is noise with no significant 24 h peak.
  threshold  : FAP < 1e-3, reproduced in >= 3 independent cruises.
  killed if  : no significant residual power, OR variance decomposes onto
               physics at R^2 > 0.8, OR the signal matches the reference channel.

--------------------------------------------------------------------------
METHOD NOTE - why version 1 of this script was discarded
--------------------------------------------------------------------------
The first implementation ran the periodogram on the raw hourly series and
returned FAP = 1.0 for every population on every cruise, INCLUDING
Prochlorococcus. That is not a null result, it is a broken analysis:
Prochlorococcus has a large, repeatedly published diel cycle measured with
this very instrument (Ribalet et al. 2015 PNAS, on SeaFlow data).

Cause: SeaFlow is an underway instrument on a moving ship, so the record is
a space series as much as a time series. Variance from crossing water masses
is orders of magnitude larger than the diel term and sits at low frequency,
where it dominates the periodogram normalisation and buries the 24 h peak.

Fixes applied here:
  1. resample onto a regular hourly grid, so window functions are honest;
  2. high-pass by subtracting a 49 h centred rolling median, which removes
     the spatial/water-mass trend while preserving the diel band;
  3. an explicit POSITIVE CONTROL GATE - mean per-cell forward scatter of
     Prochlorococcus, the canonical diel observable (cells grow through the
     day and divide near dusk). If that control does not show 24 h power,
     this script reports ITSELF as failed and refuses to interpret the
     unknown-population result.

AMENDMENT (see AMENDMENTS.md): the pre-registration named the instrument
bead channel as artifact control. The published archive has already removed
beads, so the artifact control used is the phase relationship to classified
populations. Gate leakage from Prochlorococcus would lock unknown to
prochloro phase; an independent population has no reason to share it.
"""
import json
import os
import numpy as np
import pandas as pd
import duckdb
from astropy.timeseries import LombScargle

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "data", "raw", "SeaFlow_data_10percent")
OUT = os.path.join(HERE, "..", "..", "results")
POPS = ["prochloro", "synecho", "picoeuk", "unknown"]
HIGHPASS_WINDOW_H = 49          # odd, ~2 days: kills water-mass trend, keeps diel
MIN_HOURS = 96                  # need >= 4 days to claim a 24 h period at all


def solar_elevation(lat, lon, utc_h, doy):
    dec = 23.45 * np.sin(np.radians(360.0 / 365.0 * (284 + doy)))
    H = 15.0 * ((utc_h + lon / 15.0) - 12.0)
    la, de, Ha = np.radians(lat), np.radians(dec), np.radians(H)
    return np.degrees(np.arcsin(np.sin(la) * np.sin(de)
                                + np.cos(la) * np.cos(de) * np.cos(Ha)))


def highpass(series, window=HIGHPASS_WINDOW_H):
    """Remove the low-frequency (spatial / water-mass) trend."""
    base = series.rolling(window, center=True, min_periods=window // 3).median()
    return series - base


def ls_test(t, y, period=24.0):
    """Lomb-Scargle power and Baluev false-alarm probability at one period."""
    ok = np.isfinite(t) & np.isfinite(y)
    if ok.sum() < MIN_HOURS or np.nanvar(y[ok]) == 0:
        return dict(power=np.nan, fap=np.nan, peak_period_h=np.nan, n=int(ok.sum()))
    ls = LombScargle(t[ok], y[ok])
    freq = np.linspace(1 / 96.0, 1 / 5.0, 6000)
    power = ls.power(freq)
    p = float(ls.power(np.array([1.0 / period]))[0])
    try:
        fap = float(ls.false_alarm_probability(p, method="baluev"))
    except Exception:
        fap = float("nan")
    return dict(power=p, fap=fap, peak_period_h=float(1 / freq[np.argmax(power)]),
                n=int(ok.sum()))


def harmonic_phase(lst, y, period=24.0):
    ok = np.isfinite(lst) & np.isfinite(y)
    if ok.sum() < MIN_HOURS:
        return np.nan, np.nan
    w = 2 * np.pi / period
    X = np.column_stack([np.ones(ok.sum()), np.cos(w * lst[ok]), np.sin(w * lst[ok])])
    beta, *_ = np.linalg.lstsq(X, y[ok], rcond=None)
    return float(np.hypot(beta[1], beta[2])), float((np.arctan2(beta[2], beta[1]) / w) % period)


def load_cruise(con, cruise):
    bio = os.path.join(DATA, cruise + "_bio.parquet").replace("\\", "/")
    phys = os.path.join(DATA, cruise + "_phys.parquet").replace("\\", "/")
    if not (os.path.exists(bio) and os.path.exists(phys)):
        return None
    q = """
    WITH b AS (
      SELECT date_trunc('hour', CAST(date AS TIMESTAMP)) AS h, pop,
             count(*) AS n, avg(fsc_small) AS fsc, avg(chl_small) AS chl, avg(pe) AS pe
      FROM read_parquet('{bio}') WHERE pop IS NOT NULL GROUP BY 1,2
    ), tot AS (SELECT h, sum(n) AS total FROM b GROUP BY 1),
    p AS (
      SELECT date_trunc('hour', CAST(date AS TIMESTAMP)) AS h,
             avg(latitude) AS lat, avg(longitude) AS lon,
             avg(temp) AS temp, avg(salinity) AS sal
      FROM read_parquet('{phys}') GROUP BY 1
    )
    SELECT b.h, b.pop, b.n, b.fsc, b.chl, b.pe, tot.total,
           p.lat, p.lon, p.temp, p.sal
    FROM b JOIN tot USING (h) LEFT JOIN p USING (h) ORDER BY b.h, b.pop
    """.format(bio=bio, phys=phys)
    return con.execute(q).df()


def analyse(cruise, long_df):
    # regular hourly grid so the window function is honest
    long_df["h"] = pd.to_datetime(long_df["h"])
    grid = pd.date_range(long_df["h"].min(), long_df["h"].max(), freq="h")
    phys = (long_df.groupby("h")[["lat", "lon", "temp", "sal", "total"]]
            .first().reindex(grid))
    if len(grid) < MIN_HOURS or phys["lat"].notna().sum() < MIN_HOURS:
        return {"cruise": cruise, "skipped": "too few usable hours",
                "n_hours": int(phys["lat"].notna().sum())}

    t = (grid - grid[0]).total_seconds().values / 3600.0
    utc_h = grid.hour.values + grid.minute.values / 60.0
    lon = phys["lon"].values
    lst = (utc_h + lon / 15.0) % 24.0
    sun = solar_elevation(phys["lat"].values, lon, utc_h, grid.dayofyear.values)

    res = {"cruise": cruise, "n_hours": int(len(grid)),
           "n_hours_with_phys": int(phys["lat"].notna().sum()),
           "total_particles": int(long_df["n"].sum()), "pops": {}}

    for pop in POPS:
        sub = long_df[long_df["pop"] == pop].set_index("h").reindex(grid)
        n = sub["n"]
        if n.sum(skipna=True) < 1000:
            continue
        frac = (n / phys["total"]).astype(float)
        fsc = sub["fsc"].astype(float)

        entry = {"n_particles": int(n.sum(skipna=True)),
                 "mean_fraction": float(np.nanmean(frac))}

        for label, series in (("abundance_fraction", frac), ("mean_fsc", fsc)):
            hp = highpass(series)
            r = ls_test(t, hp.values)
            amp, ph = harmonic_phase(lst, hp.values)
            entry[label] = {**r, "diel_amplitude": amp, "diel_phase_LST_h": ph}

        # deconfound the high-passed abundance against physics, then re-test
        hp = highpass(frac).values
        X = np.column_stack([np.ones_like(t), sun, phys["temp"].values,
                             phys["sal"].values])
        ok = np.all(np.isfinite(X), axis=1) & np.isfinite(hp)
        if ok.sum() > MIN_HOURS:
            beta, *_ = np.linalg.lstsq(X[ok], hp[ok], rcond=None)
            resid = np.full_like(hp, np.nan)
            resid[ok] = hp[ok] - X[ok] @ beta
            r2 = 1 - np.nanvar(resid[ok]) / np.nanvar(hp[ok])
            entry["after_physics_deconfound"] = {**ls_test(t, resid),
                                                 "physics_R2": float(r2)}
        res["pops"][pop] = entry
    return res


def main():
    con = duckdb.connect()
    cruises = sorted({f.split("_bio.parquet")[0]
                      for f in os.listdir(DATA) if f.endswith("_bio.parquet")})
    out = []
    for c in cruises:
        df = load_cruise(con, c)
        if df is None or df.empty:
            continue
        out.append(analyse(c, df))

    # ---------------- POSITIVE CONTROL GATE ----------------
    # Prochlorococcus mean forward scatter must show 24 h power. If it does not,
    # the pipeline has no sensitivity and no other result may be interpreted.
    ctrl = [(r["cruise"], r["pops"]["prochloro"]["mean_fsc"]["fap"])
            for r in out if "pops" in r and "prochloro" in r["pops"]
            and np.isfinite(r["pops"]["prochloro"]["mean_fsc"]["fap"])]
    passed = [c for c, f in ctrl if f < 1e-3]
    control_ok = len(passed) >= 3

    print("=" * 78)
    print("POSITIVE CONTROL - Prochlorococcus mean forward scatter, 24 h power")
    for c, f in ctrl:
        print("   %-14s FAP=%.3e %s" % (c, f, "PASS" if f < 1e-3 else "fail"))
    print("   -> %d/%d cruises pass. CONTROL %s"
          % (len(passed), len(ctrl), "OK" if control_ok else "FAILED"))
    print("=" * 78)

    if not control_ok:
        print("\nPIPELINE FAILED ITS OWN POSITIVE CONTROL.")
        print("The unknown-population result below is NOT interpretable and is")
        print("recorded as inconclusive, not as a null result.\n")

    print("%-14s %-10s %10s %10s %9s %9s" %
          ("cruise", "pop", "FAP_abund", "FAP_fsc", "phase_LST", "peakP_h"))
    for r in out:
        if "skipped" in r:
            continue
        for pop in POPS:
            p = r["pops"].get(pop)
            if not p:
                continue
            print("%-14s %-10s %10.2e %10.2e %9.1f %9.1f" %
                  (r["cruise"], pop, p["abundance_fraction"]["fap"],
                   p["mean_fsc"]["fap"], p["abundance_fraction"]["diel_phase_LST_h"],
                   p["abundance_fraction"]["peak_period_h"]))

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "c1_cytometry.json"), "w") as f:
        json.dump({"positive_control_passed": bool(control_ok),
                   "positive_control_detail": ctrl,
                   "verdict": ("interpretable" if control_ok
                               else "INCONCLUSIVE - pipeline failed positive control"),
                   "cruises": out}, f, indent=2)
    print("\nwrote results/c1_cytometry.json")


if __name__ == "__main__":
    main()
