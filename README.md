# Trust Circles *(working title)*

> **A matching engine for high-quality social circles, built on a graph of real-world trust.**
>
> Most platforms match people by shared interests. Interests get people into the same room — trust is what makes them want to stay in it. This project adds a *trust layer* on top of interest-based matching, so that the people placed in a circle actually want to be with *each other*, not just with the hobby.

**Status:** 🟡 Phase 0 — Specification & Design
**Track:** Open — may become a startup, an academic research project (M.Sc. track), or both.

---

## Table of Contents

1. [The Problem](#1-the-problem)
2. [The Idea in One Paragraph](#2-the-idea-in-one-paragraph)
3. [What This Is NOT](#3-what-this-is-not)
4. [Core Concepts](#4-core-concepts)
5. [Locked Design Decisions (v0)](#5-locked-design-decisions-v0)
6. [Open Questions, Framed as Hypotheses](#6-open-questions-framed-as-hypotheses)
7. [Phase 1 — The Simulation Lab](#7-phase-1--the-simulation-lab)
8. [Phase 2 — The Concierge Pilot](#8-phase-2--the-concierge-pilot)
9. [Phase 3 — Decision Gate](#9-phase-3--decision-gate)
10. [Proposed Repository Structure](#10-proposed-repository-structure)
11. [Tech Stack](#11-tech-stack)
12. [Glossary](#12-glossary)
13. [Reading List](#13-reading-list)
14. [Roadmap](#14-roadmap)

---

## 1. The Problem

Interest-based communities (Meetup groups, Facebook groups, WhatsApp communities, running clubs) suffer from the same failure mode: **high churn, low cohesion**. Two people can both love running, entrepreneurship, and chess — and still have zero social chemistry. Matching on interests alone optimizes for *topic overlap*, not for *human fit*.

Meanwhile, the strongest social circles in real life form through a different mechanism: **friends of friends**. People vouch for each other implicitly. That vouching signal — real-world trust — is exactly what existing platforms don't capture.

**The bet of this project:** a circle assembled from people who share interests *and* are embedded in overlapping webs of real trust will survive and thrive dramatically more often than a circle assembled from interests alone.

---

## 2. The Idea in One Paragraph

Every user is a node in a **Trust Graph**. Users don't "like" or "rate" each other — they *attest*: "I genuinely know this person in real life." Each attestation is an edge. From the structure of this graph, the system derives a hidden **credibility signal** (never shown to anyone), inspired by trust-propagation algorithms like Personalized PageRank and TrustRank. The **matching engine** then forms circles of ~5–7 people by combining: shared interests, compatible attributes (location, age, language, availability), **graph proximity** (mutual connections, short trust paths), and a minimum credibility floor that filters out fake or manipulated accounts. The product's single job is to be the **matchmaker** — the circle itself lives wherever people want it to live (WhatsApp group + physical meetups, in v1).

---

## 3. What This Is NOT

Setting boundaries early prevents both scope creep and ethical drift:

- **Not a social network.** No feed, no likes, no content, no chat (v1 uses WhatsApp). We build the matching engine only.
- **Not a people-rating system.** Nobody rates anybody's *worth*. An attestation means "I know this person," never "this person is good." Credibility measures *position in the trust graph*, nothing else.
- **Not a reputation score.** Scores are invisible — to the user, to others, to circle admins. No leaderboards, ever. This is a deliberate defense against both gamification and "social credit score" dynamics.
- **Not discriminatory.** Matching never uses identity, worldview, or protected attributes as quality signals. Attributes like language or location are compatibility filters chosen by the user, not rankings.

---

## 4. Core Concepts

### 4.1 Trust Graph
A directed graph `G = (V, E)` where nodes are users and each edge `(u → v)` is a **trust attestation**: user *u* declares they personally know user *v*. The graph is the system's single source of truth about real-world social structure.

### 4.2 Trust Attestation
A deliberate, scarce, accountable action — not a like:
- **Deliberate:** the user actively vouches for a real acquaintance.
- **Scarce:** each user has a limited attestation budget (exact numbers = tunable parameter, see §5-D5).
- **Accountable:** attestations are tied to the inviter chain (see Invite Tree), so abuse is traceable and prunable.

### 4.3 Credibility — Two Different Signals (Important!)
The original spec used "credibility" for two things that are actually distinct. This project separates them explicitly:

| Signal | What it is | What it's used for |
|---|---|---|
| **Global credibility floor** | A single scalar per user, derived from trust propagation seeded at verified anchor nodes (TrustRank-style). | **Filtering only.** Accounts below the floor are excluded from matching. This is the anti-Sybil / anti-fake mechanism. |
| **Personalized trust vector** | For each user *u*, a vector of trust values toward all other users, computed via Personalized PageRank rooted at *u*. | **Matching.** Answers "how socially close is candidate *v* to user *u*?" — mutual friends and short trust paths score high. |

**Why this split matters:** a global score answers "is this account real and healthy?" but *cannot* answer "will these specific seven people click?" Graph proximity can. The matchmaker uses proximity as a feature; the global score is only a gate.

### 4.4 Matching Engine
Given a pool of eligible users (above the credibility floor), the engine scores candidate circles using a weighted combination of:
- Interest overlap
- Attribute compatibility (location, age band, language, availability)
- **Pairwise graph proximity** (from personalized trust vectors)
- Circle-level balance constraints (size 5–7, no isolated members)

Exact weights are Phase-1/Phase-2 outputs, not upfront guesses.

### 4.5 Circle
v1 definition: a group of 5–7 matched people, instantiated as a WhatsApp group + a recurring physical meetup. The app's involvement ends at introduction + light nudges; the relationship lives in the real world.

---

## 5. Locked Design Decisions (v0)

These are **decided**. Everything else in this document is a hypothesis.

| # | Decision | Rationale |
|---|---|---|
| **D1** | **The product is a matchmaker, not a network.** No feed, no chat, no content in v1. | WhatsApp already exists. Cuts ~70% of build scope; sharpens differentiation. |
| **D2** | **Full privacy of trust data.** Credibility scores and the trust graph are never displayed — not your own, not others'. | Prevents score-gaming, status anxiety, and "social credit" optics. Users optimize for real relationships, not numbers. |
| **D3** | **Onboarding via invite tree with one-time keys.** An existing user generates a single-use key; the newcomer redeems it at signup; only then can trust attestations flow. | Simultaneously solves acquaintance verification *and* Sybil resistance: fake branches have an accountable root and can be pruned as a subtree. |
| **D4** | **Trust model = Personalized PageRank for matching + TrustRank-style global floor for filtering.** | See §4.3. Trust-propagation from anchor seeds is inherently Sybil-limiting: fake clusters connect to the honest region through few "attack edges," which bottlenecks the trust that can flow in. |
| **D5** | **Everything numeric is a tunable parameter, not a decision.** Attestation budget, replenishment rate, decay, expiry, revocability — all configurable, all calibrated by simulation (Phase 1), not by debate. | Turns endless spec arguments into measurable experiments. |
| **D6** | **v1 circle = hybrid (WhatsApp group + physical meetups), size 5–7.** | Small enough for cohesion, large enough to survive dropouts. |

---

## 6. Open Questions, Framed as Hypotheses

Every open item from the original spec maps to a hypothesis with a defined test. Nothing stays vague.

| ID | Hypothesis | How it's tested | Phase |
|---|---|---|---|
| **H1** | Circles matched with the trust layer (proximity + floor) survive significantly longer than circles matched on interests alone. | Controlled pilot: 50% of circles matched with full algorithm, 50% interests-only. Primary metric: survival to 3rd meetup. | **2** |
| **H2** | PPR/TrustRank-based credibility limits the score attainable by Sybil clusters and collusion rings to a bounded, acceptable level. | Simulation: inject attack scenarios into synthetic + real graphs; measure attacker credibility gain. | **1** |
| **H3** | The invite tree keeps fake-account penetration low **without** strangling organic growth. | Simulation (growth models under different key-budget policies) + observed friction in pilot onboarding. | **1 + 2** |
| **H4** | Legitimate newcomers (few edges, real people) are **not** unfairly gated out by the credibility floor. | Simulation: measure false-positive rate on honest low-degree nodes across parameter sweeps. This is the mirror image of H2 — the cold-start fairness problem. | **1** |
| **H5** | A concrete parameter set (attestation budget, decay rate, floor threshold) exists that satisfies H2 and H4 *simultaneously*. | Parameter sweep + Pareto analysis in the simulation lab. Output: the v1 default config. | **1** |
| **H6** | Hidden scores prevent gaming behavior (no observable score-optimization strategies emerge among pilot users). | Qualitative observation + exit interviews in pilot. | **2** |
| **H7** | Users are willing to make trust attestations at all (the "vouching" action feels natural, not awkward). | Pilot onboarding funnel: % of users completing ≥3 attestations. | **2** |
| **H8** | Circle-management mechanics (admins, join/leave, reporting, blocking) can be copied from proven community patterns and iterated — they are not novel risk. | Deferred to MVP; pilot circles are concierge-managed by the founder. | **3** |

**Explicitly deferred (post-gate):** circle admin roles, join-request flows, circle quality ratings, reporting/moderation tooling, trust-graph privacy *architecture* (encryption at rest, access control) — noted, owned, but not blocking.

---

## 7. Phase 1 — The Simulation Lab

### 7.1 What it is, in plain words
A **wind tunnel**. Before an airplane carries passengers, a model flies in a controlled airstream. Before this system touches real users, the trust algorithm runs on simulated and public research networks, gets *attacked on purpose*, and gets calibrated — all in Python, all measurable, zero user risk.

This phase answers, with numbers instead of opinions, every algorithmic open question from the original spec: the credibility formula, decay, attestation budgets, and Sybil defense.

### 7.2 Why simulation first
1. **The core risk is algorithmic, not UI.** If the trust math is gameable or unfair, no amount of product polish saves it.
2. **Attacks can't be ethically tested on real users.** Fake-account floods and collusion rings must be studied in vitro.
3. **It's dual-use by design:** the same codebase is startup IP *and* the experimental apparatus of a potential M.Sc. research project.

### 7.3 Components to build

```
simlab/
├── graphs/          # Graph sources
│   ├── synthetic.py     # Generators: Watts–Strogatz, Barabási–Albert,
│   │                    # community-structured (LFR benchmark)
│   └── real.py          # Loaders for public datasets (Stanford SNAP:
│                        # facebook_combined ego-networks, etc.)
├── trust/           # Trust algorithms
│   ├── ppr.py           # Personalized PageRank (per-user trust vectors)
│   ├── trustrank.py     # Seeded global propagation (credibility floor)
│   └── decay.py         # Time-decay & inactivity models
├── attacks/         # The adversary suite
│   ├── sybil_cluster.py    # N fake nodes attesting to each other
│   ├── collusion_ring.py   # Real friends inflating each other artificially
│   ├── edge_purchase.py    # Attacker "buys" attestations from real users
│   └── invite_abuse.py     # Abusing the invite tree (deep fake branches)
├── matching/        # Circle formation
│   └── engine.py        # Interest + attribute + proximity scoring,
│                        # circle assembly (constrained clustering)
├── metrics/         # What we measure
│   ├── attack_gain.py      # Max credibility an attacker achieves
│   ├── fairness.py         # False-positive rate on honest newcomers (H4)
│   └── circle_quality.py   # Intra-circle proximity, balance
└── experiments/     # Reproducible notebooks, one per hypothesis
    ├── exp_h2_sybil_resistance.ipynb
    ├── exp_h4_newcomer_fairness.ipynb
    └── exp_h5_parameter_sweep.ipynb
```

### 7.4 The two numbers that matter
Every experiment ultimately reports a trade-off between:

- **Attack Gain (must be LOW):** given attack budget *k* (fake nodes / bought edges), what is the maximum credibility and matching-eligibility an attacker achieves?
- **Newcomer Penalty (must be LOW):** what fraction of *honest* new users with few connections fall below the credibility floor and get unfairly excluded?

These pull in opposite directions — a stricter floor blocks attackers *and* newcomers. Phase 1's deliverable is the **Pareto frontier** of this trade-off and a recommended operating point (the v1 config).

### 7.5 Deliverables
- [ ] Reproducible simulation codebase (this repo)
- [ ] Calibrated v1 parameter set (attestation budget, decay, floor threshold)
- [ ] Attack-resistance report with plots (H2, H3, H4, H5)
- [ ] *(Optional, research track)* Draft paper / thesis-proposal material: *"Sybil-resistant trust propagation for small-group social matching"*

---

## 8. Phase 2 — The Concierge Pilot

### 8.1 What it is, in plain words
**The founder is the app.** One real community, a simple sign-up form, and manual (algorithm-assisted) circle assignments. No product is built; the *hypothesis* is tested. If trust-based circles don't outperform interest-based circles when a human runs the algorithm by hand, they won't outperform inside an app either — and that answer costs 8 weeks instead of a year of development.

### 8.2 Choosing the launch community
Three criteria, in order of importance:

1. **Existing acquaintance density.** The trust graph needs *triangles* (friends who share friends), not a star centered on the founder. A community where members already know each other.
2. **Existing meetup infrastructure.** Physical gatherings must be logistically easy (shared campus / city / venue).
3. **Founder leverage.** A community where the founder has standing, access, and distribution.

Candidate communities should be scored against these three explicitly before choosing. *(Current leading candidates: a university student community, a cloud/tech community, a sports community — decision open.)*

### 8.3 Pilot protocol (8 weeks, ~40–80 participants)

| Week | Activity |
|---|---|
| **0** | Build intake form (profile, interests, availability, language + trust attestations: "select people on this list you genuinely know"). Consent text: data use, anonymity, right to withdraw. |
| **1** | Recruit 40–80 participants through community channels. Collect responses. |
| **2** | Run Phase-1 code offline on the collected graph. Form circles of 5–7. **Randomized split: 50% of circles via full algorithm (interests + attributes + trust proximity + floor), 50% via interests + attributes only.** Participants are never told which arm they're in. |
| **3** | Launch: each circle gets a WhatsApp group + a suggested first meetup (founder lightly facilitates scheduling, identically for both arms). |
| **3–8** | Observe. Minimal intervention, identical across arms. Track meetups via a 30-second weekly check-in message. |
| **8** | Measure, interview, write up. |

### 8.4 Metrics

**Primary (the whole ballgame):**
- **Circle survival rate to 3rd meetup**, treatment vs. control.

**Secondary:**
- Average meetups per circle; WhatsApp activity as engagement proxy
- "Would you want to keep meeting this group?" (1–5, end-of-pilot survey)
- Attestation funnel: % completing ≥3 attestations (H7)
- Onboarding friction notes (H3), gaming-behavior observations (H6)

**Honest success bar:** treatment circles survive at a meaningfully higher rate (target: ≥1.5× control survival). With ~6–12 circles per arm this won't be publication-grade statistics — it's a directional signal strong enough to justify (or kill) the next investment. A larger, statistically powered replication is a Phase-3 option on the research track.

### 8.5 Ethics notes
- Participants consent to data collection and to being matched by an experimental method.
- Trust attestations are confidential — no participant ever learns who attested (or didn't attest) to them.
- No deception beyond arm-blinding; full debrief at pilot end.

---

## 9. Phase 3 — Decision Gate

Phase 1 and Phase 2 outputs converge here:

| Outcome | Path |
|---|---|
| **H1 confirmed + H2/H4/H5 satisfied** | Build the MVP. All circle-mechanics questions (H8) get answered from pilot observations, not guesses. Startup track opens; pilot data becomes the seed of the pitch. |
| **H1 confirmed, algorithm needs work** | Iterate in the sim lab; re-pilot with new config. |
| **H1 rejected** | The core bet is wrong — and that's a *clean, cheap* answer. Remaining assets: a rigorous simulation codebase, an attack-resistance study (publishable / thesis-grade), and a documented experiment. Research track continues; product track closes. |

**No outcome wastes the work.** That is the point of this structure.

---

## 10. Proposed Repository Structure

```
trust-circles/
├── README.md                # ← this file
├── docs/
│   ├── spec-he.md           # Original Hebrew product spec
│   ├── decisions.md         # Decision log (D1–D6 + future ADRs)
│   └── pilot-protocol.md    # Phase 2 detailed protocol & consent text
├── simlab/                 # Phase 1 (structure in §7.3)
├── pilot/                   # Phase 2 tooling
│   ├── intake-form/         # Form definition / simple web page
│   └── analysis/            # Post-pilot notebooks
└── LICENSE
```

---

## 11. Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Simulation | **Python 3.12, NetworkX, NumPy, pandas** | Fast iteration; NetworkX has PageRank/PPR built in; graphs at this scale (10²–10⁵ nodes) don't need heavier tooling yet. |
| Datasets | **Stanford SNAP** public social graphs | Real social topology, anonymized, standard in the literature. |
| Experiments | **Jupyter + matplotlib** | Reproducible, shareable, thesis-ready. |
| Pilot intake | Simple static page / form → CSV/JSON | Zero backend needed for ≤100 users. |
| MVP (post-gate) | *Deliberately undecided* | Choosing infrastructure before the gate is premature. |

---

## 12. Glossary

| Term | Meaning |
|---|---|
| **Trust attestation** | A user's declaration: "I personally know this person." An edge in the trust graph. Not a like, not a rating. |
| **Sybil attack** | Creating many fake identities to manipulate a reputation/trust system. Named after a famous case study of multiple-personality disorder. |
| **Collusion ring** | Real users coordinating attestations to artificially inflate each other. |
| **Attack edge** | An edge connecting the fake/colluding region of the graph to the honest region. Trust-propagation defenses work because these are scarce. |
| **PageRank** | Google's classic algorithm: a node is important if important nodes point to it. Computed via random walks on the graph. |
| **Personalized PageRank (PPR)** | PageRank where random walks restart at a *specific user*, yielding trust "from that user's point of view." Powers graph-proximity matching. |
| **TrustRank** | PageRank variant seeded at manually verified trustworthy nodes; trust flows outward from them. Powers the global credibility floor. |
| **Invite tree** | Signup structure where every account traces to the existing member who issued its one-time key. Fake branches can be pruned as subtrees. |
| **Credibility floor** | Minimum global credibility required to enter the matching pool. A gate, not a ranking. |
| **Concierge MVP** | Testing a product hypothesis by performing the service manually before building software. |
| **Pareto frontier** | The set of parameter configurations where improving one metric (blocking attackers) necessarily worsens the other (admitting newcomers). |

---

## 13. Reading List

- Kamvar, Schlosser, Garcia-Molina — **The EigenTrust Algorithm for Reputation Management in P2P Networks** (WWW 2003)
- Gyöngyi, Garcia-Molina, Pedersen — **Combating Web Spam with TrustRank** (VLDB 2004)
- Cao, Sirivianos, Yang, Pregueiro — **SybilRank: Aiding the Detection of Fake Accounts in Large Scale Social Online Services** (NSDI 2012)
- Yu, Kaminsky, Gibbons, Flaxman — **SybilGuard: Defending Against Sybil Attacks via Social Networks** (SIGCOMM 2006)
- Douceur — **The Sybil Attack** (IPTPS 2002)
- Stanford SNAP dataset collection — https://snap.stanford.edu/data/

---

## 14. Roadmap

- [x] **Phase 0.1** — High-level product spec (Hebrew, `docs/spec-he.md`)
- [x] **Phase 0.2** — Lock decisions D1–D6 into `docs/decisions.md`; translate open questions into hypotheses H1–H8
- [x] **Phase 1.1** — Repo scaffold + graph generators (SNAP loaders: TODO)
- [x] **Phase 1.2** — PPR + TrustRank implementations (unit tests: TODO)
- [ ] **Phase 1.3** — Attack suite (Sybil cluster, collusion ring, edge purchase, invite abuse)
- [ ] **Phase 1.4** — Experiments H2/H4/H5 → Pareto analysis → **v1 parameter config**
- [ ] **Phase 1.5** — *(Optional)* Research write-up / thesis proposal
- [ ] **Phase 2.1** — Choose launch community (criteria §8.2); write pilot protocol + consent
- [ ] **Phase 2.2** — Intake form + recruitment (40–80 participants)
- [ ] **Phase 2.3** — Run matching (A/B), launch circles, 8-week observation
- [ ] **Phase 2.4** — Analysis: H1 verdict
- [ ] **Phase 3** — Decision gate: MVP / iterate / research-only

---

*Spec originally drafted in Hebrew; this README is the canonical English project overview. The trust layer is an internal engine serving one goal — circles people genuinely want to stay in — never an end in itself.*
