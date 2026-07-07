# Web of Trust

> **A matching engine for high-quality social circles, built on a graph of real-world trust.**
>
> Most platforms match people by shared interests. Interests get people into the same room — trust is what makes them want to stay in it. This product adds a *trust layer* so that the people placed in a circle actually want to be with *each other*, not just with the hobby.

**Status:** 🟡 Specification phase · **Spec v0.6** (changelog at bottom)
**Current mode:** SPEC REFINEMENT ONLY — development is intentionally frozen. This repo deliberately contains nothing but this document.
**Track:** Open — may become a startup, an academic research project (M.Sc. track), or both. Every step is designed to serve both tracks until a decision gate.

---

## ⚠️ READ THIS FIRST (for the founder's future self, and for any AI model continuing this work)

1. **This document is the single source of truth.** Everything known about the product is here. A prototype codebase once existed and was deliberately deleted to enforce spec-first discipline; its *findings* are preserved in §9.3 and it can be rebuilt from §9 whenever the spec is ready.
2. **Do not build anything yet.** The founder explicitly froze development. The current work is thinking: answering the open questions in §7, in order.
3. **How this spec is developed (the working protocol):** the AI asks the founder at most 2–3 *deep* questions per round → the founder answers → answers get locked as numbered Decisions (D1, D2, …) → open items become numbered Open Questions (OQ-1, …) → version bumps, changelog updated. Never relitigate a locked decision unless the founder explicitly reopens it. Continue exactly this protocol.
4. **Immediate next step:** resolve OQ-1 and OQ-2 (§7.1) — both already have recommendations on the table awaiting a yes/no. Then run the deep-dive on OQ-3, which is the heart of the system.
5. **Language note:** the founder thinks and answers in Hebrew; this document is kept in English as the canonical public spec. Both are fine.

---

## Table of Contents

1. [The Problem](#1-the-problem)
2. [The Idea](#2-the-idea)
3. [What This Is NOT — Boundaries & Ethics](#3-what-this-is-not--boundaries--ethics)
4. [Core Concepts](#4-core-concepts)
5. [The Central Hypothesis (H9)](#5-the-central-hypothesis-h9)
6. [Locked Decisions (D1–D13)](#6-locked-decisions-d1d13)
7. [Open Questions (the current frontier)](#7-open-questions-the-current-frontier)
8. [Secondary Hypotheses (H1–H8)](#8-secondary-hypotheses-h1h8)
9. [Validation Plan (three phases) & Preliminary Findings](#9-validation-plan-three-phases--preliminary-findings)
10. [Optional Ideas & Future Directions](#10-optional-ideas--future-directions)
11. [Recommended Order of Attack (next work session)](#11-recommended-order-of-attack-next-work-session)
12. [Glossary](#12-glossary)
13. [Reading List](#13-reading-list)
14. [Changelog](#14-changelog)

---

## 1. The Problem

Interest-based communities (Meetup groups, Facebook groups, WhatsApp communities, running clubs) share one failure mode: **high churn, low cohesion**. Two people can both love running, entrepreneurship, and chess — and still have zero social chemistry. Matching on interests optimizes for *topic overlap*, not for *human fit*.

The strongest real-life social circles form through a different mechanism: **friends of friends** — people implicitly vouching for each other. That vouching signal, real-world trust, is exactly what existing platforms don't capture.

**The bet:** a circle assembled from people who share interests *and* are embedded in overlapping webs of real trust will survive and thrive dramatically more often than a circle assembled from interests alone.

---

## 2. The Idea

### 2.1 In one paragraph

Every user carries a **two-sided profile** (§4.2). Any user can **create a circle** around a topic — provided they have real affinity to it. Users never "like" or rate each other; they **attest**: "I genuinely know this person." Attestations form a **Trust Graph**, and each attestation is *colored by who gave it* — credibility is a **vector over domains**, hidden from everyone. The **matching engine** combines interest fit, attribute compatibility, credibility tier, and a hidden **interpersonal-compatibility signal inferred purely from graph structure** — because the promise is not "people who share your hobby" but "people you'll be glad to be with." The product is only the **matchmaker**: circles live in the real world (WhatsApp group + physical meetups in v1).

### 2.2 The Moshe Test — the canonical example of the differentiator

> Adir loves running. Shlomo loves running. Moshe also loves running — and Adir and Shlomo can't stand Moshe.
>
> A system matching on interests alone puts all three in one circle, and the product dies on contact. If Adir and Shlomo both dislike Moshe, then — whether they'd admit it or not — something about them *as people* differs from Moshe. **The differentiator of this product is detecting that difference,** and routing Moshe to a *different* running circle where he belongs. Shared hobby is a necessary condition, never a sufficient one.

Check every design decision against the Moshe Test.

### 2.3 The Bank-Account Principle

The user's real identity in the system — the **actual-profile**, nicknamed the **"bank account"** — is *what the user actually is, as revealed by reality*: **not who they think they are, and not who they want to be.** Like a bank account, it cannot be declared, only accumulated. Its primary (currently: only) source is the trust graph — who attests to you, and who *they* are, defines what you are. Extraction mechanics = OQ-3, the deepest open question.

The declared side — **the seeking-profile** (working name: "interests") — is what the user *wants from the app*: running, swimming, singing, students at my university, students in my faculty, parties in my area. Demand-side requests, not identity claims. Declaring "runner" doesn't make you credible in running; only runners attesting to you does.

---

## 3. What This Is NOT — Boundaries & Ethics

- **Not a social network.** No feed, no likes, no content, no chat (v1 circles use WhatsApp). The product creates quality circles — nothing else. (Founder note: may evolve in the future; out of scope now.)
- **Not a people-rating system.** Nobody rates anybody's *worth*. An attestation means "I know this person," never "this person is good." **Honest nuance:** the system *does* build a hidden model of interpersonal compatibility — a personality-level classification of "who fits with whom." It is pairwise and symmetric ("these two fit"), never a ranking ("this one is better"). Moshe isn't worse than Adir; he belongs in a different circle. Keeping this distinction real — in the math, not just the marketing — is a standing design constraint.
- **No negativity, by architecture (D8).** There is no way to say anything bad about anyone: no downvotes, no negative signals, no visible rejections. The system must never provide infrastructure or legitimacy for ostracism (חרם).
- **Not a reputation score.** All trust data is invisible (D2): no user ever sees their own or anyone's credibility. No leaderboards, ever. Defends against gamification and "social credit score" dynamics.
- **Not discriminatory.** Graph communities can correlate with identity groups. Community-typed credibility may be used to find *compatibility* ("where does this person belong?"), never to *exclude by identity* ("this kind of person isn't wanted"). D8's positive-only architecture is part of the enforcement: no group has any mechanism to push anyone out.

---

## 4. Core Concepts

### 4.1 Trust Graph
A graph `G = (V, E)`: nodes are users, edges are **trust attestations**. **Per D12 (PROPOSED, awaiting founder confirmation — OQ-1): the graph is UNDIRECTED** — an edge exists only when *both* sides confirm the acquaintance. One side initiates ("I know this person"), the other confirms; unconfirmed requests **expire silently** (no rejection is ever shown — consistent with D8). Invite-key redemption (D3) **auto-creates the newcomer's first mutual edge** with their inviter, so nobody starts with a fully empty bank account.

The graph is the system's single source of truth about real-world social structure.

### 4.2 Two-Sided Profile
See §2.3: the earned **bank account** (hidden, system-derived, graph-based) vs. the declared **seeking-profile** (visible, user-chosen, demand-side).

### 4.3 Trust Attestation
A deliberate, scarce, accountable action — never a like:
- **Deliberate:** actively vouching for a real acquaintance ("I genuinely know this person").
- **Mutual (per proposed D12):** requires confirmation from both sides.
- **Scarce:** each user has a limited attestation budget (numbers = tunable parameters, D5: e.g., N at signup + periodic replenishment; revocability — default yes).
- **Accountable:** every account traces to an inviter chain (D3), so abusive branches are prunable as subtrees.

### 4.4 Credibility — a Domain-Colored Vector with a Type
Not all attestations are equal — **an attestation is colored by the attester's own profile.** Attestations from runners build your credibility *in running*; attestations from swimmers build something else, even for the same activity. Formally: each user's credibility is a **vector over domains**, each incoming attestation contributing to domains in proportion to the attester's standing in them.

Key properties:
- **Recursive propagation:** an attestation from a highly-credible runner moves your running credibility more than one from a casual runner. (This mechanism family exists in research as *topic-sensitive trust propagation* — sound and computable; exact formula = OQ-4.)
- **Credibility has a *type*, not just a magnitude:** the identity of your attesters defines *what kind* of credible you are. The same person can be highly credible within one community of attesters and much less within another. The vector's "domains" may be *communities detected in the graph itself*, not only declared interest tags (tags vs. communities vs. both = part of OQ-3).
- **Positive-only scale [0, 1]** (D8): "yes" → "less yes." More attestations = more; fewer = less; nothing pushes anyone down.
- **Hidden always** (D2); consumed only by the matching engine.
- **Primary function (D9): matching stratification** — see §4.5 layer 2 and tier homophily.

### 4.5 Matching Engine — Three Layers

| Layer | Question it answers | Status |
|---|---|---|
| **1. Interest & attribute fit** | Does the user's *seeking-profile* match the circle's topic and constraints (location, language, availability, life situation)? | Necessary condition. Table stakes — every platform does this. |
| **2. Credibility tier & domain** | Is the user genuinely embedded in this domain's real community, at a level similar to the circle's members? Circles form among people of **similar credibility magnitude AND similar domain** (D9). Comparison is **relative** — percentile within domain, never raw counts (D11). An aspiring entrepreneur with 20 attestations from fellow entrepreneurs does not get matched into the circle of someone with 200,000: same domain, different league. | The trust layer. |
| **3. Interpersonal compatibility** | Will *these specific people* be glad to be with *each other*? | **The differentiator.** Resolved in principle (D7 + D10): similarity = **in-neighborhood overlap** — the people who attest to me substantially overlap the people who attest to him — conditioned on credibility magnitude within ±ε (tunable) and same credibility *type*. No questionnaires, no behavioral tracking: graph structure only. |

Layer 1 filters, layer 2 validates, layer 3 decides. The Moshe Test lives entirely in layer 3: Moshe passes layers 1–2 for a running circle; only layer 3 routes him elsewhere.

**Corollary of D10 — the graph is the ground truth:** if the same people *genuinely* attest to Adir, Shlomo, and Moshe, at similar magnitude and type, then the three CAN share a circle. The system trusts the graph over anyone's self-image. H9 (§5) is precisely the bet that when personalities truly clash, the attester sets *will* differ.

### 4.6 Circle — User-Created, Affinity-Gated
**Circles are created by users, not only by the system.** Any user may open a circle around a topic — *provided they have demonstrated affinity to that topic* ("skin in the game"). Whether the affinity gate is a declared interest, a minimum domain credibility, or something else = OQ-7.

The system's role around circles: recommending them to fitting users, evaluating join requests through the three layers, keeping composition healthy.

v1 instantiation (D6): 5–7 people, WhatsApp group + recurring physical meetup. The app's involvement ends at introduction + light nudges; the relationship lives in the real world.

### 4.7 Definition of Success (D13)
> **A successful circle is one where everyone is glad to be with everyone.**

Shared hobby is the necessary condition; mutual personal enjoyment is the sufficient one.

**Operationalization (D13): real-world participation rate.** A circle succeeds when at least **X%** of its members actually attend its meetups/outings/trainings/sessions (X = tunable). With no chat and no feed, there are no vanity metrics — attendance is the ground truth. (Attendance-capture mechanics = OQ-5, minor, deferred to pilot design.)

---

## 5. The Central Hypothesis (H9)

Choosing graph-only compatibility (D7) plus positive-only signals (D8) makes the entire product rest on one scientific bet:

> **H9 — Personality differences between people manifest as structural differences in the trust graph.**
> If Adir and Shlomo can't stand Moshe, then *who attests to Moshe* differs measurably from *who attests to Adir and Shlomo* — even though all three run, and even though nobody ever registers a negative signal anywhere.

- If H9 is **true**, the Moshe Test is passable with zero negative input and zero questionnaires — pure structural inference.
- If H9 is **false**, layer 3 has no signal and the product collapses into ordinary interest matching.

Every algorithmic choice downstream (similarity definition, community detection, tier comparison) is in service of testing and exploiting H9. H9 is also the strongest research-track angle: it is a falsifiable social-network-science claim of independent academic interest.

---

## 6. Locked Decisions (D1–D13)

Binding until explicitly superseded. Do not relitigate; reopen only by founder's explicit request.

| # | Decision | Rationale / Notes |
|---|---|---|
| **D1** | **Matchmaker, not a social network.** v1 = profile, trust graph, matching, circle assignment. No feed, no likes, no chat, no content. Circles live in WhatsApp + physical meetups. | WhatsApp exists; a feed dilutes the differentiator; cuts ~70% of scope. Success is measured downstream (attendance), not by in-app engagement. |
| **D2** | **Full privacy of trust data.** No one ever sees any credibility score or the graph — not even their own. No leaderboards. | Prevents gaming, status anxiety, and "social credit" dynamics. |
| **D3** | **Onboarding via invite tree with one-time keys.** Existing user generates a single-use key; newcomer redeems it at signup. | One mechanism solves acquaintance verification + Sybil accountability (prunable branches). Key redemption also creates the first mutual edge (see D12). |
| **D4** | ~~PPR + global TrustRank floor~~ — **SUPERSEDED** by the v0.2 credibility redefinition (§4.4). A global anti-manipulation floor remains a *candidate defense mechanism* only. | Preserved for history; see §9.3 for the prototype findings that remain valid. |
| **D5** | **Everything numeric is a tunable parameter, never a hard-coded decision.** Attestation budgets, replenishment, decay, expiry, revocability, ε, percentile bands, X% attendance threshold. | Turns spec arguments into experiments. Any future simulation must support parameter sweeps from day one. |
| **D6** | **v1 circle = hybrid (WhatsApp + physical meetups), size 5–7.** | Small enough for cohesion, large enough to survive dropouts. Founder: "שילוב של השניים." |
| **D7** | **Compatibility signal from trust-graph structure ONLY (v1).** "People similar to me gave him credibility → he is probably similar to me." No questionnaires. Post-meetup feedback loops = explicitly deferred option, not v1. | Frictionless onboarding; revealed behavior over self-report. Current priority is conceptual clarity — architecture, algorithmics, theoretical design. |
| **D8** | **Positive-only signals, ever. Scale is [0,1] ("yes"→"less yes"), never [-1,1].** No downvotes, no anti-attestations, no visible rejections of any kind. | Ethics-by-architecture: never let users speak ill of anyone; never legitimize ostracism (חרם). Dissimilarity must be *inferred* (D7), never *declared*. |
| **D9** | **Credibility-tier homophily.** Circles form among similar credibility **magnitude** AND **domain**. | Trust-level similarity was a first principle in the original Hebrew spec (§12: "רמת אמון דומה"); this operationalizes it. |
| **D10** | **"Similar to me" = in-neighborhood overlap** (who attests to me ↔ who attests to him), conditioned on magnitude ±ε and same credibility type. **Corollary: the graph is the ground truth** over anyone's self-image. | Makes layer 3 computable and H9 falsifiable — the Moshe Test now has an exact mathematical form. |
| **D11** | **Tier comparison is RELATIVE (percentile within domain), never absolute.** Bound to the **growth invariant**: as the network grows, matching must get better for everyone — never degrade or invalidate existing standings. | "20 attestations" means different things in a 500-user vs. 5M-user network; relative semantics survive scaling. |
| **D12** 🟡 | **PROPOSED — awaiting founder confirmation (OQ-1):** the trust graph is **UNDIRECTED**; an edge exists only by **mutual confirmation**. Unconfirmed requests expire silently. Invite-key redemption auto-creates the first mutual edge. | Founder-proposed. Pros: acquaintance is inherently symmetric; kills unilateral-attachment manipulation (nobody can claim proximity to high-credibility users without consent); cleans D10 (in-neighborhood = simply neighborhood); silent expiry is D8-consistent. Cost: double friction → slower early graph growth, worsening the day-one problem (OQ-2). AI recommendation: **lock it**. |
| **D13** | **Circle success metric = real-world participation rate ≥ X%** of circle members attending the circle's meetup/outing/training (X tunable). | No chat/feed → no vanity metrics; attendance is the honest signal. |

---

## 7. Open Questions (the current frontier)

### 7.1 Awaiting a founder yes/no (recommendations already on the table)

| ID | Question | Recommendation on the table |
|---|---|---|
| **OQ-1** | **Confirm or reject D12** (undirected mutual-confirmation graph). | **Lock it.** Signal quality + manipulation resistance outweigh the friction cost. |
| **OQ-2** | **The day-one problem.** New user Dana signs up with 2 attestations; her bank account is nearly empty; the system honestly knows almost nothing about her. A young sparse network = no layer-3 signal for anyone (chicken-and-egg: people join for value, but value requires data only joiners create). | **Combine (b)+(c):** launch inside ONE dense community (e.g., a single university faculty) so the graph fills fast; AND until a user's bank account matures, match honestly on layers 1–2 only, upgrading match quality as attestations accumulate. Minimum-attestation threshold N = tunable parameter. Option (a) — refusing to match new users at all — rejected as too hostile to newcomers. |

### 7.2 The next deep-dive (the heart of the system)

| ID | Question | Candidate directions to explore |
|---|---|---|
| **OQ-3** | **How exactly is the bank account extracted from the graph?** Founder's own note: "איך נדלה את המידע הזה? נחשוב." Sub-question folded in: are the credibility-vector's *domains* declared interest tags, detected graph communities, or both? | (a) **Attester-profile aggregation:** your profile = weighted mix of your attesters' profiles (recursive — leads to propagation math). (b) **Community detection:** run clustering (e.g., Louvain/Leiden family) on the graph; your bank account = your membership vector over detected communities; credibility type = which communities attest to you. (c) **Hybrid:** detected communities define *type*; declared tags remain demand-side only (consistent with §2.3). Direction (c) currently looks most consistent with everything locked, but this is exactly the discussion to have. |
| **OQ-4** | **Draft the credibility formula** (after OQ-3). Family: topic-sensitive trust propagation over the (undirected, if D12 locks) graph, producing the domain-colored vector; must respect D8 ([0,1], positive-only), D11 (relative tiers), and the growth invariant. | Start from topic-sensitive PageRank as the skeleton; adapt to undirected mutual edges; define decay/budget hooks as D5 parameters. Validate only in simulation (§9). |

### 7.3 Smaller / parked open items

| ID | Item | Status |
|---|---|---|
| **OQ-5** | Attendance-capture mechanics for D13 (self check-in? organizer confirms?). | Minor; defer to pilot design. |
| **OQ-6** | Cross-tier mixing — are mentorship circles (deliberately mixed tiers) ever allowed as an exception to D9? | Parked, low priority. |
| **OQ-7** | The circle-creation affinity gate (§4.6): declared interest vs. minimum domain credibility vs. other. | Open; decide during matching-engine detailing. |
| **OQ-8** | Attestation economics: budget sizes, replenishment cadence, decay, expiry. | All tunable (D5); calibrate in simulation, not debate. |
| **OQ-9** | Caste-system risk of tier homophily: is upward mobility (accumulating attestations over time) a sufficient answer? | Raised, unanswered; revisit after OQ-3/OQ-4. |

### 7.4 Deferred product mechanics (post-validation; from original Hebrew spec §11)
Circle admin roles · join-request flows · leaving circles · circle quality rating · reporting/moderation · user blocking · handling abusive behavior · trust-graph privacy *architecture* (encryption, access control). Owned, noted, not blocking.

---

## 8. Secondary Hypotheses (H1–H8)

| ID | Hypothesis | How it will be tested | Status |
|---|---|---|---|
| **H1** | Circles matched with the trust layer outperform interests-only circles on the D13 metric (participation/survival). | Controlled pilot (§9, Phase 2): 50% full algorithm, 50% interests-only. | Untested — the product's make-or-break. |
| **H2** | Trust propagation limits what fake-account clusters can gain, bounded by their few real connections ("attack edges"). | Simulation: inject Sybil clusters, measure gain. | **Preliminary support** from deleted prototype (§9.3). |
| **H3** | The invite tree keeps fake-account penetration low without strangling organic growth. | Simulation growth models + pilot onboarding friction. | Untested. |
| **H4** | Honest newcomers are NOT unfairly gated out by any credibility threshold. | Simulation: false-positive rate on honest low-degree nodes. | **Preliminary warning** from prototype: naive calibration excluded 88–96% of newcomers (§9.3). Mitigated in spec by OQ-2's recommendation. |
| **H5** | A parameter set exists satisfying H2 and H4 *simultaneously* (they pull in opposite directions). | Parameter sweep → Pareto frontier → v1 config. | Untested; the core simulation deliverable. |
| **H6** | Hidden scores (D2) prevent gaming behavior. | Pilot observation + exit interviews. | Untested. |
| **H7** | Users are willing to attest at all — mutual confirmation (D12) feels natural, not awkward. | Pilot onboarding funnel: % completing ≥3 mutual attestations. | Untested; friction doubled if D12 locks. |
| **H8** | Circle-management mechanics are standard, copyable patterns — not novel risk. | Deferred to MVP; pilot circles are concierge-managed. | Assumed. |

*(H9 — the central hypothesis — is §5.)*

---

## 9. Validation Plan (three phases) & Preliminary Findings

### Phase 1 — Simulation Lab ("wind tunnel")
Before any real users: Python codebase generating synthetic social graphs (small-world, scale-free, community-structured) + loading real anonymized graphs (Stanford SNAP), implementing the credibility propagation (per OQ-4's outcome), then **attacking it on purpose** (Sybil clusters, collusion rings, edge purchase, invite abuse) and measuring two opposing numbers:
- **Attack Gain** (must be low): max credibility/eligibility an attacker achieves per unit of real cost (attack edges).
- **Newcomer Penalty** (must be low): fraction of honest new users unfairly gated.

Deliverable: the Pareto frontier of that trade-off + a recommended v1 parameter config. Dual-use by design: startup IP *and* the experimental apparatus for the research track (H9 is thesis-grade). Rebuild only after OQ-1…OQ-4 are answered.

### Phase 2 — Concierge Pilot ("the founder is the app")
One real community (~40–80 people), 8 weeks. Simple intake form (seeking-profile + mutual attestations against a member list, with consent text). Offline computation; circles of 5–7. **Randomized split: 50% of circles via full algorithm, 50% via interests+attributes only; participants blind to arms.** Founder facilitates identically for both arms. Primary metric: **D13 participation/survival, treatment vs. control** (honest bar: ≥1.5× — directional signal, not publication statistics at this sample size). Community-selection criteria: (1) existing acquaintance density (the graph needs triangles, not a star around the founder), (2) existing meetup infrastructure, (3) founder leverage. Ethics: consent, confidential attestations (nobody learns who attested to them or didn't), full debrief.

### Phase 3 — Decision Gate
- **H1 confirmed + H5 satisfied** → build MVP; product mechanics answered from pilot observations; startup track opens with pilot data as pitch seed.
- **H1 confirmed, algorithm weak** → iterate in simulation, re-pilot.
- **H1 rejected** → clean, cheap kill: remaining assets = rigorous spec, simulation codebase, attack-resistance study (publishable/thesis-grade). Research track continues; product track closes. **No outcome wastes the work.**

### 9.3 Preliminary findings (from the deleted v0.1 prototype — preserved knowledge)
A first simulation prototype (1,000-node community graph; seeded trust propagation; 50-node Sybil cluster) showed, before deletion:
1. **The attack-edge bottleneck is real:** with up to 20 attack edges, 100% of Sybil accounts stayed below the eligibility threshold; attacker gain scaled with attack edges (their real cost), NOT with the free fake-account count. Supports H2 and the whole trust-propagation approach.
2. **Naive thresholding brutally punishes newcomers:** honest new users with 2–3 attestations were excluded 88–96% of the time at default calibration. This is the H4 warning that motivated OQ-2's "honest layers-1–2 fallback" recommendation and D5's insistence on tunable, simulation-calibrated thresholds.

---

## 10. Optional Ideas & Future Directions

Explicitly *not* commitments — a parking lot so nothing is lost:

- **Post-meetup feedback loop** ("were you glad to meet X again?") as a layer-3 signal booster — deferred by D7; revisit only if graph-only inference proves insufficient.
- **Mentorship circles** — deliberate cross-tier mixing as a curated exception to D9 (OQ-6).
- **Evolution beyond pure matchmaking** — founder note: "לפחות נכון לעכשיו... אולי נשנה/נשפר את הרעיון בעתיד." Any such evolution must re-justify itself against D1.
- **Research track deliverables** — H9 as a falsifiable network-science claim; the simulation lab as thesis apparatus; the pilot as a small controlled social experiment.
- **Global integrity floor** (old D4) — a candidate anti-manipulation defense to revisit during OQ-4, informed by §9.3.

---

## 11. Recommended Order of Attack (next work session)

1. **Read this document fully** (founder + whichever AI model is assisting).
2. **Close OQ-1** — yes/no on D12 (recommendation: lock).
3. **Close OQ-2** — day-one strategy (recommendation: dense-community launch + honest layers-1–2 fallback).
4. **Deep-dive OQ-3** (bank-account extraction) using the working protocol from the "READ THIS FIRST" box: 2–3 deep questions per round, lock answers as decisions, bump version. Candidate directions are listed in §7.2 — start from direction (c).
5. **Draft the credibility formula (OQ-4)** on paper — no code yet.
6. Only after 1–5: **rebuild the simulation lab** (Phase 1, §9) to calibrate parameters and test H2/H4/H5.
7. Then: pilot design (Phase 2), community selection, and the decision gate.

---

## 12. Glossary

| Term | Meaning |
|---|---|
| **Trust attestation** | "I genuinely know this person." An edge in the trust graph. Never a like or a rating. |
| **Mutual confirmation (D12)** | An edge exists only after both sides confirm. Unconfirmed requests expire silently. |
| **Bank account** | The actual-profile: what a user *is*, accumulated from reality (the graph) — never declared. "Not who you think you are, not who you want to be." |
| **Seeking-profile ("interests")** | What a user *wants from the app* — declared, demand-side, visible. |
| **Domain-colored credibility** | Credibility as a vector over domains; each attestation contributes according to the attester's own standing. Votes from runners ≠ votes from swimmers. |
| **Credibility type** | *What kind* of credible you are — defined by which communities attest to you, not just how much. |
| **Tier homophily (D9/D11)** | Circles form among similar credibility magnitude (relative/percentile) and domain. |
| **In-neighborhood overlap (D10)** | The layer-3 similarity: the people who attest to me substantially overlap the people who attest to him. |
| **The Moshe Test** | Canonical differentiator check: shared hobby + clashing personalities must NOT land in the same circle (§2.2). |
| **H9** | The central bet: personality differences manifest as trust-graph structure differences (§5). |
| **Growth invariant (D11)** | Network growth must make matching better for everyone, never degrade existing standings. |
| **Sybil attack** | Flooding a trust system with fake identities. |
| **Collusion ring** | Real users coordinating attestations to inflate each other. |
| **Attack edge** | A connection between the fake/colluding region and the honest region; defenses work because these are scarce and costly. |
| **Invite tree (D3)** | Every account traces to the member who issued its one-time key; fake branches prune as subtrees. |
| **Silent expiry** | Unconfirmed attestation requests disappear without any visible rejection (D8-consistent). |
| **PageRank / Personalized PageRank / TrustRank / topic-sensitive propagation** | The algorithm family for propagating importance/trust through a graph — from everywhere / from one user's viewpoint / from verified seeds / per-topic. OQ-4 draws from this family. |
| **Concierge MVP** | Testing the hypothesis by performing the service manually before building software (Phase 2). |
| **Pareto frontier** | The trade-off curve where blocking attackers harder necessarily excludes more honest newcomers (H5). |

---

## 13. Reading List

- Kamvar, Schlosser, Garcia-Molina — *The EigenTrust Algorithm for Reputation Management in P2P Networks* (WWW 2003)
- Haveliwala — *Topic-Sensitive PageRank* (WWW 2002) ← closest ancestor of the domain-colored credibility idea
- Gyöngyi, Garcia-Molina, Pedersen — *Combating Web Spam with TrustRank* (VLDB 2004)
- Cao, Sirivianos, Yang, Pregueiro — *SybilRank* (NSDI 2012)
- Yu, Kaminsky, Gibbons, Flaxman — *SybilGuard* (SIGCOMM 2006)
- Douceur — *The Sybil Attack* (IPTPS 2002)
- Fortunato — *Community detection in graphs* (Physics Reports 2010) ← background for OQ-3 direction (b)/(c)
- Stanford SNAP dataset collection — https://snap.stanford.edu/data/
- "Web of trust" (PGP concept) — the historical namesake; worth a skim for inspiration.

---

## 14. Changelog

**Spec v0.6 — 2026-07-07 (consolidation).** Single-source-of-truth rewrite. Repo reduced to this README only (prototype code and auxiliary docs deliberately deleted; findings preserved in §9.3; original Hebrew spec fully absorbed into this document). Added: READ-THIS-FIRST protocol box, unified OQ numbering, recommended order of attack, expanded glossary, full decision table D1–D13.

**Spec v0.5 — 2026-07-07.** D12 drafted (PROPOSED): undirected mutual-confirmation graph (founder-initiated); D13 locked: success = participation rate ≥ X% at real-world meetups; reaffirmed not-a-social-network.

**Spec v0.4 — 2026-07-06.** D10 locked: similarity = in-neighborhood overlap ± ε, same type; corollary "the graph is the ground truth." Bank-account principle articulated. D11 locked: relative tiers + growth invariant.

**Spec v0.3 — 2026-07-06.** D7 locked: graph-only compatibility (no questionnaires, feedback deferred). D8 locked: positive-only [0,1], zero negativity, anti-ostracism ethics. Credibility gains a *type* (attester communities). D9 locked: tier homophily. H9 named as the central hypothesis.

**Spec v0.2 — 2026-07-06.** Circles are user-created and affinity-gated. Two-sided profile introduced. Credibility redefined as a domain-colored vector (D4 superseded). The Moshe Test added; matching restructured into three layers. Success defined qualitatively. Development frozen — spec refinement only.

**Spec v0.1 — 2026-07-06.** Initial README from the original Hebrew spec: problem, concepts, first decisions, hypotheses, three-phase validation plan, simulation-lab scaffold (later deleted in v0.6).

---

*The trust layer is an internal engine serving one goal — circles people genuinely want to stay in — never an end in itself.*
