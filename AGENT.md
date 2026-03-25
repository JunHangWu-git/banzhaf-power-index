# AGENT.md

## Project
**Voting Weight vs. Voting Power: An Analysis of the Banzhaf Power Index in Weighted Voting Games**

## Purpose
This project studies how actual voting power differs from assigned voting weight in weighted voting systems. The main tool is the **Banzhaf Power Index**, which measures how often a player is critical in winning coalitions.

## Core Research Question
To what extent does a player's formal voting weight correspond to their actual influence in a weighted voting game?

## Main Thesis
Voting weight does not always equal voting power. Coalition structure and quota choice can cause players with different weights to have equal power, or cause players with positive weight to have zero effective influence.

---

## Mathematical Setup
A weighted voting game is written as:

\[
[q:w_1,w_2,\dots,w_n]
\]

where:
- \(q\) = quota required for passage
- \(w_i\) = voting weight of player \(i\)
- a coalition is any subset of players

A coalition \(S\) is **winning** if:

\[
\sum_{i\in S} w_i \ge q
\]

A player \(i\in S\) is **critical** in coalition \(S\) if:

\[
W(S) \ge q \quad \text{and} \quad W(S\setminus\{i\}) < q
\]

Let \(\eta_i\) be the number of coalitions in which player \(i\) is critical. The normalized Banzhaf index is:

\[
\beta_i = \frac{\eta_i}{\sum_j \eta_j}
\]

For comparison, the normalized weight share is:

\[
\omega_i = \frac{w_i}{\sum_j w_j}
\]

---

## Project Scope
The project should prioritize exact, interpretable mathematics over oversized real-world complexity.

### Required components
1. Formal definition of weighted voting games
2. Explanation of coalition enumeration
3. Definition of critical players using the deletion test
4. Calculation of raw swing counts and normalized Banzhaf indices
5. Comparison of Banzhaf power with normalized weight share
6. Discussion of how quota changes affect power

### Recommended case studies
- **Case 1:** \([10:7,6,4,1]\)
- **Case 2:** \([6:4,3,2,1]\)
- **Case 3:** fixed weights with varying quotas

### Optional extension
- Python computation for larger examples
- Simplified corporate governance interpretation
- Simplified real-world council or electoral example

Do not make a large computational case study the core of the report unless the code and data are already reliable.

---

## Expected Mathematical Themes
The report should highlight the following ideas:
- larger weight does not guarantee proportionally larger power
- different players can have equal Banzhaf power despite unequal weights
- some players can be dummy players with zero power
- quota choice can dramatically change power distribution
- voting systems are shaped by coalition structure, not only raw weights

---

## Preferred Report Structure
1. Introduction
2. Background and definitions
3. Methodology
4. Case studies and computation
5. Results and discussion
6. Limitations
7. Conclusion

---

## Calculation Workflow
Use this pipeline for every example:

```text
Select weighted voting game
   -> list all nonempty coalitions
   -> compute coalition weights
   -> classify winning vs losing
   -> for each winning coalition, test each member by deletion
   -> count critical occurrences eta_i
   -> normalize to beta_i
   -> compare beta_i with omega_i
   -> interpret result
```

---

## Quality Control Rules
When generating or reviewing content for this project:

### Always do
- keep notation consistent
- distinguish raw swing counts from normalized indices
- verify every coalition table entry
- interpret each example in words after computing it
- explain why a player is or is not critical
- compare power and weight explicitly
- mention assumptions and limitations of the model

### Never do
- assume weight equals power without proof
- present a table without discussing it
- switch between quota values without clearly stating the game
- include real-world claims without checking the data
- introduce Shapley-Shubik as a main method unless explicitly needed

---

## Deliverable Standards
The final written report should:
- be mathematically correct
- include at least two complete worked examples
- contain at least one deeper analytical comparison, preferably quota sensitivity
- use clean tables and consistent notation
- connect the numerical results to the broader question of power vs weight

---

## If Writing New Content Later
Future writing should align with this style:
- concise but rigorous
- explanatory rather than overly abstract
- focused on Banzhaf unless comparison is explicitly requested
- suitable for an upper-level undergraduate math project

### Good output types
- report paragraphs
- theorem-style definitions
- coalition tables
- result summaries
- LaTeX-ready formulas
- interpretation paragraphs

### Good future tasks
- compute Banzhaf indices for a new game
- draft a section of the report
- verify coalition tables
- compare quota changes
- convert results into IEEE/LaTeX format