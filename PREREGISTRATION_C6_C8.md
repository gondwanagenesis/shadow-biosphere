# Pre-registration — channels C6–C8

**Committed before any C6/C7/C8 result exists.** Same rule as
`PREREGISTRATION.md`: never edited after the first result lands; corrections go
to `AMENDMENTS.md`. Added after the literature sweep documented in `GAPS.md`.

---

## The assumption every published "agnostic" classifier rests on

Every validated biotic/abiotic classifier in the literature trains its **biotic
class entirely on canonical Earth life**. The learned decision boundary is
therefore "canonical-life-like vs abiotic," not "life vs non-life." That these
coincide is an *assumption*, and as far as the sweep found, it has never been
tested.

It has a consequence that inverts the naive shadow search. If the classifier
learned genuine, substrate-independent selectivity, a shadow biosphere lands in
**biotic** and is filed as unremarkable. If it merely memorized canonical
biochemistry, a shadow biosphere lands in **abiotic** — actively discarded as
geology. These predict opposite search strategies, and nothing in the literature
distinguishes them.

**C6 tests this first, because the answer determines what C6 even means.**

---

## C6 — Agnostic classifier, inverted

Data: Cleaves et al. 2023, OSF `EMBH8` (verified public, 221 MB, 150 datasets).

### C6a — POSITIVE CONTROL AND PRIMARY RESULT: does "agnostic" generalize?

- **Test:** leave-one-domain-out cross-validation. Hold out an entire biotic
  domain (e.g. train on bacteria + eukarya, test on archaea; and each other
  partition the labels support). Compare to random-fold accuracy.
- **Null:** a genuinely agnostic classifier suffers little loss when the held-out
  biotic domain is unseen.
- **Threshold:** report the accuracy gap between random-fold and
  leave-one-domain-out. A drop of >15 percentage points on held-out biotic
  domains indicates memorization of canonical biochemistry rather than
  substrate-independent selectivity.
- **Interpretation is fixed in advance, both ways:**
  - small drop → agnosticism supported → shadow life would classify BIOTIC →
    proceed to C6b as designed.
  - large drop → agnosticism overstated → **shadow life would classify ABIOTIC**
    → the search inverts, and the target becomes samples the classifier calls
    abiotic that nonetheless carry selectivity signatures.
- **This is a publishable methodological result either way** and does not depend
  on shadow life existing.
- **KILLED IF:** the deposited labels do not support a domain partition with
  enough samples per class to make the comparison meaningful (report as
  underpowered, do not force it).

### C6b — the shadow conjunction

- **Test:** samples classified BIOTIC at high confidence that additionally carry
  **no canonical biomarkers** (hopanes, steranes, recognizable lipid suites) and
  **no amplifiable sequence**.
- **Null:** every high-confidence biotic sample carries canonical biomarkers.
- **Threshold:** reproduced across independent studies and both classifier
  families.
- **KILLED IF:** every biotic-classified sample carries canonical biomarkers, OR
  the biomarker-null cases are explained by thermal maturity / degradation, which
  destroys biomarkers without implying alien chemistry. **This confound is
  expected to dominate and is stated in advance.**

### C6c — residuals, not accuracy

- **Test:** persistent misclassification. A third class appears as *reproducible*
  error — stable across retrains, folds, seeds and feature subsets. Random error
  scatters; a third class clusters in feature space.
- **Statistic:** per-sample misclassification frequency over ≥100 retrains, then
  clustering of the persistently-misclassified set.
- **KILLED IF:** persistent misclassifications do not cluster, OR they cluster by
  a known nuisance variable (instrument, lab, run date, sample prep).

### C6d — deep time (see GAPS.md, reframe)

- **Rationale, stated in advance:** the standard argument against an *extant*
  shadow biosphere is that 4 Gyr of competition would have eliminated it. That
  argument says nothing against one that existed and died. Early Earth had no
  incumbent. **The prior for an extinct shadow biosphere is materially higher**,
  and py-GC-MS reads molecular fossils.
- **Test:** organic matter classified BIOTIC at high confidence in rocks whose
  age or biomarker inventory is incompatible with the canonical record.
- **KILLED IF:** explained by thermal maturity, contamination by younger carbon
  (the dominant failure mode in Archean organic geochemistry), or metamorphic
  alteration.

## C7 — Non-protein amino-acid alphabet

- **Test:** is any sample *selected* but on a non-canonical alphabet? Abiotic
  distributions are smooth in carbon number and rich in α-aminoisobutyric acid
  and isovaline. Canonical biology is sharply selected on ~20. A shadow
  biosphere is sharply selected on something else.
- **Statistic:** selectivity (concentration of abundance on few monomers, e.g.
  normalized entropy of the monomer abundance distribution) crossed with overlap
  against the canonical 20.
- **POSITIVE CONTROL:** meteoritic (abiotic, smooth, AIB-rich) and cultured
  biomass (canonical, selected) must separate cleanly on the selectivity
  statistic. If they do not, the statistic is broken and nothing is interpreted.
- **KILLED IF:** high-selectivity non-canonical alphabets are explained by
  degradation, analytical derivatization artifacts, or contamination.

## C8 — Electrochemical disequilibrium / energy transfer

- **Test:** redox chemistry inconsistent with abiotic electrochemistry in
  archived sediment microelectrode / voltammetry profiles.
- **POSITIVE CONTROL:** known biotic vs abiotic iron oxidation must separate on
  the chosen statistic before anything else is examined.
- **KILLED IF:** no public archive supports the measurement at usable scale
  (report as blocked, with the specific reason, rather than as a null).

## C6–C8 cross-channel operator: classifier disagreement

Independent agnostic classifiers exist on different features — py-GC-MS random
forest, LUMOS amino-acid HOMO-LUMO gaps, assembly theory on MS², monomer
abundance distributions. Canonical life should be classified **consistently** by
all of them. A third class produces maximal **disagreement**.

This is the conjunction operator lifted from the measurement level to the
classifier level. It is only run if ≥2 classifiers can be applied to the same
samples, and it is reported as blocked otherwise.

## Prior, restated

Unchanged and low for an extant shadow biosphere. **Raised, but still below 5%,
for an extinct one**, on the competition argument above. Every C6 sub-test is
expected to return negative or to be dominated by thermal maturity confounds.
C6a is expected to return a real methodological result regardless.
