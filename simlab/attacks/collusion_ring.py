"""Attack #2 — Collusion ring (spec §10: 'קבוצת חברים שמצביעה רק אחד לשני').

REAL users coordinate to attest maximally to each other, hoping to inflate
their standing. Harder than Sybil: the participants are legitimate nodes
with genuine outside connections. The relevant question is not "are they
excluded" (they shouldn't be — they're real) but "how much EXTRA
credibility does the ring buy them over their organic baseline".
"""

import networkx as nx
import numpy as np


def add_collusion_ring(g: nx.DiGraph, ring_size: int = 10, seed: int = 0) -> list:
    """Pick real honest nodes and fully interconnect them. Returns ring ids."""
    rng = np.random.default_rng(seed)
    honest = [v for v, d in g.nodes(data=True) if d.get("kind") == "honest"]
    ring = list(rng.choice(honest, size=ring_size, replace=False))
    for i, u in enumerate(ring):
        for v in ring[i + 1 :]:
            g.add_edge(u, v)
            g.add_edge(v, u)
    for v in ring:
        g.nodes[v]["kind"] = "colluder"
    return ring
