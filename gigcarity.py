"""
Gigcarity: computational implementation for labor economics analysis.

Gigcarity refers to the precarious economic conditions experienced by gig economy workers, characterized by income volatility, lack of employment benefits and protections, algorithmic management systems that shift risk to workers, and the absence of collective bargaining power typical of traditional employment relationships. This module provides a reproducible calculator that validates the canonical channels, normalizes each series, computes a weighted index, and supports simple counterfactual policy simulation. The design is intentionally transparent so researchers can inspect how the concept moves from definition to code. Typical uses include comparative diagnostics, notebook-based scenario testing, and integration into empirical pipelines where consistent measurement matters as much as prediction.
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

# Gigcarity channels track the observable anatomy of the canonical definition.
TERM_CHANNELS = [
    "income_volatility",  # Income volatility captures a distinct economic channel.
    "benefit_gap",  # Benefit gap captures a distinct economic channel.
    "schedule_instability",  # Schedule instability captures a distinct economic channel.
    "algorithmic_control",  # Algorithmic control captures a distinct economic channel.
    "earnings_uncertainty",  # Earnings uncertainty captures a distinct economic channel.
    "collective_voice_deficit",  # Collective voice deficit captures a distinct economic channel.
    "safety_net_access",  # Safety net access mitigates exposure when it is high.
]

# Weighted channels preserve the repository's existing score logic.
WEIGHTED_CHANNELS = [
    "income_volatility",
    "benefit_gap",
    "schedule_instability",
    "algorithmic_control",
    "earnings_uncertainty",
    "collective_voice_deficit",
    "safety_net_access",
]

# Default weights encode the relative economic importance of each weighted channel.
DEFAULT_WEIGHTS: dict[str, float] = {
    "income_volatility": 0.2,  # Income volatility captures a distinct economic channel.
    "benefit_gap": 0.16,  # Benefit gap captures a distinct economic channel.
    "schedule_instability": 0.14,  # Schedule instability captures a distinct economic channel.
    "algorithmic_control": 0.16,  # Algorithmic control captures a distinct economic channel.
    "earnings_uncertainty": 0.12,  # Earnings uncertainty captures a distinct economic channel.
    "collective_voice_deficit": 0.12,  # Collective voice deficit captures a distinct economic channel.
    "safety_net_access": 0.1,  # Safety net access mitigates exposure when it is high.
}


class GigcarityCalculator:
    """
    Compute Gigcarity index scores from tabular data.

    Parameters
    ----------
    weights : dict[str, float] | None
        Optional weights overriding DEFAULT_WEIGHTS. Keys must match
        WEIGHTED_CHANNELS and values must sum to 1.0.
    """

    def __init__(self, weights: Optional[dict[str, float]] = None) -> None:
        # Alternative weights are useful for robustness checks across specifications.
        self.weights = weights or DEFAULT_WEIGHTS.copy()

        # Exact key matching prevents silent omission of economically relevant channels.
        if set(self.weights) != set(WEIGHTED_CHANNELS):
            raise ValueError(f"Weights must include exactly these channels: {WEIGHTED_CHANNELS}")

        # Unit-sum weights keep the index interpretable across datasets.
        if abs(sum(self.weights.values()) - 1.0) >= 1e-6:
            raise ValueError("Weights must sum to 1.0")

    @staticmethod
    def _normalise(series: pd.Series) -> pd.Series:
        """
        Return min-max normalized values on the unit interval.
        """
        lo = float(series.min())
        hi = float(series.max())
        if hi == lo:
            # Degenerate channels should not create spurious variation.
            return pd.Series(np.zeros(len(series)), index=series.index)
        return (series - lo) / (hi - lo)

    def calculate_gigcarity(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute normalized channels, composite scores, and qualitative bands.
        """
        # Full channel validation keeps the score tied to the canonical definition.
        missing = [channel for channel in TERM_CHANNELS if channel not in df.columns]
        if missing:
            raise ValueError(f"Missing Gigcarity channels: {missing}")

        out = df.copy()
        for channel in TERM_CHANNELS:
            out[f"{channel}_norm"] = self._normalise(out[channel])

        # Positive channels intensify the mechanism while negative channels offset it.
        out["gigcarity_index"] = (
            + self.weights["income_volatility"] * out["income_volatility_norm"]
            + self.weights["benefit_gap"] * out["benefit_gap_norm"]
            + self.weights["schedule_instability"] * out["schedule_instability_norm"]
            + self.weights["algorithmic_control"] * out["algorithmic_control_norm"]
            + self.weights["earnings_uncertainty"] * out["earnings_uncertainty_norm"]
            + self.weights["collective_voice_deficit"] * out["collective_voice_deficit_norm"]
            + self.weights["safety_net_access"] * (1.0 - out["safety_net_access_norm"])
        )

        # Three bands keep the metric usable in audits, papers, and dashboards.
        out["gigcarity_band"] = pd.cut(
            out["gigcarity_index"],
            bins=[-np.inf, 0.33, 0.66, np.inf],
            labels=["low", "moderate", "high"],
        )
        return out

    def simulate_policy(self, df: pd.DataFrame, channel: str, reduction: float = 0.2) -> pd.DataFrame:
        """
        Simulate a policy shock that reduces one observed channel.
        """
        if channel not in TERM_CHANNELS:
            raise ValueError(f"Unknown Gigcarity channel: {channel}")
        if reduction < 0.0 or reduction > 1.0:
            raise ValueError("reduction must be between 0.0 and 1.0")

        # Counterfactual shocks translate reforms into score movements.
        df_policy = df.copy()
        df_policy[channel] = df_policy[channel] * (1 - reduction)
        return self.calculate_gigcarity(df_policy)


if __name__ == "__main__":
    sample = pd.read_csv("gigcarity_dataset.csv")
    calc = GigcarityCalculator()
    print(calc.calculate_gigcarity(sample)[["gigcarity_index", "gigcarity_band"]].head(10).to_string(index=False))

    scenario = calc.simulate_policy(sample, channel="income_volatility", reduction=0.15)
    print("\nPolicy Scenario Mean Index:")
    print(float(scenario["gigcarity_index"].mean()))
