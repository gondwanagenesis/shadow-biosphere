# C8 — Electrochemical disequilibrium / energy transfer

**Verdict: KILLED ON DESIGN.** No data acquisition attempted, because the
discriminator cannot work in principle on Earth. Run 2026-08-19.

## The intended test

NASA's Laboratory for Agnostic Biosignatures organises detection around chemical
complexity, disequilibrium, compartmentalisation, and **energy transfer** — the
last seeking redox chemistry inconsistent with abiotic electrochemistry, on the
grounds that biotic and abiotic iron oxidation have distinct electrochemical
signatures. C8 was added to close that gap.

## Why it cannot work here

**The set of thermodynamically favourable redox couples in an environment is
fixed by geochemistry, not by biology.** Any organism exploiting a couple draws
it down the same way, because thermodynamics constrains the outcome regardless of
which enzymes mediate it. Canonical microbial life already saturates essentially
every accessible redox niche on Earth.

So an electrochemical disequilibrium signature says *something is metabolising
here*. It cannot say *whose metabolism*. On Earth, "whose" is the entire question.

This is acknowledged in the literature, if not always emphasised: existing Earth
life already occupies redox gradients throughout the environment, which makes
distinguishing a second genesis from known biospheric activity very difficult.

## The general point

The LAB pillars were designed for **Mars, Europa and Enceladus** — worlds where
the background hypothesis is *no life*. There a biochemistry-agnostic detector is
exactly right, because any positive is a discovery.

Earth's background hypothesis is *abundant life*. Importing those methods here
inherits their reference class, and that reference class is wrong for this
question:

> **Agnostic biosignatures are agnostic about biochemistry, but not about
> lineage.** On a sterile world that is sufficient. On Earth, lineage *is* the
> question, so agnosticism about biochemistry buys nothing.

This is the same failure identified in `GAPS.md` for the ML classifiers — every
validated agnostic method separates biotic from abiotic, none separates our
biotic from another biotic — reached here from thermodynamics rather than from
training-set composition.

## The narrow version that might survive

One formulation is not obviously dead: a redox couple that is thermodynamically
favourable but that **canonical life demonstrably cannot exploit**, being drawn
down somewhere. A "missing sink" argument.

It is weak. It requires proving a negative about canonical enzymatic capability,
and unused couples usually have kinetic barriers that explain non-use abiotically.
Recorded as the residual rather than pursued.
