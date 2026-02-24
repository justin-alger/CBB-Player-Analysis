# 🏀 NCAA Scoring Analytics — 2025-26 Season

Interactive player report cards + full analytics notebook for ESPN's Top 500 college basketball scorers. 

>*Does the box score tell the full story? We built a framework to find out.*

**[→ View the Interactive Player Dashboard](https://justin-alger.github.io/CBB-Player-Analysis/cbb_player_cards.html)**

---

## What's in this repo

| File | Description |
|------|-------------|
| `cbb_player_cards.html` | **Self-contained interactive web app** — player report cards, archetype filter, compare mode |
| `cbb_analytics_notebook.ipynb` | Full Jupyter notebook — k=2 & k=4 clustering, efficiency index, all charts |
| `cbb_analytics.py` | Standalone Python script (generates all static charts) |
| `cbb_project1_v2.py` | Project 1 v2 — k=4 archetype analysis |
| `cbb_final_visuals.py` | Capstone visuals — report cards, leaderboard, case study |
| `cbb_players.csv` | Raw scraped ESPN data (500 players) |
| `cbb_enriched_final.csv` | Enriched dataset with archetypes + efficiency scores |

---
## What This Is

An analytics deep-dive into ESPN's top 500 college basketball scorers, built to answer two questions:

1. **How do elite scorers actually differ from each other?** Not in how many points they score — but in *how* they produce them.
2. **Who is the country overrating — and who is flying completely under the radar?**

The result is an interactive dashboard where you can pull up any of 500 players, see their full scoring profile, and compare them head-to-head.

---

## The Dashboard

**[→ Open it here](https://justin-alger.github.io/CBB-Player-Analysis/cbb_player_cards.html)**

Every player card shows:
- Full shooting profile: FG%, 3P%, FT%, True Shooting %
- Shot selection fingerprint: how often they attack the rim vs. shoot threes
- Efficiency rank vs. PPG rank: are they more or less valuable than their scoring average suggests?
- Radar chart vs. their archetype average
- Scout-style narrative summary

**Features:**
- 🔍 Search any player or school
- 🎯 Filter by scoring archetype
- ↕️ Sort by PPG, efficiency, True Shooting%, biggest overrated/underrated gaps
- ⚖️ Compare any two players side by side

---

## The Four Scoring Archetypes

Players were clustered using K-Means on shot selection and efficiency metrics — not raw scoring volume. Four distinct profiles emerged:

| | Archetype | Identity |
|--|-----------|----------|
| 🔴 | **Paint Dominators** | Interior-first. Highest FG%. Rarely shoots threes. |
| 🟢 | **Versatile Playmakers** | The most complete scorers. Elite True Shooting%. Balanced from every zone. |
| 🟠 | **Shot Creators** | High-usage guards. Score in volume — but efficiency lags. |
| 🔵 | **Perimeter Snipers** | Three-point specialists. Best FT%. Rarely attacks the rim. |

---

## Key Findings

**The #2 scorer in the country might overrated...**
Jordan Riley (ECU) averages 23.6 PPG — but ranks #299 out of 500 in composite efficiency. High volume, lower quality.

**The most efficient scorer you've never heard of.**
Logan Duncomb (Winthrop) ranks #56 in PPG but **#2 in efficiency** across all 500 players. 59.5% FG, elite rim presence, criminally underexposed.

**Efficiency and volume only agree at the very top.**
Cameron Boozer (Duke) is the rare case where PPG rank (#5) and efficiency rank (#5) are identical. What you see really is what you get.

---

## Methodology (Summary)

- **Clustering:** K-Means on six shot-profile and efficiency features. Optimal k evaluated via elbow method and silhouette scoring.
- **Efficiency Score:** Composite of True Shooting %, Points Per Minute, FT Attempt Rate, and AST/TO Ratio — each z-score normalised and equally weighted.
- **Rank Delta:** PPG Rank − Efficiency Rank. Positive = underrated. Negative = overrated.
- **Data:** ESPN Men's College Basketball, scraped February 2026. 500 players, 305 programs.

---

*Built as part of an ongoing sports analytics series. Catch up with me on [LinkedIn](https://www.linkedin.com/in/justin-alger/).*
