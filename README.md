# 🏀 NCAA Scoring Analytics: 2025-26 Season

Interactive player report cards + full analytics notebook for ESPN's Top 500 college basketball scorers (PPG). 

>*Does the box score tell the full story? I built a framework to find out.*

**[→ View the Interactive Player Dashboard](https://justin-alger.github.io/CBB-Player-Analysis/cbb_player_cards_v2.html)**

---

## What's in this repo

| File | Description |
|------|-------------|
| `cbb_player_cards.html` | **Self-contained interactive web app**: player report cards, archetype filter, compare mode |
| `cbb_analytics_combined.ipynb` | Full Jupyter notebook: k=2 & k=4 clustering, efficiency index, all charts |
| `cbb_final_visuals.py` | Key visuals: report cards, leaderboard, case study |
| `espn-cbb top players ppg-2026-02-23.csv` | Raw scraped ESPN data (500 players) |
| `cbb_enriched_final.csv` | Enriched dataset with archetypes + efficiency scores |

---
## What This Is

An analytics deep-dive into ESPN's top 500 college basketball scorers, built to answer two questions:

1. **How do elite scorers actually differ from each other?** Not in how many points they score, but in *how* they produce them.
2. **Who might be overrated and who is flying completely under the radar?**

The result is an interactive dashboard where you can pull up any of the 500 players, see their full scoring profile, and compare them head-to-head.

---

## The Dashboard

**[→ Open it here](https://justin-alger.github.io/CBB-Player-Analysis/cbb_player_cards_v2.html)**

Every player card shows:
- Full shooting profile: FG%, 3P%, FT%, True Shooting %
- Shot selection fingerprint: how often they attack the rim vs. shoot threes
- Efficiency rank vs. PPG rank: are they more or less valuable than their scoring average suggests?
- Radar chart vs. their archetype average
- Scout-style narrative summary

**Features:**
- 🔍 Search any player or school
- 🎯 Filter by scoring archetype
- ↕️ Sort by PPG, efficiency, True Shooting %, biggest overrated/underrated gaps
- ⚖️ Compare any two players side by side

---

## The Four Scoring Archetypes

Players were clustered using K-Means on shot selection and efficiency metrics, not raw scoring volume. Four distinct profiles emerged:

| | Archetype | Identity |
|--|-----------|----------|
| 🔴 | **Paint Dominators** | Interior-first. Highest FG%. Rarely shoot threes. |
| 🟢 | **Versatile Playmakers** | The most complete scorers. Elite True Shooting %. Balanced from every zone. |
| 🟠 | **Shot Creators** | High-usage guards. Score in volume but efficiency lags. |
| 🔵 | **Perimeter Snipers** | Three-point specialists. Best FT%. Rarely attack the rim. |

---

## Key Findings

**The #2 scorer in the country might be overrated on paper...**
Jordan Riley (ECU) averages 23.6 PPG but ranks #299 out of 500 in composite efficiency. High volume but lower quality.

**The most efficient scorer you've never heard of.**
Logan Duncomb (Winthrop) ranks #56 in PPG but **#2 in efficiency** across all 500 players. 59.5% FG, elite rim presence, criminally underexposed.

**Efficiency and volume only agree at the very top.**
Cameron Boozer (Duke) is the rare case where PPG rank (#5) and efficiency rank (#5) are identical. **What you see really is what you get**.

---

## Methodology (Summary)

- **Clustering:** K-Means on six shot-profile and efficiency features. Optimal k (2) evaluated via elbow method and silhouette scoring, but expanded the analysis to 4 clusters for more meaningful insights.
- **Efficiency Score:** Composite of True Shooting %, Points Per Minute, FT Attempt Rate, and AST/TO Ratio — each z-score normalized and equally weighted.
- **Rank Delta:** PPG Rank − Efficiency Rank. Positive = underrated. Negative = overrated.
- **Data:** ESPN Men's College Basketball, scraped February 2026. 500 players across 305 programs.

---
Author: Justin Alger

*Built as part of an ongoing sports analytics series. Catch up with me on [LinkedIn](https://www.linkedin.com/in/justin-alger/) or on my website [Integ Analytics](https://www.integanalytics.com).*
