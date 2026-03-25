import itertools
import pandas as pd

# -----------------------------
# 1. Input real countries + populations
# Replace these with official Eurostat values you want to use
# -----------------------------
pop = {
    "Germany": 83.6,
    "France": 68.4,
    "Spain": 48.6,
    "Netherlands": 18.0,
    "Malta": 0.6,
    "Luxembourg": 0.7
}

countries = list(pop.keys())
n = len(countries)

# -----------------------------
# 2. Simplified EU-style dual-majority rule
# For 6 countries:
# - at least 4 countries in favour
# - at least 65% of total population
# -----------------------------
state_threshold = 4
total_population = sum(pop.values())
population_threshold = 0.65 * total_population

# -----------------------------
# 3. Enumerate all coalitions
# -----------------------------
rows = []
critical_count = {c: 0 for c in countries}

for r in range(1, n + 1):
    for coalition in itertools.combinations(countries, r):
        coalition = list(coalition)
        num_states = len(coalition)
        coalition_population = sum(pop[c] for c in coalition)

        meets_state = num_states >= state_threshold
        meets_population = coalition_population >= population_threshold
        winning = meets_state and meets_population

        critical_states = []

        if winning:
            for c in coalition:
                reduced = [x for x in coalition if x != c]
                reduced_num_states = len(reduced)
                reduced_population = sum(pop[x] for x in reduced)

                reduced_meets_state = reduced_num_states >= state_threshold
                reduced_meets_population = reduced_population >= population_threshold
                reduced_winning = reduced_meets_state and reduced_meets_population

                if not reduced_winning:
                    critical_states.append(c)
                    critical_count[c] += 1

        rows.append({
            "Coalition": ", ".join(coalition),
            "#States": num_states,
            "Population": round(coalition_population, 1),
            "Meets state threshold": "Yes" if meets_state else "No",
            "Meets population threshold": "Yes" if meets_population else "No",
            "Winning": "Yes" if winning else "No",
            "Critical states": ", ".join(critical_states) if critical_states else "--"
        })

# -----------------------------
# 4. Full coalition table
# -----------------------------
coalition_df = pd.DataFrame(rows)

# Sort for readability
coalition_df = coalition_df.sort_values(
    by=["#States", "Population"],
    ascending=[True, True]
).reset_index(drop=True)

# -----------------------------
# 5. Banzhaf summary
# -----------------------------
total_critical = sum(critical_count.values())

summary_rows = []
for c in countries:
    beta = critical_count[c] / total_critical if total_critical > 0 else 0
    summary_rows.append({
        "Country": c,
        "Population": pop[c],
        "Critical Count": critical_count[c],
        "Normalized Banzhaf Index": round(beta, 4)
    })

summary_df = pd.DataFrame(summary_rows).sort_values(
    by="Normalized Banzhaf Index", ascending=False
).reset_index(drop=True)

# -----------------------------
# 6. Print results
# -----------------------------
print("=== FULL COALITION TABLE ===")
print(coalition_df.to_string(index=False))

print("\n=== BANZHAF SUMMARY ===")
print(summary_df.to_string(index=False))

# -----------------------------
# 7. Save to CSV (optional)
# -----------------------------
coalition_df.to_csv("eu_mini_case_coalitions.csv", index=False)
summary_df.to_csv("eu_mini_case_summary.csv", index=False)

print("\nSaved files:")
print(" - eu_mini_case_coalitions.csv")
print(" - eu_mini_case_summary.csv")