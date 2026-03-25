# AGENT.md

## Project
**Voting Weight vs. Voting Power: An Analysis of the Banzhaf Power Index in Weighted and Dual-Majority Voting Games**

## Purpose
This project studies how actual voting power differs from formal voting weight or institutional voting rules in collective decision systems. The main tool is the **Banzhaf Power Index**, which measures how often a player is critical in winning coalitions.

The report should combine:
- exact hand-worked mathematics for small weighted voting games
- one medium-to-advanced computational case study based on the **European Union Council voting system under the Treaty of Lisbon**

## Core Research Question
To what extent does a player's formal voting weight, population share, or institutional role correspond to their actual influence in a voting game?

## Main Thesis
Formal weight is only one determinant of voting power. Coalition structure, quota choice, and multi-condition voting rules can cause players with different sizes to have similar power, or cause apparently large players to have less influence than their raw weight suggests.

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

### Dual-majority extension
For the EU case study, the winning condition is not a single weighted quota. Instead, for a coalition \(S\) of member states, passage requires both:

\[
|S| \ge 15
\]

and

\[
P(S) \ge 0.65
\]

where \(|S|\) is the number of supporting states and \(P(S)\) is the coalition's share of total EU population.

Thus the EU case should be treated as a **dual-majority voting game** with an AND condition rather than a standard one-quota weighted game.

---

## Project Scope
The project should combine exact, interpretable mathematics with one computationally serious real-world application.

### Required components
1. Formal definition of weighted voting games and Banzhaf power
2. Explanation of coalition enumeration and the deletion test for criticality
3. At least one complete hand-worked small voting game
4. A second case study on the **EU Council voting system under the Treaty of Lisbon**
5. Python-based computation for the EU case, since the full coalition space is \(2^{27}\)
6. Comparison of Banzhaf power against formal weight share or population share
7. Discussion of how quota rules and institutional design affect power

### Recommended case studies
- **Case 1:** \([10:7,6,4,1]\)
- **Case 2:** **European Union Council voting under the Treaty of Lisbon**
  - 27 member states
  - approval requires at least 55% of member states, i.e. at least 15 of 27 states, and at least 65% of EU population
  - use Python to compute or rigorously approximate swing counts
  - compare each state's population share with its Banzhaf index

### Optional extensions
- blocking-minority discussion for the EU rule
- reinforced qualified majority as a comparison rule
- visualization of population share vs. Banzhaf power
- sensitivity analysis under alternative quotas

For the EU case, exact computation is preferred when feasible. If approximation or sampling is used, it must be clearly labeled, justified, and tested against smaller exact examples.

---

## Academic Depth Rationale
The EU case study raises the project to a stronger upper-level undergraduate standard because it introduces:
- **computational complexity**: the coalition space is \(2^{27}\), so the analysis is beyond hand calculation
- **multi-dimensional quotas**: winning depends on two simultaneous thresholds rather than one
- **policy relevance**: the institutional rule comes from a major real-world political system
- **computational methodology**: the report must explain how Python is used to evaluate coalitions and critical players

The report should not paste large blocks of code. Instead, it should show:
- the algorithm logic used to test whether a coalition satisfies both conditions
- a short description of the implementation strategy
- visual output, especially a comparison between population share and Banzhaf power

---

## Expected Mathematical Themes
The report should highlight the following ideas:
- larger weight does not guarantee proportionally larger power
- different players can have equal Banzhaf power despite unequal weights
- some players can be dummy players with zero power
- quota choice can dramatically change power distribution
- multi-condition rules can alter power in ways that a single weighted quota cannot capture
- voting systems are shaped by coalition structure, not only raw size

### Expected EU case-study insight
A strong hypothesis for the EU section is that the dual-majority rule moderates the dominance of the largest states and increases the leverage of some medium-sized states. The reason is structural:
- large states matter for the population threshold
- every state counts equally toward the member-state threshold

This should be presented as a result to test computationally, not as an assumption to assert without evidence.

---

## Preferred Report Structure
1. Introduction
2. Background and definitions
3. Methodology
4. Case study 1: exact weighted voting analysis
5. Case study 2: EU dual-majority computational analysis
6. Results and discussion
7. Limitations
8. Conclusion

---

## Calculation Workflow
Use this pipeline for every example:

```text
Define the player set and voting rule
   -> generate coalitions or use a validated computational method
   -> test whether each coalition is winning
   -> for each winning coalition, test each member by deletion
   -> count critical occurrences eta_i
   -> normalize to beta_i
   -> compare beta_i with weight share or population share
   -> interpret the gap between formal size and actual power
```

For the EU case, the winning test is:

```text
count_supporting_states >= 15
AND
population_share_of_supporting_states >= 0.65
```

---

## Quality Control Rules
When generating or reviewing content for this project:

### Always do
- keep notation consistent
- distinguish raw swing counts from normalized indices
- verify every coalition table entry in small cases
- describe the EU rule as a dual-majority system, not a simple weighted game
- state clearly whether a computation is exact or approximate
- interpret each example in words after computing it
- explain why a player is or is not critical
- compare power and weight or population explicitly
- record the population dataset and date used for the EU analysis
- mention assumptions and limitations of the model

### Never do
- assume weight equals power without proof
- present a table without discussing it
- switch between quota values without clearly stating the game
- reduce the EU rule to a single synthetic weight without justification
- report computational results without describing the algorithm
- include real-world claims without checking the data
- introduce Shapley-Shubik as a main method unless explicitly needed

---

## Deliverable Standards
The final written report should:
- be mathematically correct
- include at least two complete case studies
- include one medium-to-advanced computational section
- explain the algorithm used for the EU analysis
- contain at least one visualization comparing population share and Banzhaf power
- use clean tables and consistent notation
- connect the numerical results to the broader question of power vs. weight

---

## If Writing New Content Later
Future writing should align with this style:
- concise but rigorous
- explanatory rather than overly abstract
- focused on Banzhaf unless comparison is explicitly requested
- suitable for an upper-level undergraduate math project with a meaningful computational component

### Good output types
- report paragraphs
- theorem-style definitions
- coalition tables
- pseudocode or short algorithm descriptions
- result summaries
- LaTeX-ready formulas
- interpretation paragraphs
- visualization captions

### Good future tasks
- compute Banzhaf indices for a new game
- draft a section of the report
- verify coalition tables
- compare quota changes
- compute the EU dual-majority case in Python
- generate a population-share vs. Banzhaf plot
- convert results into IEEE/LaTeX format
