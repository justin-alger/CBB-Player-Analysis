# 🏀 NCAA Scoring Analytics — 2025-26 Season

Interactive player report cards + full analytics notebook for ESPN's Top 500 college basketball scorers.

**[→ View the interactive app](https://justin-alger.github.io/cbb_player_cards.html)**

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

## Projects

### Project 1 — Scoring Archetypes (K-Means Clustering)
Clusters 500 players by *how* they score, not how many points they put up. Features: 3PA rate, FTA rate, FG%, 3P%, FT%, True Shooting%.

- **Stage 1:** Elbow + silhouette methods select k=2 (statistically optimal)
- **Stage 2:** Analyst override to k=4 for richer, scouting-ready archetypes

| Archetype | n | Identity |
|-----------|---|----------|
| 🔴 Paint Dominators | 43 | Interior scorers, highest FG% (~58%) |
| 🟢 Versatile Playmakers | 150 | Most complete scorers, highest TS% (~62%) |
| 🟠 Shot Creators | 158 | High-usage guards, below-avg efficiency |
| 🔵 Perimeter Snipers | 149 | 3-point specialists, best FT% (~84%) |

### Project 2 — Scoring Efficiency Index
Composite efficiency score (TS% + PPM + FTA Rate + AST/TO) vs. PPG rank.

**Key finding:** Jordan Riley (#2 PPG nationally) ranks **#299** in efficiency — a 297-position gap. Logan Duncomb (#56 PPG) ranks **#2** in efficiency.

---

*Data: ESPN Men's College Basketball, scraped 2026-02-23 · Analysis: Python 3, scikit-learn, matplotlib*
