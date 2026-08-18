# C7 — Non-protein amino-acid alphabet

**Verdict: KILLED ON DESIGN.** The discriminator does not discriminate, and this
is established from published literature without needing to run the search.
Run 2026-08-18.

## The intended test

Abiotic amino-acid distributions are smooth in carbon number and rich in
non-protein species — α-aminoisobutyric acid (AIB) and isovaline are the classic
markers, abundant in Murchison and Aguas Zarcas. Canonical biology is sharply
selected on ~20 protein amino acids. A shadow biosphere would be sharply selected
on *something else*. So: find a terrestrial sample that is selected but on a
non-canonical alphabet.

## Why it fails

**AIB and isovaline are made by ordinary fungi.** They are the defining residues
of *peptaibols* (peptaibiotics), a large family of non-ribosomal peptides
produced by cosmopolitan filamentous microfungi, notably *Trichoderma*. AIB is
described in that literature as a *specific marker for fungal polypeptides*, and
peptaibol production is explicitly flagged as a confound for interpreting AIB and
isovaline in both recent and ancient sediments.

So a terrestrial sample showing abundant non-protein amino acids has a mundane
canonical explanation available before any exotic one is considered. The
signature is not diagnostic.

## The pattern — and this is the real finding

This is the **third** channel killed by the same mechanism:

| Channel | Proposed shadow marker | Canonical life already makes it via |
|---|---|---|
| C2 | D-amino acids | peptidoglycan (D-Ala, D-Glu); racemases (D-Asp, D-Ser) |
| C7 | non-protein amino acids | fungal peptaibols (AIB, isovaline) |
| C6a | "non-canonical" molecular selectivity | classifier generalizes across canonical diversity |

> **The "canonical life" null hypothesis is far wider than shadow-biosphere
> detection schemes assume.** Chemistry-based shadow markers are built against a
> caricature — "the 20 protein amino acids, L-only, phosphate backbone" — and
> Earth's actual biosphere routinely operates outside it. Every marker proposed
> as evidence of a *second* origin turns out to be within the first one's range.

That is a substantive conclusion about the detection programme, not about this
project's plumbing, and it is the most transferable thing found so far. It
predicts that any *chemical* shadow marker will have far less discriminating
power than it appears to, and it implies the search should move away from
"molecule X is non-canonical" toward relational or organisational signatures
where the canonical null is genuinely narrow.

## Data status, recorded for completeness

The positive-control data exists but is not machine-readable at useful scale.
Glavin et al. 2021 (*MAPS* 56:148) Table 1 gives full-suite abundances for Aguas
Zarcas, Murchison **and the Aguas Zarcas recovery-site soil** — a terrestrial
sample analysed by the same method, which is exactly the right control pairing.
It is a PDF table with wrapped values and misaligned columns; automated parsing
would inject silent errors of the kind this project has already been caught by
once. Manual transcription would yield n ≈ 6.

There is no archive of terrestrial environmental samples analysed with full
non-protein amino-acid suites at scale. Full-suite analysis is largely a
meteoritics technique applied to meteorites.

Neither limitation is why C7 is killed. It is killed because the marker is not
diagnostic.

## Sources

- Peptaibols / AIB as fungal marker: [Amino Acids, use of AIB and isovaline as marker amino acids for fungal polypeptide antibiotics](https://link.springer.com/article/10.1007/BF00806923); [marine-derived peptaibols review](https://pmc.ncbi.nlm.nih.gov/articles/PMC12734927/)
- AIB/isovaline in terrestrial sediment: [Tokyo Bay sediments](https://www.sciencedirect.com/science/article/abs/pii/S0016703797003268)
- Meteoritic reference: [Glavin et al. 2021](https://onlinelibrary.wiley.com/doi/10.1111/maps.13451)
