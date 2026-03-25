# Banzhaf Power Index

This repository contains code and notes for a Simon Fraser University mathematics project on the **Banzhaf Power Index** in weighted and EU-style dual-majority voting systems.

## Team Members

- **Cira Chen** — sca386@sfu.ca
- **Allen Gao** — yga110@sfu.ca
- **JunHang Wu** — jwa337@sfu.ca

## Project Goal

The project studies the difference between **formal size** and **actual voting power** in collective decision systems.

A weighted voting game is written in the form:

\[
[q : w_1, w_2, \dots, w_n]
\]

where:

- \(q\) is the quota required to pass a motion
- \(w_i\) is the voting weight of player \(i\)

The main goal is to compute and analyze the **Banzhaf Power Index**, which measures how often a voter is **critical** in a winning coalition.

The current codebase supports two main case studies:

- Case Study I: the exact weighted voting game `[10:7,6,4,1]`
- Case Study II: a 6-country **EU dual-majority mini-model**
- exact coalition enumeration in both cases
- comparison of formal size vs. `Banzhaf power`

## Repository Structure

```text
.
├── AGENT.md
├── README.md
├── code/
│   ├── eu_mini_banzhaf.py
│   ├── case1_weighted_game.py
│   ├── plot_eu_mini.py
│   └── outputs/
│       ├── case1_coalitions.csv
│       ├── case1_summary.csv
│       ├── eu_mini_case_coalitions.csv
│       ├── eu_mini_case_summary.csv
│       └── eu_mini_population_vs_banzhaf.svg
├── data/
│   ├── eu_mini_population.json
│   └── examples.md
└── report/
```

## Main Files

### `code/eu_mini_banzhaf.py`

Core implementation for the 6-country EU dual-majority mini-model.

Functions included:

- load the population dataset from `data/eu_mini_population.json`
- enumerate all nonempty coalitions
- test whether a coalition satisfies both thresholds
- identify critical players by deletion
- compute raw Banzhaf counts
- compute normalized Banzhaf indices
- export coalition and summary tables to CSV

This file is useful for:
- checking the mini-model exactly
- generating coalition tables
- producing summary tables for the report

### `code/case1_weighted_game.py`

Exact coalition analysis for Case Study I, the weighted voting game `[10:7,6,4,1]`.

This file:

- enumerates all nonempty coalitions
- classifies each coalition as winning or losing
- identifies critical players by deletion
- computes raw Banzhaf counts
- compares normalized weight share with normalized Banzhaf power
- exports Case 1 coalition and summary tables to CSV

This file is useful for:
- filling the Case Study I table in the report
- verifying the swing-count calculation exactly
- showing that Players 1, 2, and 3 have equal power despite unequal weights

### `code/plot_eu_mini.py`

Simple visualization generator for the mini-model summary output.

This file:

- reads `code/outputs/eu_mini_case_summary.csv`
- generates an SVG scatter plot
- compares `Population Share` with `Normalized Banzhaf Index`
- writes the figure to `code/outputs/eu_mini_population_vs_banzhaf.svg`

This file is useful for:
- adding a report-ready visual comparison
- showing where countries sit relative to the `power = population share` line

### `data/eu_mini_population.json`

Dataset and metadata for the 6-country teaching example.

This file includes:

- the selected countries
- population values in millions
- the reference date
- source metadata
- the mini-model voting rule

## Mathematical Idea

For the current project:

- A **coalition** is any subset of players.
- In Case Study I, a coalition is **winning** if its total weight meets the quota.
- In the EU mini-model, a coalition is **winning** if it satisfies both conditions:
  - at least 4 supporting states
  - at least 65% of the sample population
- A player is **critical** in a winning coalition if removing that player makes the coalition losing.
- The **raw Banzhaf count** of a player is the number of coalitions where that player is critical.
- The **normalized Banzhaf index** is the player's raw count divided by the total raw count of all players.

## How to Run

Make sure Python 3 is installed.

Run:

```bash
python3 code/case1_weighted_game.py
python3 code/eu_mini_banzhaf.py
python3 code/plot_eu_mini.py
```

The first command regenerates:

- `code/outputs/case1_coalitions.csv`
- `code/outputs/case1_summary.csv`

The second command regenerates:

- `code/outputs/eu_mini_case_coalitions.csv`
- `code/outputs/eu_mini_case_summary.csv`

The third command regenerates:

- `code/outputs/eu_mini_population_vs_banzhaf.svg`

## Mini-Model Workflow

```text
Load 6-country dataset and rule
    ->
Enumerate all coalitions
    ->
Check dual-majority rule
    ->
Check critical players
    ->
Count swings for each player
    ->
Normalize counts
    ->
Compare population share vs. Banzhaf power
    ->
Export CSV tables
    ->
Generate SVG figure
```

## Example Output

`code/eu_mini_banzhaf.py` prints:

- dataset metadata
- the full coalition table
- the Banzhaf summary table

`code/plot_eu_mini.py` exports a scatter plot for the EU mini-model comparing:

- `Population Share`
- `Normalized Banzhaf Index`

## Why This Code Is Useful

This code supports the written report by:

- verifying manual computations
- making the mini-model reproducible from a dataset file
- generating clean tables and a figure for the report
- helping demonstrate that **population share does not always equal voting power**

## Notes

This code is intended as a project support tool. The main report should still explain the mathematics clearly with worked examples, algorithm logic, and interpretation.
