"""Attack #1 — Sybil cluster (spec §10: 'פתיחת משתמשים מזויפים').

An attacker creates n_sybils fake accounts that densely attest to each
other, and manages to obtain `n_attack_edges` attestations from tricked
honest users. The attack-edge budget is the attacker's real-world cost —
the defense's whole job is to make credibility gain scale with attack
edges, NOT with the (free) number of fake accounts.
"""

import networkx as nx
import numpy as np


def add_sybil_cluster(
    g: nx.DiGraph,
    n_sybils: int = 50,
    n_attack_edges: int = 5,
    internal_density: float = 0.5,
    seed: int = 0,
) -> list:
    """Mutates g in place; returns the list of sybil node ids."""
    rng = np.random.default_rng(seed)
    honest = [v for v, d in g.nodes(data=True) if d.get("kind") == "honest"]

    base = max(g.nodes) + 1 if all(isinstance(v, int) for v in g.nodes) else len(g)
    sybils = list(range(base, base + n_sybils))
    g.add_nodes_from(sybils, kind="sybil")

    # dense internal mutual attestations (free for the attacker)
    for i, u in enumerate(sybils):
        for v in sybils[i + 1 :]:
            if rng.random() < internal_density:
                g.add_edge(u, v)
                g.add_edge(v, u)

    # attack edges: honest -> sybil attestations obtained by deception
    victims = rng.choice(honest, size=min(n_attack_edges, len(honest)), replace=False)
    targets = rng.choice(sybils, size=len(victims), replace=True)
    for victim, target in zip(victims, targets):
        g.add_edge(victim, target)
        g.add_edge(target, victim)  # sybil happily attests back

    return sybils
