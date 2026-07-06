"""Personalized PageRank (Decision D4, signal #2).

PPR rooted at user u = trust "from u's point of view": mutual friends and
short trust paths score high. This is the graph-proximity FEATURE used by
the matching engine — it answers "how socially close is v to u?",
which a single global score cannot.
"""

import networkx as nx

from simlab.config import TrustConfig, DEFAULT


def ppr(g: nx.DiGraph, root, cfg: TrustConfig = DEFAULT) -> dict:
    """Trust vector from `root`'s perspective."""
    return nx.pagerank(g, alpha=cfg.damping, personalization={root: 1.0})


def proximity(g: nx.DiGraph, u, v, cfg: TrustConfig = DEFAULT) -> float:
    """Symmetric pairwise proximity: mean of PPR(u→v) and PPR(v→u).

    NOTE: O(V+E) per node — fine for pilot scale (<10^4 nodes).
    For larger graphs switch to push-based approximate PPR (future work).
    """
    return 0.5 * (ppr(g, u, cfg)[v] + ppr(g, v, cfg)[u])


def proximity_matrix(g: nx.DiGraph, nodes: list, cfg: TrustConfig = DEFAULT):
    """Pairwise proximity among a candidate pool (for circle assembly)."""
    vectors = {u: ppr(g, u, cfg) for u in nodes}
    return {
        (u, v): 0.5 * (vectors[u][v] + vectors[v][u])
        for i, u in enumerate(nodes)
        for v in nodes[i + 1 :]
    }
