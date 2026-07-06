"""The two numbers that matter (README §7.4).

ATTACK GAIN  (must be low): how far do fake accounts get?
NEWCOMER PENALTY (must be low): how many honest new users are unfairly gated?

They pull in opposite directions; Phase 1's product is their Pareto frontier.
"""

import networkx as nx
import numpy as np

from simlab.config import TrustConfig, DEFAULT
from simlab.trust.trustrank import trustrank, credibility_floor


def attack_gain(scores: dict, g: nx.DiGraph, floor: float, attacker_kind: str = "sybil") -> dict:
    """How well did the attackers do against the eligibility gate?"""
    attackers = [v for v, d in g.nodes(data=True) if d.get("kind") == attacker_kind]
    honest = [v for v, d in g.nodes(data=True) if d.get("kind") == "honest"]
    a_scores = np.array([scores[v] for v in attackers])
    h_median = float(np.median([scores[v] for v in honest]))
    return {
        "n_attackers": len(attackers),
        "pct_above_floor": float((a_scores >= floor).mean()) * 100,
        "attacker_median_vs_honest_median": float(np.median(a_scores)) / h_median if h_median else 0.0,
    }


def newcomer_penalty(
    g: nx.DiGraph,
    n_newcomers: int = 50,
    edges_per_newcomer: int = 2,
    cfg: TrustConfig = DEFAULT,
    seed: int = 1,
) -> dict:
    """Add honest low-degree newcomers, recompute, measure unfair exclusion.

    Works on a copy — does not mutate g.
    """
    rng = np.random.default_rng(seed)
    g2 = g.copy()
    honest = [v for v, d in g2.nodes(data=True) if d.get("kind") == "honest"]

    base = max(v for v in g2.nodes if isinstance(v, int)) + 1
    newcomers = list(range(base, base + n_newcomers))
    g2.add_nodes_from(newcomers, kind="newcomer")
    for nc in newcomers:
        friends = rng.choice(honest, size=edges_per_newcomer, replace=False)
        for f in friends:
            g2.add_edge(nc, f)
            g2.add_edge(f, nc)

    from simlab.trust.trustrank import pick_seeds  # local import to avoid cycle
    seeds = pick_seeds(g2, cfg)
    scores = trustrank(g2, seeds, cfg)
    floor = credibility_floor(scores, g2, cfg)
    nc_scores = np.array([scores[v] for v in newcomers])
    return {
        "n_newcomers": n_newcomers,
        "edges_per_newcomer": edges_per_newcomer,
        "pct_unfairly_excluded": float((nc_scores < floor).mean()) * 100,
    }
