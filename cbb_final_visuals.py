"""
Final Visuals — Engagement-First Design
Projects 1 & 2 Completion: Report Cards, Leaderboard, Connector, Case Study
"""
import pandas as pd, numpy as np
import matplotlib, matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch, Circle
import matplotlib.patheffects as pe
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.stats import zscore
import warnings; warnings.filterwarnings('ignore')
matplotlib.use('Agg')

# ── Style ─────────────────────────────────────────────────────────────────────
BG, PANEL, GRID = '#0D1117', '#161B22', '#21262D'
TEXT, MUTED      = '#E6EDF3', '#8B949E'
ARCHETYPE_COLORS = {
    'Paint Dominators':     '#FF7B72',
    'Shot Creators':        '#F0883E',
    'Versatile Playmakers': '#3FB950',
    'Perimeter Snipers':    '#58A6FF',
}
ARCHETYPE_ICONS = {
    'Paint Dominators':     '🔴',
    'Shot Creators':        '🟠',
    'Versatile Playmakers': '🟢',
    'Perimeter Snipers':    '🔵',
}
plt.rcParams.update({
    'figure.facecolor':BG,'axes.facecolor':PANEL,'axes.edgecolor':GRID,
    'axes.labelcolor':TEXT,'axes.titlecolor':TEXT,'xtick.color':MUTED,
    'ytick.color':MUTED,'text.color':TEXT,'grid.color':GRID,
    'grid.linewidth':0.6,'font.family':'DejaVu Sans','figure.dpi':150,
})

# ── Rebuild dataset ───────────────────────────────────────────────────────────
df = pd.read_csv('espn-cbb top players ppg-2026-02-23.csv')
df['3PA_rate'] = df['3PA'] / df['FGA']
df['FTA_rate'] = df['FTA'] / df['FGA']
df['TS_pct']   = df['PTS'] / (2*(df['FGA']+0.44*df['FTA']))
df['PPM']      = df['PTS'] / df['MIN']
df['AST_TO']   = df['AST'] / df['TO'].replace(0,0.1)
df['Position'] = df['Position'].replace('PG','G')

cluster_features = ['3PA_rate','FTA_rate','FGPct','3PPct','FTPct','TS_pct']
X_scaled = StandardScaler().fit_transform(df[cluster_features])
df['Cluster'] = KMeans(n_clusters=4,random_state=42,n_init=10).fit_predict(X_scaled)
means = df.groupby('Cluster')[cluster_features].mean()
s3pa  = means['3PA_rate'].sort_values()
paint_c = s3pa.index[0]; sniper_c = s3pa.index[-1]
mid = [i for i in means.index if i not in [paint_c,sniper_c]]
vers_c = max(mid, key=lambda c: means.loc[c,'TS_pct'])
creat_c = [c for c in mid if c!=vers_c][0]
c2a = {paint_c:'Paint Dominators',creat_c:'Shot Creators',
       vers_c:'Versatile Playmakers',sniper_c:'Perimeter Snipers'}
df['Archetype'] = df['Cluster'].map(c2a)

eff_features = ['TS_pct','PPM','FTA_rate','AST_TO']
df_eff = df[eff_features].copy()
for col in eff_features:
    df_eff[col+'_z'] = zscore(df_eff[col])
df['Efficiency_Score'] = df_eff[[c+'_z' for c in eff_features]].mean(axis=1)
df['PPG_Rank']   = df['PTS'].rank(ascending=False).astype(int)
df['Eff_Rank']   = df['Efficiency_Score'].rank(ascending=False).astype(int)
df['Rank_Delta'] = df['PPG_Rank'] - df['Eff_Rank']

# Normalize features 0-1 for radar
radar_features = ['3PA_rate','FTA_rate','FGPct','3PPct','FTPct','TS_pct']
radar_labels   = ['3PA Rate','FTA Rate','FG%','3P%','FT%','True\nShooting%']
for col in radar_features:
    df[col+'_norm'] = (df[col]-df[col].min())/(df[col].max()-df[col].min())
archetype_means_norm = df.groupby('Archetype')[[c+'_norm' for c in radar_features]].mean()

# ── Helper: draw a single radar ───────────────────────────────────────────────
def draw_radar(ax, player_vals, archetype_vals, color, labels):
    N      = len(labels)
    angles = np.linspace(0,2*np.pi,N,endpoint=False).tolist()
    angles += angles[:1]
    pv = player_vals + [player_vals[0]]
    av = archetype_vals + [archetype_vals[0]]
    # Archetype average (ghost)
    ax.fill(angles, av, color=color, alpha=0.10)
    ax.plot(angles, av, color=color, linewidth=1.2, linestyle='--', alpha=0.45)
    # Player profile
    ax.fill(angles, pv, color=color, alpha=0.28)
    ax.plot(angles, pv, color=color, linewidth=2.5)
    # Dots on vertices
    ax.scatter(angles[:-1], player_vals, color=color, s=40, zorder=5)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color=TEXT, fontsize=8.5)
    ax.set_ylim(0,1); ax.set_yticks([])
    ax.spines['polar'].set_color(GRID)
    ax.grid(color=GRID, linewidth=0.6)
    for r in [0.25,0.5,0.75]:
        ax.plot(angles,[r]*len(angles),color=GRID,linewidth=0.5,linestyle=':')

# ── Report card subjects ──────────────────────────────────────────────────────
subjects = {
    'Paint Dominators':     'Logan Duncomb',
    'Versatile Playmakers': 'Cameron Boozer',
    'Shot Creators':        'Jordan Riley',
    'Perimeter Snipers':    'Jadin Booth',
}
scout_notes = {
    'Logan Duncomb': (
        "Winthrop's center is the 2nd most efficient scorer in the entire dataset "
        "despite only ranking 56th in PPG — a textbook hidden gem. He converts "
        "73.5% of his shots at the rim, attacks the free throw line relentlessly "
        "(0.79 FTA per FGA), and is virtually automatic from the line (72.4%). "
        "Limited 3-point range caps his ceiling, but as a high-efficiency big, "
        "he's severely underexposed at the mid-major level."
    ),
    'Cameron Boozer': (
        "The Duke forward is the rare player whose PPG rank (#5) and efficiency "
        "rank (#5) are in perfect agreement — what you see IS what you get. Boozer "
        "does everything: scores in the paint (58.2% FG), attacks the line, and "
        "stretches defenses with legitimate 3-point range (39.6%). At 22.6 PPG "
        "with elite True Shooting (67.4%), he's the prototype of a modern "
        "NBA-ready forward. The most 'complete' scorer in this dataset."
    ),
    'Jordan Riley': (
        "ECU's guard ranks 2nd nationally in PPG — but 299th in efficiency. "
        "He scores a lot because he shoots a lot (37.8 min, 19.7 FGA per game), "
        "not because he shoots well (42.7% FG, 50.5% TS%). His low FTA rate "
        "signals he rarely attacks the rim, preferring contested mid-range shots. "
        "His AST/TO ratio is below average for a ball-handler. The raw numbers "
        "look like a star — the efficiency numbers tell a different story."
    ),
    'Jadin Booth': (
        "Samford's guard epitomizes the Perimeter Sniper: 65.9% of his attempts "
        "come from three, he converts them at 42.9%, and his 87.2% FT% confirms "
        "elite mechanics. He's not a rim attacker — just 3.5 rebounds per game "
        "and a low FTA rate — but in the right system he's an elite spacing "
        "weapon. His True Shooting (64.9%) ranks among the top 15% of all "
        "scorers in the dataset. A legitimate sleeper."
    ),
}

archetype_order = ['Paint Dominators','Versatile Playmakers','Shot Creators','Perimeter Snipers']

# ══════════════════════════════════════════════════════════════════════════════
# VISUAL 1 — PLAYER REPORT CARDS (2×2 grid, one per archetype)
# ══════════════════════════════════════════════════════════════════════════════
print("Building Visual 1: Player Report Cards...")

fig = plt.figure(figsize=(20, 22))
fig.patch.set_facecolor(BG)
fig.suptitle('Player Report Cards — One Star Per Scoring Archetype\nESPN Top 500 Scorers  |  2025-26 NCAA Season',
             fontsize=16, fontweight='bold', color=TEXT, y=0.98)

outer = gridspec.GridSpec(2, 2, figure=fig, hspace=0.38, wspace=0.12)

for card_idx, archetype in enumerate(archetype_order):
    player_name = subjects[archetype]
    row_data    = df[df['Name']==player_name].iloc[0]
    color       = ARCHETYPE_COLORS[archetype]

    # Each card: left=stats panel, right=radar
    inner = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=outer[card_idx//2, card_idx%2],
                                              width_ratios=[1.2, 1], wspace=0.05)
    ax_stats = fig.add_subplot(inner[0])
    ax_radar  = fig.add_subplot(inner[1], polar=True)
    ax_radar.set_facecolor(PANEL)

    # ── Stats panel background ────────────────────────────────────────────────
    ax_stats.set_facecolor(BG)
    ax_stats.set_xlim(0,1); ax_stats.set_ylim(0,1)
    ax_stats.axis('off')

    # Colored accent bar along left edge
    ax_stats.add_patch(FancyBboxPatch((0,0),0.04,1, boxstyle='square,pad=0',
                                       facecolor=color, alpha=0.85, transform=ax_stats.transAxes,
                                       clip_on=False))

    # Archetype badge
    ax_stats.text(0.08, 0.96, archetype.upper(), fontsize=8, color=color,
                  fontweight='bold', va='top', alpha=0.9,
                  transform=ax_stats.transAxes)

    # Player name
    name_parts = player_name.split()
    ax_stats.text(0.08, 0.88, player_name, fontsize=15, color=TEXT,
                  fontweight='bold', va='top', transform=ax_stats.transAxes)

    # College + position
    info_str = f"{row_data['College']}  ·  {row_data['Position']}  ·  {int(row_data['GP'])} GP"
    ax_stats.text(0.08, 0.80, info_str, fontsize=9, color=MUTED,
                  va='top', transform=ax_stats.transAxes)

    # Separator line
    ax_stats.axhline(0.76, xmin=0.06, xmax=0.96, color=GRID, linewidth=0.8)

    # Big 3 headline stats
    big_stats = [
        (f"{row_data['PTS']}", 'PPG', f"Rank #{row_data['PPG_Rank']}"),
        (f"{row_data['TS_pct']*100:.1f}%", 'True Shooting', f"Eff Rank #{row_data['Eff_Rank']}"),
        (f"{row_data['REB']}", 'RPG', ''),
    ]
    for i, (val, lbl, sub) in enumerate(big_stats):
        x = 0.08 + i * 0.31
        ax_stats.text(x, 0.73, val, fontsize=18, color=color, fontweight='bold',
                      va='top', transform=ax_stats.transAxes)
        ax_stats.text(x, 0.63, lbl, fontsize=8, color=MUTED, va='top',
                      transform=ax_stats.transAxes)
        if sub:
            ax_stats.text(x, 0.57, sub, fontsize=7.5, color=TEXT, va='top',
                          transform=ax_stats.transAxes, alpha=0.7)

    ax_stats.axhline(0.53, xmin=0.06, xmax=0.96, color=GRID, linewidth=0.8)

    # Detailed stat grid
    detail_stats = [
        ('FG%',    f"{row_data['FGPct']:.1f}%"),
        ('3P%',    f"{row_data['3PPct']:.1f}%"),
        ('FT%',    f"{row_data['FTPct']:.1f}%"),
        ('APG',    f"{row_data['AST']:.1f}"),
        ('SPG',    f"{row_data['STL']:.1f}"),
        ('MIN',    f"{row_data['MIN']:.1f}"),
        ('3PA Rate', f"{row_data['3PA_rate']*100:.0f}%"),
        ('FTA Rate', f"{row_data['FTA_rate']*100:.0f}%"),
        ('AST/TO',   f"{row_data['AST_TO']:.2f}"),
    ]
    for i, (lbl, val) in enumerate(detail_stats):
        col_x = 0.08 + (i % 3) * 0.31
        row_y = 0.50 - (i // 3) * 0.095
        ax_stats.text(col_x, row_y,     lbl, fontsize=7.5, color=MUTED, va='top', transform=ax_stats.transAxes)
        ax_stats.text(col_x, row_y-0.04, val, fontsize=10,  color=TEXT,  va='top', fontweight='bold',
                      transform=ax_stats.transAxes)

    ax_stats.axhline(0.21, xmin=0.06, xmax=0.96, color=GRID, linewidth=0.8)

    # Rank delta badge
    delta = row_data['Rank_Delta']
    delta_color = '#3FB950' if delta > 10 else ('#FF7B72' if delta < -10 else MUTED)
    delta_label = f"▲ +{delta} efficiency vs PPG rank" if delta > 0 else (
                  f"▼ {delta} efficiency vs PPG rank" if delta < 0 else "≈ PPG rank matches efficiency")
    ax_stats.text(0.08, 0.19, delta_label, fontsize=8.5, color=delta_color,
                  fontweight='bold', va='top', transform=ax_stats.transAxes)

    # Scout note
    note = scout_notes[player_name]
    # Word-wrap manually to ~55 chars per line
    words = note.split()
    lines = []; cur = ''
    for w in words:
        if len(cur)+len(w)+1 <= 55: cur += (' ' if cur else '') + w
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    note_wrapped = '\n'.join(lines[:5])  # max 5 lines
    ax_stats.text(0.08, 0.14, note_wrapped, fontsize=7.2, color=MUTED,
                  va='top', transform=ax_stats.transAxes, linespacing=1.5,
                  style='italic')

    # ── Radar ─────────────────────────────────────────────────────────────────
    player_norm = [row_data[c+'_norm'] for c in radar_features]
    arch_norm   = archetype_means_norm.loc[archetype, [c+'_norm' for c in radar_features]].tolist()
    draw_radar(ax_radar, player_norm, arch_norm, color, radar_labels)

    # Radar subtitle
    ax_radar.set_title(f'vs. {archetype}\navg (dashed)', color=MUTED, fontsize=8,
                        pad=12, style='italic')

plt.savefig('final_player_report_cards.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  ✓ final_player_report_cards.png")


# ══════════════════════════════════════════════════════════════════════════════
# VISUAL 2 — EFFICIENCY-ADJUSTED TOP 10 LEADERBOARD
# ══════════════════════════════════════════════════════════════════════════════
print("Building Visual 2: Efficiency-Adjusted Top 10 Leaderboard...")

ppg_top10  = df.nlargest(10,'PTS')[['Name','College','PTS','Eff_Rank','PPG_Rank','Archetype','Efficiency_Score','TS_pct']].reset_index(drop=True)
eff_top10  = df.nsmallest(10,'Eff_Rank')[['Name','College','PTS','Eff_Rank','PPG_Rank','Archetype','Efficiency_Score','TS_pct']].sort_values('Eff_Rank').reset_index(drop=True)

fig, axes = plt.subplots(1, 2, figsize=(20, 10))
fig.patch.set_facecolor(BG)
fig.suptitle('ESPN PPG Ranking vs. Efficiency-Adjusted Ranking\n"If scoring titles rewarded quality over volume, this is who leads the country"',
             fontsize=14, fontweight='bold', color=TEXT, y=1.02)

def draw_leaderboard(ax, data, title, rank_col, score_col, score_label, title_color):
    ax.set_facecolor(BG)
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')

    # Header
    ax.text(0.5, 0.97, title, fontsize=13, color=title_color, fontweight='bold',
            ha='center', va='top', transform=ax.transAxes)
    ax.plot([0,1],[0.93,0.93], color=GRID, linewidth=1.2, transform=ax.transAxes, clip_on=False)

    # Column headers
    headers = ['RANK', 'PLAYER', 'SCHOOL', 'ARCH.', 'PPG', score_label, 'TS%']
    col_x   = [0.04, 0.13, 0.38, 0.54, 0.67, 0.78, 0.90]
    for hdr, cx in zip(headers, col_x):
        ax.text(cx, 0.91, hdr, fontsize=7.5, color=MUTED, fontweight='bold',
                va='top', transform=ax.transAxes)

    row_h = 0.079
    for i, (_, row) in enumerate(data.iterrows()):
        y = 0.88 - i * row_h
        arch_color = ARCHETYPE_COLORS.get(row['Archetype'], MUTED)

        # Alternating row bg
        if i % 2 == 0:
            ax.add_patch(FancyBboxPatch((0.02, y-0.055), 0.96, 0.068,
                                         boxstyle='round,pad=0.005',
                                         facecolor=PANEL, alpha=0.6, zorder=0))

        # Rank number with color glow for top 3
        rank_val  = int(row[rank_col])
        rank_color = ['#FFD700','#C0C0C0','#CD7F32'][i] if i < 3 else MUTED
        ax.text(col_x[0], y, f"#{rank_val}", fontsize=11, color=rank_color,
                fontweight='bold', va='center', transform=ax.transAxes)

        # Player name
        fname = row['Name'].split()[0][0] + '. ' + ' '.join(row['Name'].split()[1:])
        ax.text(col_x[1], y, fname, fontsize=9.5, color=TEXT, fontweight='bold',
                va='center', transform=ax.transAxes)

        # School
        ax.text(col_x[2], y, row['College'], fontsize=8.5, color=MUTED,
                va='center', transform=ax.transAxes)

        # Archetype badge
        arch_short = {'Paint Dominators':'PAINT','Shot Creators':'CREATOR',
                      'Versatile Playmakers':'VERSITLE','Perimeter Snipers':'SNIPER'}
        ax.text(col_x[3], y, arch_short.get(row['Archetype'],'—'), fontsize=7.5,
                color=arch_color, fontweight='bold', va='center', transform=ax.transAxes)

        # PPG
        ax.text(col_x[4], y, f"{row['PTS']:.1f}", fontsize=10, color=TEXT,
                va='center', transform=ax.transAxes, fontweight='bold')

        # Score
        score_val = row[score_col]
        if score_label == 'EFF RANK':
            ax.text(col_x[5], y, f"#{int(score_val)}", fontsize=10, color=arch_color,
                    va='center', transform=ax.transAxes, fontweight='bold')
        else:
            ax.text(col_x[5], y, f"{score_val:.2f}", fontsize=10, color=arch_color,
                    va='center', transform=ax.transAxes, fontweight='bold')

        # TS%
        ts_color = '#3FB950' if row['TS_pct'] > 0.61 else (MUTED if row['TS_pct'] > 0.55 else '#FF7B72')
        ax.text(col_x[6], y, f"{row['TS_pct']*100:.1f}%", fontsize=9.5,
                color=ts_color, va='center', transform=ax.transAxes, fontweight='bold')

    ax.plot([0,1],[0.07,0.07], color=GRID, linewidth=0.8, transform=ax.transAxes, clip_on=False)
    ax.text(0.5, 0.04, f'Data: ESPN 2025-26  |  {score_label} = composite of TS%, PPM, FTA rate, AST/TO',
            fontsize=7.5, color=MUTED, ha='center', transform=ax.transAxes)

draw_leaderboard(axes[0], ppg_top10,
                 '📊 ESPN PPG Ranking — Top 10', 'PPG_Rank', 'Eff_Rank', 'EFF RANK', '#F0883E')
draw_leaderboard(axes[1], eff_top10,
                 '⚡ Efficiency-Adjusted Ranking — Top 10', 'Eff_Rank', 'Efficiency_Score', 'EFF SCORE', '#3FB950')

# Annotation arrow between panels highlighting the biggest mover
fig.text(0.5, 0.5, '→', fontsize=40, color=MUTED, ha='center', va='center', alpha=0.4)

plt.tight_layout()
plt.savefig('final_leaderboard.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  ✓ final_leaderboard.png")


# ══════════════════════════════════════════════════════════════════════════════
# VISUAL 3 — ARCHETYPE × EFFICIENCY CONNECTOR
# ══════════════════════════════════════════════════════════════════════════════
print("Building Visual 3: Archetype × Efficiency connector...")

fig, axes = plt.subplots(1, 2, figsize=(18, 8))
fig.patch.set_facecolor(BG)
fig.suptitle('Which Scoring Archetype Produces the Most Efficient Scorers?\nProject 1 × Project 2 — Connecting Archetypes to Efficiency',
             fontsize=14, fontweight='bold', color=TEXT, y=1.02)

# Left: violin/box plot of efficiency scores per archetype
ax = axes[0]
arch_data   = [df[df['Archetype']==a]['Efficiency_Score'].values for a in archetype_order]
arch_colors = [ARCHETYPE_COLORS[a] for a in archetype_order]

# Violin
vp = ax.violinplot(arch_data, positions=range(4), widths=0.65,
                   showmedians=True, showextrema=False)
for body, color in zip(vp['bodies'], arch_colors):
    body.set_facecolor(color); body.set_alpha(0.35); body.set_edgecolor(color)
vp['cmedians'].set_colors(arch_colors); vp['cmedians'].set_linewidth(2.5)

# Overlay scatter (jittered)
for i, (data, color) in enumerate(zip(arch_data, arch_colors)):
    jitter = np.random.default_rng(42).uniform(-0.18, 0.18, len(data))
    ax.scatter(i + jitter, data, color=color, s=12, alpha=0.35, edgecolors='none', zorder=3)

# Mean dot
for i, (data, color) in enumerate(zip(arch_data, arch_colors)):
    ax.scatter(i, np.mean(data), color='white', s=80, zorder=5, edgecolors=color, linewidths=2)

ax.axhline(0, color=MUTED, linewidth=0.8, linestyle='--', alpha=0.5)
ax.set_xticks(range(4))
ax.set_xticklabels([a.replace(' ','\n') for a in archetype_order], fontsize=10, color=TEXT)
ax.set_ylabel('Composite Efficiency Score', color=MUTED, fontsize=10)
ax.set_title('Efficiency Score Distribution per Archetype\n(○ = mean, line = median, dots = individual players)',
             color=TEXT, fontsize=11, pad=10)
ax.grid(True, alpha=0.25, axis='y')

# Right: stacked bar showing % of archetype in each efficiency tier
bins    = [-3, -0.5, 0, 0.5, 1.0, 3]
labels  = ['Very Low\n(<−0.5)', 'Below Avg\n(−0.5–0)', 'Above Avg\n(0–0.5)', 'High\n(0.5–1.0)', 'Elite\n(>1.0)']
tier_colors = ['#FF7B72','#F0883E','#8B949E','#58A6FF','#3FB950']

ax = axes[1]
bar_width = 0.6
bottoms = np.zeros(4)
tier_data = []
for b_lo, b_hi, tlbl, tcol in zip(bins[:-1], bins[1:], labels, tier_colors):
    pcts = []
    for arch in archetype_order:
        sub = df[df['Archetype']==arch]['Efficiency_Score']
        pct = ((sub >= b_lo) & (sub < b_hi)).mean() * 100
        pcts.append(pct)
    tier_data.append((pcts, tlbl, tcol))

for pcts, tlbl, tcol in tier_data:
    bars = ax.bar(range(4), pcts, bar_width, bottom=bottoms,
                  color=tcol, alpha=0.85, edgecolor=BG, linewidth=0.6, label=tlbl)
    # Label segments > 12%
    for i, (pct, bot) in enumerate(zip(pcts, bottoms)):
        if pct > 12:
            ax.text(i, bot + pct/2, f'{pct:.0f}%', ha='center', va='center',
                    fontsize=8, color='white', fontweight='bold')
    bottoms += np.array(pcts)

ax.set_xticks(range(4))
ax.set_xticklabels([a.replace(' ','\n') for a in archetype_order], fontsize=10, color=TEXT)
ax.set_ylabel('% of Archetype Players', color=MUTED, fontsize=10)
ax.set_title('Efficiency Tier Breakdown by Archetype\n(What % of each archetype lands in each tier?)',
             color=TEXT, fontsize=11, pad=10)
ax.legend(facecolor=PANEL, edgecolor=GRID, labelcolor=TEXT, fontsize=8.5,
          loc='lower right', title='Efficiency Tier', title_fontsize=8)
ax.grid(True, alpha=0.2, axis='y')
ax.set_ylim(0, 105)

plt.tight_layout()
plt.savefig('final_archetype_efficiency_connector.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  ✓ final_archetype_efficiency_connector.png")


# ══════════════════════════════════════════════════════════════════════════════
# VISUAL 4 — HEADLINE CASE STUDY: Fake Stars vs Hidden Gems
# ══════════════════════════════════════════════════════════════════════════════
print("Building Visual 4: Headline Case Study...")

case_fake = df[df['Name'].isin(['Jordan Riley','Michael James','Tai\'Reon Joseph','Skylar Wicks','Erik Pratt'])]
case_gems = df[df['Name'].isin(['Cameron Boozer','Logan Duncomb','Roman Domon','Terrence Hill Jr.','Darius Acuff Jr.'])]

fig = plt.figure(figsize=(20, 13))
fig.patch.set_facecolor(BG)
fig.suptitle('"The Box Score Lies" — Fake Stars vs. Hidden Gems\nWho is the country actually overrating and underrating?',
             fontsize=15, fontweight='bold', color=TEXT, y=1.01)

gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.3)

# ── Top panel: scatter with case study players highlighted ───────────────────
ax_scatter = fig.add_subplot(gs[0, :])
# Background players (grey)
ax_scatter.scatter(df['PTS'], df['Efficiency_Score'], c=GRID, s=25, alpha=0.4,
                   edgecolors='none', zorder=2, label='All 500 players')

# Fake stars
ax_scatter.scatter(case_fake['PTS'], case_fake['Efficiency_Score'],
                   c='#FF7B72', s=120, alpha=0.95, edgecolors='white',
                   linewidths=1.2, zorder=4, label='"Fake Stars"')
# Hidden gems
ax_scatter.scatter(case_gems['PTS'], case_gems['Efficiency_Score'],
                   c='#3FB950', s=120, alpha=0.95, edgecolors='white',
                   linewidths=1.2, zorder=4, label='"Hidden Gems" / Truly Elite')

# Annotate
for _, row in pd.concat([case_fake, case_gems]).iterrows():
    fname = row['Name'].split()[0][0] + '. ' + row['Name'].split()[-1]
    is_fake = row['Name'] in case_fake['Name'].values
    color   = '#FF7B72' if is_fake else '#3FB950'
    offset  = (-75, -12) if is_fake else (8, 4)
    ax_scatter.annotate(fname, (row['PTS'], row['Efficiency_Score']),
                        fontsize=8.5, color=color, fontweight='bold',
                        xytext=offset, textcoords='offset points',
                        arrowprops=dict(arrowstyle='-',color=color,lw=0.8,alpha=0.6))

# Median lines
ax_scatter.axvline(df['PTS'].median(), color=MUTED, linestyle='--', alpha=0.4, linewidth=1)
ax_scatter.axhline(df['Efficiency_Score'].median(), color=MUTED, linestyle='--', alpha=0.4, linewidth=1)
ax_scatter.set_xlabel('Points Per Game', color=MUTED, fontsize=10)
ax_scatter.set_ylabel('Composite Efficiency Score', color=MUTED, fontsize=10)
ax_scatter.set_title('PPG vs. Efficiency — 500 Scorers Plotted  |  Highlighted: This Year\'s Biggest Gaps',
                     color=TEXT, fontsize=11, pad=10)
ax_scatter.legend(facecolor=PANEL, edgecolor=GRID, labelcolor=TEXT, fontsize=9)
ax_scatter.grid(True, alpha=0.2)

# ── Bottom row: individual stat profiles for 3 most compelling cases ─────────
spotlight = [
    ('Jordan Riley', 'ECU', '#FF7B72', '"The Volume Mirage"\n#2 PPG nationally, #299 Efficiency'),
    ('Logan Duncomb', 'WIN', '#3FB950', '"The Hidden Giant"\n#56 PPG nationally, #2 Efficiency'),
    ('Cameron Boozer', 'DUKE', '#58A6FF', '"The Real Deal"\nPPG rank = Efficiency rank. Legit star.'),
]
stat_pairs = [('PPG','PTS'),('FG%','FGPct'),('TS%','TS_pct'),('FTA/G','FTA'),('AST/TO','AST_TO')]

for col_i, (name, school, color, subtitle) in enumerate(spotlight):
    ax = fig.add_subplot(gs[1, col_i])
    ax.set_facecolor(BG); ax.axis('off')
    ax.set_xlim(0,1); ax.set_ylim(0,1)

    row = df[df['Name']==name].iloc[0]

    # Card header
    ax.add_patch(FancyBboxPatch((0,0.88),1,0.12,boxstyle='round,pad=0',
                                 facecolor=color,alpha=0.2,transform=ax.transAxes,clip_on=True))
    ax.text(0.5,0.97, name, fontsize=12, color=color, fontweight='bold',
            ha='center', va='top', transform=ax.transAxes)
    ax.text(0.5,0.90, subtitle, fontsize=8, color=TEXT, ha='center', va='top',
            transform=ax.transAxes, style='italic', alpha=0.85)

    ax.plot([0,1],[0.87,0.87], color=GRID, linewidth=0.8, transform=ax.transAxes, clip_on=False)

    # Rank comparison
    ppg_r = int(row['PPG_Rank']); eff_r = int(row['Eff_Rank'])
    delta = row['Rank_Delta']
    ax.text(0.25, 0.82, f"#{ppg_r}", fontsize=22, color='#F0883E', fontweight='bold',
            ha='center', va='top', transform=ax.transAxes)
    ax.text(0.25, 0.71, 'PPG Rank', fontsize=8, color=MUTED, ha='center',
            va='top', transform=ax.transAxes)
    ax.text(0.5, 0.77, '→', fontsize=20, color=MUTED, ha='center', va='top',
            transform=ax.transAxes, alpha=0.5)
    eff_color = '#3FB950' if delta > 0 else '#FF7B72'
    ax.text(0.75, 0.82, f"#{eff_r}", fontsize=22, color=eff_color, fontweight='bold',
            ha='center', va='top', transform=ax.transAxes)
    ax.text(0.75, 0.71, 'Eff. Rank', fontsize=8, color=MUTED, ha='center',
            va='top', transform=ax.transAxes)

    delta_str = f"{'▲ +' if delta>0 else '▼ '}{abs(delta)} rank spots"
    ax.text(0.5, 0.65, delta_str, fontsize=9, color=eff_color, ha='center',
            va='top', transform=ax.transAxes, fontweight='bold')

    ax.plot([0,1],[0.62,0.62], color=GRID, linewidth=0.8, transform=ax.transAxes, clip_on=False)

    # Key stats
    disp_stats = [
        ('PPG',    f"{row['PTS']:.1f}"),
        ('FG%',    f"{row['FGPct']:.1f}%"),
        ('TS%',    f"{row['TS_pct']*100:.1f}%"),
        ('FTA/G',  f"{row['FTA']:.1f}"),
        ('AST/TO', f"{row['AST_TO']:.2f}"),
        ('MIN',    f"{row['MIN']:.1f}"),
    ]
    for stat_i, (lbl, val) in enumerate(disp_stats):
        xi = 0.08 + (stat_i % 3) * 0.32
        yi = 0.58 - (stat_i // 3) * 0.14
        ax.text(xi, yi,       lbl, fontsize=7.5, color=MUTED, va='top', transform=ax.transAxes)
        ax.text(xi, yi-0.055, val, fontsize=10, color=color, fontweight='bold',
                va='top', transform=ax.transAxes)

    # Archetype badge
    ax.text(0.5, 0.22, df[df['Name']==name]['Archetype'].values[0],
            fontsize=8, color=color, ha='center', va='top', transform=ax.transAxes,
            fontweight='bold', alpha=0.8)

plt.savefig('final_case_study.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  ✓ final_case_study.png")

print("\n✓ All 4 final visuals complete.")
