import itertools
import pandas as pd

# -----------------------------
# 1. Canada population data (%)
# -----------------------------
pop = {
    "ON": 38.8, "QC": 22.3, "BC": 13.7, "AB": 11.7,
    "MB": 3.6, "SK": 3.1, "NS": 2.6, "NB": 2.1, "NL": 1.4, "PE": 0.4
}

provinces = list(pop.keys())
n = len(provinces)

# -----------------------------
# 2. Voting rules
# -----------------------------
population_threshold = 0.50 * sum(pop.values())   # 50% population
state_threshold = 7                               # 7 provinces (7/50 rule)

# -----------------------------
# 3. Function to compute coalition table + Banzhaf
# -----------------------------
def analyze_system(use_dual_majority=False):
    rows = []
    critical_count = {p: 0 for p in provinces}

    for r in range(1, n + 1):
        for coalition in itertools.combinations(provinces, r):
            coalition = list(coalition)
            num_states = len(coalition)
            coalition_population = sum(pop[p] for p in coalition)

            # Conditions
            meets_pop = coalition_population >= population_threshold
            meets_state = num_states >= state_threshold if use_dual_majority else True

            winning = meets_pop and meets_state

            critical_states = []

            if winning:
                for p in coalition:
                    reduced = [x for x in coalition if x != p]
                    reduced_pop = sum(pop[x] for x in reduced)
                    reduced_states = len(reduced)

                    reduced_meets_pop = reduced_pop >= population_threshold
                    reduced_meets_state = (
                        reduced_states >= state_threshold if use_dual_majority else True
                    )

                    if not (reduced_meets_pop and reduced_meets_state):
                        critical_states.append(p)
                        critical_count[p] += 1

            rows.append({
                "Coalition": ", ".join(coalition),
                "#States": num_states,
                "Population": round(coalition_population, 1),
                "Winning": "Yes" if winning else "No",
                "Critical States": ", ".join(critical_states) if critical_states else "--"
            })

    coalition_df = pd.DataFrame(rows)

    # Banzhaf
    total_critical = sum(critical_count.values())
    summary_rows = []

    for p in provinces:
        beta = critical_count[p] / total_critical if total_critical > 0 else 0
        summary_rows.append({
            "Province": p,
            "Population %": pop[p],
            "Critical Count": critical_count[p],
            "Banzhaf Index": round(beta, 4)
        })

    summary_df = pd.DataFrame(summary_rows).sort_values(
        by="Banzhaf Index", ascending=False
    )

    return coalition_df, summary_df

# -----------------------------
# 4. Run both systems
# -----------------------------
coal_1, summary_1 = analyze_system(use_dual_majority=False)
coal_2, summary_2 = analyze_system(use_dual_majority=True)

# -----------------------------
# 5. Merge comparison
# -----------------------------
comparison = summary_1.merge(
    summary_2,
    on="Province",
    suffixes=(" (Pop Only)", " (7/50 Rule)")
)

# -----------------------------
# 6. Output
# -----------------------------
print("=== BANZHAF COMPARISON ===")
print(comparison.to_string(index=False))

# Save
coal_1.to_csv("canada_pop_only_coalitions.csv", index=False)
coal_2.to_csv("canada_7_50_coalitions.csv", index=False)
comparison.to_csv("canada_banzhaf_comparison.csv", index=False)

print("\nSaved files:")
print(" - canada_pop_only_coalitions.csv")
print(" - canada_7_50_coalitions.csv")
print(" - canada_banzhaf_comparison.csv")