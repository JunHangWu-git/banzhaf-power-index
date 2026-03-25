import csv
import itertools
import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT_DIR / "data" / "eu_mini_population.json"
OUTPUT_DIR = ROOT_DIR / "code" / "outputs"
COALITIONS_FILE = OUTPUT_DIR / "eu_mini_case_coalitions.csv"
SUMMARY_FILE = OUTPUT_DIR / "eu_mini_case_summary.csv"


def load_dataset(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


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

    header_line = " | ".join(f"{header:<{widths[header]}}" for header in headers)
    divider_line = "-+-".join("-" * widths[header] for header in headers)

    print(header_line)
    print(divider_line)

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
    dataset = load_dataset(DATA_FILE)
    countries_data = dataset["countries"]

    populations = {
        row["country"]: row["population_millions"]
        for row in countries_data
    }
    countries = [row["country"] for row in countries_data]
    n = len(countries)

    rule = dataset["rule"]
    state_threshold = rule["state_threshold_count"]
    population_threshold_share = rule["population_threshold_share"]

    total_population = sum(populations.values())
    population_threshold = population_threshold_share * total_population

    coalition_rows = []
    critical_count = {country: 0 for country in countries}

    for r in range(1, n + 1):
        for coalition_tuple in itertools.combinations(countries, r):
            coalition = list(coalition_tuple)
            coalition_population = sum(populations[country] for country in coalition)
            coalition_share = coalition_population / total_population

            meets_state = len(coalition) >= state_threshold
            meets_population = coalition_share >= population_threshold_share
            winning = meets_state and meets_population

            critical_states = []
            if winning:
                for country in coalition:
                    reduced = [member for member in coalition if member != country]
                    reduced_population = sum(populations[member] for member in reduced)
                    reduced_share = reduced_population / total_population
                    reduced_winning = (
                        len(reduced) >= state_threshold
                        and reduced_share >= population_threshold_share
                    )
                    if not reduced_winning:
                        critical_states.append(country)
                        critical_count[country] += 1

            coalition_rows.append(
                {
                    "Coalition": ", ".join(coalition),
                    "States": len(coalition),
                    "Population (millions)": round(coalition_population, 3),
                    "Population Share": round(coalition_share, 6),
                    "Meets State Threshold": "Yes" if meets_state else "No",
                    "Meets Population Threshold": "Yes" if meets_population else "No",
                    "Winning": "Yes" if winning else "No",
                    "Critical States": ", ".join(critical_states) if critical_states else "--",
                }
            )

    coalition_rows.sort(key=lambda row: (row["States"], row["Population (millions)"]))

    total_critical = sum(critical_count.values())
    summary_rows = []
    for row in countries_data:
        country = row["country"]
        population = row["population_millions"]
        population_share = population / total_population
        banzhaf = critical_count[country] / total_critical if total_critical else 0.0
        summary_rows.append(
            {
                "Country": country,
                "Population (millions)": round(population, 3),
                "Population Share": round(population_share, 6),
                "Critical Count": critical_count[country],
                "Normalized Banzhaf Index": round(banzhaf, 6),
            }
        )

    summary_rows.sort(
        key=lambda row: (
            -row["Normalized Banzhaf Index"],
            -row["Population (millions)"],
            row["Country"],
        )
    )

    coalition_headers = [
        "Coalition",
        "States",
        "Population (millions)",
        "Population Share",
        "Meets State Threshold",
        "Meets Population Threshold",
        "Winning",
        "Critical States",
    ]
    summary_headers = [
        "Country",
        "Population (millions)",
        "Population Share",
        "Critical Count",
        "Normalized Banzhaf Index",
    ]

    print(f"Dataset: {dataset['dataset_name']}")
    print(f"Reference date: {dataset['reference_date']}")
    print(
        "Rule: at least "
        f"{state_threshold} states and at least {population_threshold_share:.0%} of total population"
    )
    print(f"Total population in sample: {total_population:.3f} million")
    print(f"Population threshold in sample: {population_threshold:.3f} million\n")

    print_table("=== FULL COALITION TABLE ===", coalition_rows, coalition_headers)
    print()
    print_table("=== BANZHAF SUMMARY ===", summary_rows, summary_headers)

    write_csv(COALITIONS_FILE, coalition_rows, coalition_headers)
    write_csv(SUMMARY_FILE, summary_rows, summary_headers)

    print("\nSaved files:")
    print(f" - {COALITIONS_FILE.relative_to(ROOT_DIR)}")
    print(f" - {SUMMARY_FILE.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
