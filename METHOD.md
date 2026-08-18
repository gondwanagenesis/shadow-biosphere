# Method

## The problem with the usual framing

"Search for organisms whose sequences don't match anything known" cannot work.
Sequencing is a homology-based assay: PCR primers assume conserved rRNA,
assembly assumes canonical base-pairing, and taxonomic assignment assumes a
reference database. A lineage from an independent origin is excluded by the
method before the analysis begins. Unassigned reads are not evidence of a second
origin; they are uncatalogued members of the first one.

This is why "microbial dark matter" — huge, well-funded, decades old — has never
been able to address the question. It is the wrong aperture, pointed harder.

## Aperture and filter

Every assay has an **aperture**, what it physically responds to, and a **filter**,
what it structurally excludes. Sorting the archives this way reorganizes the
entire search:

**Physics-aperture** — responds to matter itself, sees anything:
mass and mass defect, light scattering and refractive index, vibrational modes,
isotope ratios, elemental composition, chirality, electron density, charge
mobility, heat.

**Biology-aperture** — responds to homology, sees only our lineage:
PCR, sequencing, hybridization, antibodies, culture, enzyme assays, nucleic-acid
stains.

The filters **compose multiplicatively**. A silica-column extraction already
selected for a phosphate backbone under chaotropic salt; a ligation step already
required canonical duplex ends; a motor protein already required a grip it
evolved for. By the time a sample reaches a basecaller, several independent
lineage filters have been applied, and their joint passband has never been
measured.

So the operational question is not "where is the anomaly in the data?" It is:

> **Which archived data was collected *before* the filter that would have
> removed shadow life?**

Which means the best archives are the ones collected earliest in the pipeline —
raw signal, raw spectra, raw images — before homology-based interpretation.

## The conjunction operator

No single physics channel survives its own confounds. Scattering has detritus,
mass spectrometry has anthropogenic contamination, isotopes have abiotic
fractionation, chirality has racemization.

So a candidate requires a **conjunction**: physics-aperture positive AND
biology-aperture null, on the *same physical sample*, in ≥ 2 orthogonal physics
channels. Each channel alone has on the order of 10⁴ false positives; the
intersection of orthogonal ones is near zero.

This makes the project a **cross-archive conjunction search**, and it makes
co-registered programmes the substrate — Tara Oceans, HOT/BATS, IODP cores,
Deep Carbon Observatory, SeaFlow — because they ran multiple channels on the same
water or the same core.

## Channel ranking criterion

Channels were ranked by one rule, and it did the real work:

> **Prefer channels whose dominant confound has a quantitative null model
> testable inside the archive itself.**

"Geochemistry, probably" is not a null model you can refute. Racemization rate
ordering is: first-order kinetics predicts a strict ordering across amino acids,
so a biological D-excess is distinguishable from a diagenetic one *within the
same table*. Diel periodicity is: detritus has no reason to divide on a 24 h
clock.

This is why multi-isotope off-slope hunting was demoted despite being appealing —
our knowledge of *canonical* fractionation is itself incomplete, so the null is
soft. And why bulk Redfield-ratio anomalies were dropped entirely: the confound
space swamps the effect.

## Guards

Adapted from the `new-idea` protocol used to generate the channels.

1. **Kill tests written before the search**, committed to git before any result
   exists. Deviations logged in `AMENDMENTS.md`, never by editing the
   pre-registration.
2. **Positive controls as code gates.** A channel that cannot recover a *known*
   signal may not report a null. C1 proved why: its first implementation produced
   a clean-looking null that also nulled *Prochlorococcus*, whose diel cycle is
   published from that same instrument. The gate caught it. Prose would not have.
3. **Planted controls.** One idea believed false, one believed already known,
   carried through the ranking. If they rank competitively, the ranking is
   reported broken rather than trusted.
4. **The prior is stated in advance and it is low.** Four billion years of
   competition, HGT homogenization, 150 years of microbiology, and every prior
   claim collapsed (GFAJ-1 arsenic, nanobes). Well under 1%.

## Why run it anyway

The expected output is negative results and a measured detection limit — and
those have real value, because nobody has published the aperture width of
standard microbiology. C1 already delivered one number of that kind: 18.0% of
detected particles discarded at a single curation step.

The secondary yield is also real. Searching for high-selectivity molecules in
vacant formula space finds novel natural products whether or not they came from a
second origin; mining discarded cytometry gates characterizes what is actually in
them. The lottery ticket is attached to work that pays out regardless.

That distinction — between a search with a null-result yield and a search that
only pays out on the extraordinary claim — is what separates this from the
history of the field.
