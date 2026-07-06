"""Central tunable configuration (Decision D5).

Every number that the original spec left open lives here, so experiments
can sweep it. Nothing in the algorithms is hard-coded.
"""

from dataclasses import dataclass


@dataclass
class TrustConfig:
    # --- Trust propagation ---
    damping: float = 0.85          # PageRank damping factor (alpha)
    n_seeds: int = 20              # verified anchor nodes for TrustRank
    seed_strategy: str = "degree"  # "degree" | "random" (how anchors are picked in sims)

    # --- Credibility floor (eligibility gate) ---
    # The floor is set as a percentile of *honest* node scores in simulation,
    # so it is scale-free across graph sizes.
    floor_percentile: float = 5.0

    # --- Attestation economics (spec §4 open questions) ---
    signup_attestations: int = 5      # votes granted at signup
    monthly_attestations: int = 2     # replenishment per period
    attestation_revocable: bool = True

    # --- Decay (spec §6 open questions) ---
    decay_enabled: bool = True
    decay_half_life_days: float = 365.0   # trust edge weight half-life
    inactivity_grace_days: float = 90.0   # no decay before this


DEFAULT = TrustConfig()
