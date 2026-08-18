# Literature gap analysis

Sweep run 2026-08-18 against the shadow-biosphere and agnostic-biosignature
literature. Purpose: find detection strategies the five original channels missed.

**Verdict: the design was directionally right but missed a large, mature, and
partly ready-made body of work. Three new channels are added below, one of which
has publicly deposited training data that was verified fetchable during this
sweep.**

---

## What the literature confirms

- The **aperture/filter framing** in `METHOD.md` is Cleland & Copley's core
  methodological argument, independently arrived at. Davies et al. (2009) state
  the same failure mode: microscopy with staining, culturing, and PCR are all
  "very specific to the molecular biology and biochemistry of our form of life."
- The **conjunction operator** maps onto NASA's Laboratory for Agnostic
  Biosignatures (LAB) multi-pillar design, which likewise refuses to rest on one
  channel.
- **C3's selectivity signature** was the right instinct. The literature has since
  formalized it at least four separate ways, all more mature than my version.

## Gap 1 — validated agnostic classifiers already exist, with public data

This is the largest miss. Several groups have built and *validated* biochemistry-
independent biotic/abiotic classifiers:

| Method | Basis | Reported accuracy |
|---|---|---|
| Cleaves et al. 2023, *PNAS* 120:e2307149120 | random forest on py-GC-MS; uses relational retention time / abundance / m-z, **no compound identification required** | ~90% |
| LUMOS | abundance-weighted HOMO-LUMO gap distribution of amino acids | >95% |
| Monomer abundance distribution (Dorn, Adami et al., arXiv:1101.1013) | shape of the monomer abundance distribution | — |
| Assembly theory (Marshall, Cronin, Walker) | MS² fragmentation depth as construction-step proxy | — |

**Training data is public.** Cleaves et al. deposited 150 datasets (16 new + 134
previously published) at OSF DOI `10.17605/OSF.IO/EMBH8`. Verified during this
sweep: node is public, `Cleavesetal.pyrGCMSData.zip` is 221 MB and fetchable via
the OSF API. That supplies a **ready-made positive control**, which is the thing
every channel here needs and the thing hardest to obtain.

### The shadow-specific inversion nobody has run

Every one of these classifiers separates **biotic from abiotic**. Not one
separates **our biotic from another biotic**. A shadow biosphere would classify
as "biotic" with high confidence and be filed as unremarkable — the classifier is
*designed* to be agnostic, so it cannot tell whose life it is looking at.

That makes the shadow search a conjunction over an existing validated tool:

> samples a validated agnostic classifier calls **BIOTIC** with high confidence,
> that carry **no canonical biomarkers** (no hopanes, steranes, recognizable
> lipid suites), and yield **no amplifiable sequence**.

Each of those three is a routine measurement. Their intersection is not, and as
far as this sweep found, nobody has queried it. This becomes **C6** and is now the
highest-ranked open channel.

## Gap 2 — the polyelectrolyte theory of the gene

Benner & Hutter (2002); Benner (2017), *Astrobiology* 17:840. Any linear genetic
biopolymer dissolved in water must be a **polyelectrolyte** — a repeating
backbone charge — because only such polymers can change sequence without changing
bulk physical behaviour, which Darwinian evolution requires.

Two consequences I missed:

1. **It narrows the search space.** PNA is uncharged, so PNA-like life cannot run
   Darwinian evolution in water. My earlier speculation about uncharged backbones
   is excluded on theoretical grounds, which is useful: it means an alien genetic
   polymer *will* respond to an electric field.
2. **It hands over a concentration method.** Polyelectrolytes concentrate from
   ultra-dilute aqueous solution simply by washing across a polycharged support,
   and they migrate in electric fields. This is a lineage-agnostic enrichment step
   that requires no enzymology at all.

This strengthens rather than replaces the nuclease-resistance idea: the two
compose into "nuclease-resistant polyanion," which is a much tighter target.

## Gap 3 — two of LAB's four pillars are uncovered

LAB organizes agnostic detection around chemical **complexity**, **disequilibrium**,
**compartmentalization**, and **energy transfer**.

| Pillar | Covered? |
|---|---|
| Complexity | ✅ C3, and now C6 |
| Compartmentalization | ◐ partially, C1 scatter and C5 elemental |
| **Disequilibrium** | ❌ not covered |
| **Energy transfer** | ❌ not covered |

The energy-transfer approach looks for redox chemistry inconsistent with abiotic
electrochemistry — biotic and abiotic iron oxidation have distinct electrochemical
signatures. Archived analogues exist as sediment microelectrode and voltammetry
profiles. Becomes **C8**.

## Gap 4 — the amino-acid alphabet, which I underweighted

Davies et al. name this explicitly: "identify potentially biologically useful
molecules that are not incorporated in standard life or produced in its decay
products." Murchison carries several dozen amino acids; canonical life uses about
20. Meteoritic distributions are smooth in carbon number and rich in non-protein
species such as α-aminoisobutyric acid and isovaline; biological distributions are
sharply selected.

A shadow biosphere would be **selected but on a different alphabet** — neither
smooth-abiotic nor canonical-biotic.

This is nearly free: it runs on the same archived GC-MS amino-acid analyses C2
already used. Becomes **C7**.

## Gap 5 — a scoring framework exists

The Ladder of Life Detection (Neveu, Hays, Voytek, New & Schulte 2018,
*Astrobiology* 18:1375) provides criteria for what makes a measurement convincing
evidence of life. Channels here should be scored against it rather than against
my own ad-hoc ranking rule.

## New channels

| | Channel | Why it ranks | Positive control |
|---|---|---|---|
| **C6** | Agnostic ML classifier, inverted for the shadow conjunction | Validated method, public training data verified fetchable, nobody has run the inversion | Cleaves et al. published train/test split |
| **C7** | Non-protein amino-acid alphabet | Reuses C2 data, directly named by Davies et al. | Meteoritic (abiotic) vs cultured (biotic) distributions |
| **C8** | Electrochemical disequilibrium / energy transfer | Closes two LAB pillars | Abiotic vs biotic iron oxidation signatures |

## Honest assessment of the original five

C1 and C2 were run and killed, and both produced a quantified aperture, which was
worth having. But neither was among the strongest available strategies. **C6 is
better than anything in the original set**, because it inherits a validated
classifier and a published positive control rather than requiring me to build and
justify both.

The original design's real contribution is not any single channel. It is the
conjunction operator, and Gap 1 shows exactly where that operator has the most
leverage: pointed at a tool the field already trusts, asking a question the field
has not asked of it.

## Sources

- Davies, Benner, Cleland, Lineweaver, McKay & Wolfe-Simon (2009), *Signatures of a Shadow Biosphere*, Astrobiology 9:241. [PDF](https://www.mso.anu.edu.au/~charley/papers/DaviesetalShadow.pdf)
- Cleaves et al. (2023), *A robust, agnostic molecular biosignature based on machine learning*, PNAS 120:e2307149120. [DOI](https://www.pnas.org/doi/10.1073/pnas.2307149120) · data [OSF EMBH8](https://doi.org/10.17605/OSF.IO/EMBH8)
- Benner (2017), *Detecting Darwinism from Molecules in the Enceladus Plumes...*, Astrobiology. [DOI](https://dx.doi.org/10.1089/ast.2016.1611)
- Neveu, Hays, Voytek, New & Schulte (2018), *The Ladder of Life Detection*, Astrobiology 18:1375. [link](https://www.liebertpub.com/doi/abs/10.1089/ast.2017.1773)
- [Laboratory for Agnostic Biosignatures](https://www.agnosticbiosignatures.org/about)
- *Agnostic Biosignatures: Expanding the Search for Life in the Solar System*, Annual Review of Earth and Planetary Sciences. [link](https://www.annualreviews.org/content/journals/10.1146/annurev-earth-040722-101044)
- Dorn, Adami et al., *Monomer abundance distribution patterns as a universal biosignature*. [arXiv:1101.1013](https://arxiv.org/pdf/1101.1013)
- Hystad et al. (2025), JGR Machine Learning and Computation. [DOI](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JH000441)
