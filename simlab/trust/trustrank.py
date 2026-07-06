"""TrustRank-style global credibility (Decision D4, signal #1).

Trust is propagated from a small set of verified anchor ("seed") nodes.
Because trust can only reach a Sybil region through its few attack edges,
the total credibility a fake cluster can absorb is bottlenecked — this is
the core anti-Sybil property being validated in Phase 1.

Output is used ONLY as an eligibility floor, never as a ranking (D2/D4).
"""

import networkx as nx
import numpy as np

from simlab.config import TrustConfig, DEFAULT


def pick_seeds(g: nx.DiGraph, cfg: TrustConfig = DEFAULT) -> list:
    """Choose anchor nodes among honest users.

    In production these are manually verified accounts; in simulation we
    proxy them by degree (community organizers) or at random.
    """
    honest = [v for v, d in g.nodes(data=True) if d.get("kind") == "honest"]
    if cfg.seed_strategy == "degree":
        honest.sort(key=lambda v: g.degree(v), reverse=True)
        return honest[: cfg.n_seeds]
    rng = np.random.default_rng(0)
    return list(rng.choice(honest, size=min(cfg.n_seeds, len(honest)), replace=False))


def trustrank(g: nx.DiGraph, seeds: list, cfg: TrustConfig = DEFAULT) -> dict:
    """Seeded PageRank: random walks restart only at anchor nodes."""
    personalization = {s: 1.0 for s in seeds}
    return nx.pagerank(g, alpha=cfg.damping, personalization=personalization)


def credibility_floor(scores: dict, g: nx.DiGraph, cfg: TrustConfig = DEFAULT) -> float:
    """Floor = percentile of HONEST nodes' scores (scale-free threshold)."""
    honest_scores = [
        s for v, s in scores.items() if g.nodes[v].get("kind") == "honest"
    ]
    return float(np.percentile(honest_scores, cfg.floor_percentile))


def eligible(scores: dict, floor: float) -> set:
    """Nodes admitted into the matching pool."""
    return {v for v, s in scores.items() if s >= floor}
