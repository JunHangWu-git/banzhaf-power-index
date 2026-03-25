# Banzhaf Power Index

This repository contains code and notes for a Simon Fraser University mathematics project on the **Banzhaf Power Index** in weighted voting games.

## Team Members

- **Cira Chen** — sca386@sfu.ca
- **Allen Gao** — yga110@sfu.ca
- **JunHang Wu** — jwa337@sfu.ca

## Project Goal

The project studies the difference between **voting weight** and **actual voting power** in a weighted voting system.

A weighted voting game is written in the form:

\[
[q : w_1, w_2, \dots, w_n]
\]

where:

- \(q\) is the quota required to pass a motion
- \(w_i\) is the voting weight of player \(i\)

The main goal is to compute and analyze the **Banzhaf Power Index**, which measures how often a voter is **critical** in a winning coalition.

## Repository Structure

```text
.
├── README.md
├── banzhaf.py
├── quota_analysis.py
└── outputs/
```

## Files

### `banzhaf.py`

Core implementation for weighted voting games.

Functions included:

- define a weighted voting game
- enumerate all coalitions
- compute coalition weights
- determine winning coalitions
- identify critical players
- compute raw Banzhaf counts
- compute normalized Banzhaf indices
- compare voting power with weight share

This file is useful for:
- checking hand calculations
- generating coalition tables
- producing summary tables for the report

### `quota_analysis.py`

Quota sensitivity analysis.

This file:

- imports `banzhaf.py`
- fixes a set of player weights
- varies the quota from `1` to `sum(weights)`
- computes Banzhaf indices for each quota
- prints a quota-by-quota summary
- exports results to CSV

This file is useful for:
- showing that **changing the quota changes actual power**
- generating tables or figures for the report
- comparing weight share vs. Banzhaf power across different thresholds

## Mathematical Idea

For a weighted voting game:

- A **coalition** is any subset of players.
- A coalition is **winning** if its total weight is at least the quota.
- A player is **critical** in a winning coalition if removing that player makes the coalition losing.
- The **raw Banzhaf count** of a player is the number of coalitions where that player is critical.
- The **normalized Banzhaf index** is the player's raw count divided by the total raw count of all players.

## How to Run

Make sure Python 3 is installed.

Run:

```bash
python banzhaf.py
python quota_analysis.py
```

## Example Workflow

```text
Choose game [q : w1, w2, ..., wn]
    ->
Enumerate all coalitions
    ->
Find winning coalitions
    ->
Check critical players
    ->
Count swings for each player
    ->
Normalize counts
    ->
Compare:
   voting weight share
   vs
   Banzhaf power
    ->
Export tables / figures for report
```

## Example Output

`banzhaf.py` prints a readable summary of one weighted voting game.

`quota_analysis.py` prints a quota table and exports a CSV file into `outputs/`.

## Why This Code Is Useful

This code supports the written report by:

- verifying manual computations
- handling larger examples cleanly
- making quota comparisons easier
- helping demonstrate that **weight does not always equal power**

## Notes

This code is intended as a project support tool. The main report should still explain the mathematics clearly with worked examples and interpretation.
