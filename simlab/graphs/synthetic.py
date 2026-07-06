"""Synthetic social-graph generators.

All generators return a *directed* graph, because a trust attestation
("I know this person") is directional. Undirected base topologies are
converted with reciprocal edges — in real life most acquaintance is mutual,
and attacks/newcomers later add asymmetric edges on top.

Node attribute convention:
    kind: "honest" (default) | "sybil" | "newcomer"
"""

import networkx as nx


def _finalize(g_undirected: nx.Graph) -> nx.DiGraph:
    g = g_undirected.to_directed()
    nx.set_node_attributes(g, "honest", name="kind")
    return g


def watts_strogatz(n: int = 1000, k: int = 8, p: float = 0.1, seed: int = 42) -> nx.DiGraph:
    """Small-world graph: high clustering + short paths (friend-group-like)."""
    return _finalize(nx.watts_strogatz_graph(n, k, p, seed=seed))


def barabasi_albert(n: int = 1000, m: int = 4, seed: int = 42) -> nx.DiGraph:
    """Scale-free graph: few hubs, many low-degree nodes (online-community-like)."""
    return _finalize(nx.barabasi_albert_graph(n, m, seed=seed))


def community_graph(
    n_communities: int = 10,
    community_size: int = 100,
    p_in: float = 0.15,
    p_out: float = 0.002,
    seed: int = 42,
) -> nx.DiGraph:
    """Planted-partition graph: dense communities, sparse bridges.

    Closest to the product's reality — real social circles are exactly
    dense clusters with a few cross-links.
    """
    sizes = [community_size] * n_communities
    g = nx.planted_partition_graph(n_communities, community_size, p_in, p_out, seed=seed)
    # keep community id for later matching experiments
    for node, data in g.nodes(data=True):
        data["community"] = data.pop("block", None)
    dg = _finalize(g)
    return dg
