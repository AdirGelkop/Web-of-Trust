"""End-to-end demo — the first real experiment (toward H2 + H4).

Pipeline:
  1. Generate a community-structured social graph (1,000 honest users).
  2. Compute TrustRank from anchor seeds; set the credibility floor.
  3. Inject a 50-node Sybil cluster with a varying attack-edge budget.
  4. Report: Attack Gain vs. Newcomer Penalty.

Run from repo root:  python -m simlab.experiments.run_demo
"""

from simlab.config import DEFAULT as CFG
from simlab.graphs.synthetic import community_graph
from simlab.trust.trustrank import pick_seeds, trustrank, credibility_floor
from simlab.attacks.sybil_cluster import add_sybil_cluster
from simlab.metrics.core import attack_gain, newcomer_penalty


def main():
    print("=" * 72)
    print("Trust Circles — Simulation Lab · Demo experiment (H2/H4 preview)")
    print("=" * 72)

    # --- Baseline: honest world -------------------------------------------
    base = community_graph(n_communities=10, community_size=100)
    print(f"\nBase graph: {base.number_of_nodes()} honest users, "
          f"{base.number_of_edges()} attestation edges (10 communities)")

    # --- Newcomer fairness on the honest graph (H4) -----------------------
    print("\n[H4] Newcomer penalty (honest users joining with few edges):")
    for k in (1, 2, 3):
        r = newcomer_penalty(base, n_newcomers=50, edges_per_newcomer=k, cfg=CFG)
        print(f"  {k} attestation(s) at signup -> "
              f"{r['pct_unfairly_excluded']:5.1f}% unfairly excluded by the floor")

    # --- Sybil attack sweep (H2) ------------------------------------------
    print("\n[H2] Sybil cluster: 50 fake accounts, varying attack-edge budget:")
    print(f"  {'attack edges':>12} | {'% sybils above floor':>20} | "
          f"{'sybil median / honest median':>28}")
    for budget in (1, 5, 20, 50):
        g = base.copy()
        add_sybil_cluster(g, n_sybils=50, n_attack_edges=budget, seed=7)
        seeds = pick_seeds(g, CFG)
        scores = trustrank(g, seeds, CFG)
        floor = credibility_floor(scores, g, CFG)
        r = attack_gain(scores, g, floor)
        print(f"  {budget:>12} | {r['pct_above_floor']:>19.1f}% | "
              f"{r['attacker_median_vs_honest_median']:>28.3f}")

    print("\nReading the results:")
    print("  * Attacker gain should scale with attack edges (their real cost),")
    print("    NOT with the free 50 fake accounts. If % above floor stays low")
    print("    at small budgets, the bottleneck property holds.")
    print("  * Newcomer exclusion should drop fast with 2-3 attestations —")
    print("    that is the invite-tree onboarding working as intended.")
    print("  * Next: exp_h5 parameter sweep -> Pareto frontier -> v1 config.")


if __name__ == "__main__":
    main()
