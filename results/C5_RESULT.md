# C5 — Phosphorus-free single cells

**Verdict: BLOCKED on data discoverability. The discriminator itself survives —
this is the only channel so far whose null is structural rather than chemical.**
Run 2026-08-18.

## Why this channel was worth trying

C2 and C7 both died because the proposed shadow marker turned out to be something
canonical life already makes (peptidoglycan D-amino acids; fungal peptaibol
AIB/isovaline). C5 is different in kind:

**Canonical life cannot build nucleic acids without phosphate.** Sulfolipid
substitution under P limitation — the SAR11 trick — replaces *phospholipids*, not
DNA and RNA. So a low-P cell is ordinary and expected; a genuinely **zero-P cell
with normal C and N** has no canonical route. The null is a structural constraint,
not a chemical convention, which is exactly the property the C7 result argues we
should be selecting for.

## What was attempted

Three independent acquisition routes:

1. **BCO-DMO API** across seven query terms (`SXRF`, `EPZT`, `GeoMICS`, `IRNBRU`,
   `single cell elemental`, `phytoplankton elemental quota`, `Twining`). Returns
   exactly one relevant dataset every time: `nid 1005186`, *Single-cell
   Synechococcus WH8102 XRMA elemental data*.
2. **That dataset's full record** (`osprey.bco-dmo.org/api/dataset/1005186`) —
   JSON-LD with no resolvable data-file URL, and the landing page exposes no
   direct download.
3. **BCO-DMO dataset search UI** — JavaScript-driven, returns no results to a
   fetch.

The one discoverable dataset is a **laboratory culture** (Duhamel Lab,
*Synechococcus* WH8102 under varied P conditions). That makes it a good
**canonical-P reference distribution** and useless as an environmental search set.

Environmental SXRF single-cell data demonstrably exists — Twining, Baines and
colleagues analysed individual cells from GEOTRACES EPZT, GeoMICS and IRNBRU
cruises, and the literature states it is archived at BCO-DMO. It was not
reachable through any public API route tried here.

## Design caveat, recorded whether or not the data arrives

SXRF measurement requires an analyst to **optically identify and select cells**
on a filter before measuring them. That is a selection step upstream of the data.
A particle that did not look like a cell would not be picked; a cell returning no
P signal could plausibly be discarded as a failed measurement rather than
recorded as a zero.

This is structurally identical to C1, where 18% of detected particles were
discarded at the gating stage. **In both cases the discard happens before the
dataset exists**, so no amount of reanalysis can recover it.

That is the fifth aperture observation in this project, and the most general one:

> Every physics-aperture channel examined has a human or algorithmic selection
> step upstream of the archive, and that step removes precisely the anomalous
> objects the channel was chosen to detect.

## Status

Blocked, not killed. Unblocking needs a direct request to BCO-DMO or to the
Twining group for the field SXRF per-cell elemental tables. Unlike C2 and C7, the
test would still mean something if the data arrived.
