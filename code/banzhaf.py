"""
banzhaf.py

Core utilities for weighted voting games and the Banzhaf Power Index.

Model:
    [q : w1, w2, ..., wn]

Definitions:
- A coalition is any subset of players.
- A coalition is winning if its total weight >= quota q.
- A player is critical in a winning coalition if removing that player
  makes the coalition losing.
- The raw Banzhaf count eta_i is the number of winning coalitions in
  which player i is critical.
- The normalized Banzhaf index beta_i is:
      beta_i = eta_i / sum_j eta_j
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, List, Sequence, Tuple


@dataclass(frozen=True)
class WeightedVotingGame:
    quota: int
    weights: Tuple[int, ...]

    def __post_init__(self) -> None:
        if self.quota <= 0:
            raise ValueError("quota must be positive")
        if len(self.weights) == 0:
            raise ValueError("weights must be non-empty")
        if any(w < 0 for w in self.weights):
            raise ValueError("weights must be non-negative")

    @property
    def n(self) -> int:
        return len(self.weights)

    @property
    def players(self) -> Tuple[int, ...]:
        """1-based player labels for math/report readability."""
        return tuple(range(1, self.n + 1))


def coalition_weight(game: WeightedVotingGame, coalition: Sequence[int]) -> int:
    """
    Return total weight of a coalition.

    coalition uses 1-based player labels, e.g. (1, 3, 4).
    """
    return sum(game.weights[player - 1] for player in coalition)


def all_coalitions(players: Sequence[int]) -> Iterable[Tuple[int, ...]]:
    """Yield all coalitions (including empty and grand coalition)."""
    for r in range(len(players) + 1):
        yield from combinations(players, r)


def is_winning(game: WeightedVotingGame, coalition: Sequence[int]) -> bool:
    """Check whether a coalition is winning."""
    return coalition_weight(game, coalition) >= game.quota


def critical_players(game: WeightedVotingGame, coalition: Sequence[int]) -> List[int]:
    """
    Return the players who are critical in the given coalition.

    A player is critical iff the coalition is winning and removing that player
    makes it losing.
    """
    if not is_winning(game, coalition):
        return []

    total = coalition_weight(game, coalition)
    critical: List[int] = []
    for player in coalition:
        player_weight = game.weights[player - 1]
        if total - player_weight < game.quota:
            critical.append(player)
    return critical


def raw_banzhaf_counts(game: WeightedVotingGame) -> List[int]:
    """
    Compute the raw Banzhaf counts eta_i for each player.
    """
    counts = [0] * game.n
    for coalition in all_coalitions(game.players):
        for player in critical_players(game, coalition):
            counts[player - 1] += 1
    return counts


def normalized_banzhaf(game: WeightedVotingGame) -> List[float]:
    """
    Compute normalized Banzhaf indices beta_i.

    If the total raw count is 0, return all zeros.
    """
    counts = raw_banzhaf_counts(game)
    total = sum(counts)
    if total == 0:
        return [0.0] * game.n
    return [count / total for count in counts]


def weight_shares(game: WeightedVotingGame) -> List[float]:
    """
    Compute each player's share of total assigned weight.
    """
    total_weight = sum(game.weights)
    if total_weight == 0:
        return [0.0] * game.n
    return [w / total_weight for w in game.weights]


def coalition_table(game: WeightedVotingGame) -> List[dict]:
    """
    Build a full coalition table useful for debugging, exporting, or reports.

    Each row contains:
    - coalition
    - weight
    - winning
    - critical_players
    """
    rows = []
    for coalition in all_coalitions(game.players):
        rows.append(
            {
                "coalition": coalition,
                "weight": coalition_weight(game, coalition),
                "winning": is_winning(game, coalition),
                "critical_players": critical_players(game, coalition),
            }
        )
    return rows


def summary(game: WeightedVotingGame) -> dict:
    """
    Return a compact summary of the weighted voting game.
    """
    raw = raw_banzhaf_counts(game)
    norm = normalized_banzhaf(game)
    shares = weight_shares(game)

    return {
        "quota": game.quota,
        "weights": list(game.weights),
        "players": list(game.players),
        "weight_shares": shares,
        "raw_banzhaf": raw,
        "normalized_banzhaf": norm,
    }


def format_summary(game: WeightedVotingGame, decimals: int = 4) -> str:
    """
    Pretty-print a report-friendly summary.
    """
    info = summary(game)

    lines = []
    lines.append(f"Game: [{info['quota']} : {', '.join(map(str, info['weights']))}]")
    lines.append("")
    lines.append("Player | Weight | Weight Share | Raw Banzhaf | Normalized Banzhaf")
    lines.append("-" * 68)

    for i, player in enumerate(info["players"]):
        lines.append(
            f"{player:>6} | "
            f"{info['weights'][i]:>6} | "
            f"{info['weight_shares'][i]:>{12 + decimals}.{decimals}f} | "
            f"{info['raw_banzhaf'][i]:>11} | "
            f"{info['normalized_banzhaf'][i]:>{18 + decimals}.{decimals}f}"
        )

    return "\n".join(lines)


def main() -> None:
    # Example from a typical weighted voting game.
    game = WeightedVotingGame(quota=6, weights=(4, 3, 2, 1))

    print(format_summary(game))
    print("\nWinning coalitions with critical players:\n")

    for row in coalition_table(game):
        if row["winning"]:
            print(
                f"{row['coalition']}: "
                f"weight={row['weight']}, "
                f"critical={row['critical_players']}"
            )


if __name__ == "__main__":
    main()
