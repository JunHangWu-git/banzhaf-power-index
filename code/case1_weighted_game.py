import csv
import itertools
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / "code" / "outputs"
COALITIONS_FILE = OUTPUT_DIR / "case1_coalitions.csv"
SUMMARY_FILE = OUTPUT_DIR / "case1_summary.csv"

GAME_NAME = "[10:7,6,4,1]"
QUOTA = 10
PLAYERS = [
    ("Player 1", 7),
    ("Player 2", 6),
    ("Player 3", 4),
    ("Player 4", 1),
]


def to_display_value(value, digits=4):
    if isinstance(value, float):
        text = f"{value:.{digits}f}".rstrip("0").rstrip(".")
        return text if text else "0"
    return str(value)


def print_table(title, rows, headers):
    print(title)
    if not rows:
        print("(no rows)")
        return

    widths = {
        header: max(len(header), max(len(to_display_value(row[header])) for row in rows))
        for header in headers
    }

    print(" | ".join(f"{header:<{widths[header]}}" for header in headers))
    print("-+-".join("-" * widths[header] for header in headers))

    for row in rows:
        print(
            " | ".join(
                f"{to_display_value(row[header]):<{widths[header]}}"
                for header in headers
            )
        )


def write_csv(path, rows, headers):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main():
    player_weights = dict(PLAYERS)
    players = [player for player, _ in PLAYERS]
    total_weight = sum(weight for _, weight in PLAYERS)
    critical_counts = {player: 0 for player in players}
    coalition_rows = []

    for r in range(1, len(players) + 1):
        for coalition_tuple in itertools.combinations(players, r):
            coalition = list(coalition_tuple)
            coalition_weight = sum(player_weights[player] for player in coalition)
            winning = coalition_weight >= QUOTA

            critical_players = []
            if winning:
                for player in coalition:
                    reduced_weight = coalition_weight - player_weights[player]
                    if reduced_weight < QUOTA:
                        critical_players.append(player)
                        critical_counts[player] += 1

            coalition_rows.append(
                {
                    "Coalition": "{" + ", ".join(coalition) + "}",
                    "Total Weight": coalition_weight,
                    "Winning": "Yes" if winning else "No",
                    "Critical Players": ", ".join(critical_players) if critical_players else "--",
                }
            )

    coalition_rows.sort(key=lambda row: (row["Total Weight"], row["Coalition"]))

    total_swings = sum(critical_counts.values())
    summary_rows = []
    for player, weight in PLAYERS:
        normalized_weight = weight / total_weight
        normalized_banzhaf = critical_counts[player] / total_swings if total_swings else 0.0
        summary_rows.append(
            {
                "Player": player,
                "Weight": weight,
                "Normalized Weight Share": round(normalized_weight, 6),
                "Critical Count": critical_counts[player],
                "Normalized Banzhaf Index": round(normalized_banzhaf, 6),
            }
        )

    summary_rows.sort(
        key=lambda row: (
            -row["Normalized Banzhaf Index"],
            -row["Weight"],
            row["Player"],
        )
    )

    coalition_headers = ["Coalition", "Total Weight", "Winning", "Critical Players"]
    summary_headers = [
        "Player",
        "Weight",
        "Normalized Weight Share",
        "Critical Count",
        "Normalized Banzhaf Index",
    ]

    print(f"Game: {GAME_NAME}")
    print(f"Quota: {QUOTA}")
    print(f"Total weight: {total_weight}\n")

    print_table("=== COALITION TABLE ===", coalition_rows, coalition_headers)
    print()
    print_table("=== BANZHAF SUMMARY ===", summary_rows, summary_headers)

    write_csv(COALITIONS_FILE, coalition_rows, coalition_headers)
    write_csv(SUMMARY_FILE, summary_rows, summary_headers)

    print("\nSaved files:")
    print(f" - {COALITIONS_FILE.relative_to(ROOT_DIR)}")
    print(f" - {SUMMARY_FILE.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
