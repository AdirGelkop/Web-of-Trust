# Decision Log

Locked decisions for Trust Circles. Each entry is an ADR (Architecture Decision Record).
A decision here is **binding until explicitly superseded** by a new entry — no relitigating in threads.
Everything not written here is a hypothesis (see README §6).

---

## D1 — The product is a matchmaker, not a social network
**Date:** 2026-07-06 · **Status:** Accepted

**Decision:** v1 builds only: profile, trust graph, matching engine, circle assignment. No feed, no likes, no in-app chat, no content. Circles live in WhatsApp + physical meetups.

**Rationale:** WhatsApp already exists; a feed dilutes the differentiator. Cuts ~70% of build scope.

**Consequences:** The app's success metric is downstream (circle survival), not in-app engagement. We must design lightweight measurement (check-in nudges) instead of relying on in-app analytics.

---

## D2 — Full privacy of trust data
**Date:** 2026-07-06 · **Status:** Accepted

**Decision:** Credibility scores and the trust graph are never displayed to anyone — not one's own score, not others'. No leaderboards, no badges derived from trust.

**Rationale:** Visible scores invite gaming, status anxiety, and "social credit score" comparisons. Hidden scores keep users optimizing for real relationships.

**Consequences:** All trust math runs server-side, behind the matching engine. Product copy must explain matching quality without exposing the mechanism. H6 tests whether gaming still emerges.

---

## D3 — Onboarding via invite tree with one-time keys
**Date:** 2026-07-06 · **Status:** Accepted

**Decision:** An existing user generates a single-use key; a newcomer redeems it at signup. Every account is rooted in an inviter chain. Trust attestations are enabled only after key redemption.

**Rationale:** One mechanism solves two spec problems at once: acquaintance verification (§5 of the original spec) and Sybil resistance (§10) — fake branches have an accountable root and can be pruned as subtrees.

**Consequences:** Growth is gated by key budgets (tunable, see D5). H3 tests the growth/security trade-off.

---

## D4 — Trust model: Personalized PageRank for matching + TrustRank-style floor for filtering
**Date:** 2026-07-06 · **Status:** Accepted

**Decision:** Two distinct signals:
1. **Global credibility floor** — trust propagated from verified anchor seeds (TrustRank). Used *only* as an eligibility gate against fake/manipulated accounts.
2. **Personalized trust vectors** — PPR rooted at each user. Used as the *graph-proximity feature* in matching.

**Rationale:** A global scalar answers "is this account real?"; it cannot answer "will these seven people click?" Graph proximity (mutual friends, short trust paths) is the matching signal. Trust propagation from seeds is inherently Sybil-limiting via the attack-edge bottleneck.

**Consequences:** Resolves the spec's scalar-vs-vector ambiguity (§2.2 vs §6). The exact floor threshold and PPR parameters are Phase-1 outputs (H5).

---

## D5 — Everything numeric is a tunable parameter
**Date:** 2026-07-06 · **Status:** Accepted

**Decision:** Attestation budget, replenishment rate, decay, expiry, revocability, floor threshold, damping factors — all live in a single config, calibrated by simulation, never hard-coded or decided by debate.

**Rationale:** Converts the spec's open questions (§11) from arguments into experiments.

**Consequences:** `simlab` must support parameter sweeps from day one (see `simlab/config.py`).

---

## D6 — v1 circle = hybrid, size 5–7
**Date:** 2026-07-06 · **Status:** Accepted

**Decision:** A circle is 5–7 matched people instantiated as a WhatsApp group + recurring physical meetup.

**Rationale:** Small enough for cohesion, large enough to survive dropouts; hybrid matches user answer "שילוב של השניים".

**Consequences:** Matching engine includes circle-size constraints and a "no isolated member" balance rule.

---

## Template for future decisions

```
## Dx — Title
**Date:** · **Status:** Proposed / Accepted / Superseded by Dy

**Decision:**
**Rationale:**
**Consequences:**
```
