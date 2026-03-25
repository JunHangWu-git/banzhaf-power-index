"""
quota_analysis.py

Analyze how Banzhaf power changes as the quota varies for a fixed set of weights.

This script imports banzhaf.py and produces:
- a quota-by-quota table
- optional CSV export

Good use in the project:
- show that voting weight != voting power
- show that changing quota can change actual influence
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Sequence

from banzhaf import WeightedVotingGame, normalized_banzhaf, raw_banzhaf_counts, weight_shares


def quota_range_for_weights(weights: Sequence[int]) -> range:
    """
    Sensible quota range for weighted voting games:
        1, 2, ..., sum(weights)

    In many examples, quota > sum(weights) is trivial (nothing can win),
    so we stop at sum(weights).
    """
    total = sum(weights)
    return range(1, total + 1)


def quota_analysis(weights: Sequence[int]) -> List[dict]:
    """
    Compute Banzhaf results for every quota from 1 to sum(weights).
    """
    rows: List[dict] = []
    shares = weight_shares(WeightedVotingGame(quota=1, weights=tuple(weights)))

    for q in quota_range_for_weights(weights):
        game = WeightedVotingGame(quota=q, weights=tuple(weights))
        raw = raw_banzhaf_counts(game)
        norm = normalized_banzhaf(game)

        row = {
            "quota": q,
            "weights": list(weights),
            "weight_shares": shares,
            "raw_banzhaf": raw,
            "normalized_banzhaf": norm,
        }
        rows.append(row)

    return rows


def print_quota_table(weights: Sequence[int], decimals: int = 4) -> None:
    """
    Print a readable quota-by-quota summary.
    """
    rows = quota_analysis(weights)
    n = len(weights)

    print(f"Weights: {list(weights)}")
    print("Weight shares:")
    for i, share in enumerate(rows[0]["weight_shares"], start=1):
        print(f"  Player {i}: {share:.{decimals}f}")
    print()

    header_parts = ["Quota"]
    for i in range(1, n + 1):
        header_parts.append(f"B{i}")
    print(" | ".join(f"{h:>8}" for h in header_parts))
    print("-" * (11 * (n + 1)))

    for row in rows:
        parts = [f"{row['quota']:>8}"]
        for value in row["normalized_banzhaf"]:
            parts.append(f"{value:>8.{decimals}f}")
        print(" | ".join(parts))


def export_quota_csv(weights: Sequence[int], output_path: str | Path) -> Path:
    """
    Export quota analysis to CSV for plotting or report tables.

    Columns:
    quota, p1_weight_share, ..., pN_weight_share, p1_raw, ..., pN_raw,
    p1_banzhaf, ..., pN_banzhaf
    """
    rows = quota_analysis(weights)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    n = len(weights)
    fieldnames = ["quota"]
    fieldnames += [f"p{i}_weight_share" for i in range(1, n + 1)]
    fieldnames += [f"p{i}_raw" for i in range(1, n + 1)]
    fieldnames += [f"p{i}_banzhaf" for i in range(1, n + 1)]

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            out = {"quota": row["quota"]}
            for i, value in enumerate(row["weight_shares"], start=1):
                out[f"p{i}_weight_share"] = value
            for i, value in enumerate(row["raw_banzhaf"], start=1):
                out[f"p{i}_raw"] = value
            for i, value in enumerate(row["normalized_banzhaf"], start=1):
                out[f"p{i}_banzhaf"] = value
            writer.writerow(out)

    return output_path


def main() -> None:
    # Example: analyze quota sensitivity for a fixed voting system.
    weights = (4, 3, 2, 1)

    print_quota_table(weights, decimals=4)

    csv_path = export_quota_csv(weights, "outputs/quota_analysis_4_3_2_1.csv")
    print(f"\nSaved CSV to: {csv_path}")


if __name__ == "__main__":
    main()