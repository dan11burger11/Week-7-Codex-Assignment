"""Summarize Ames sale prices by total-bath count and draw the half-bath chart."""

import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).parent
DATA = ROOT / "AmesHousing_clean.csv"
SUMMARY = ROOT / "AmesHousing_bath_summary.csv"
CHANGES = ROOT / "AmesHousing_bath_price_changes.csv"
CHART = ROOT / "AmesHousing_bath_price_changes.svg"
VARS = ("SalePrice", "Total Bathrooms", "Bsmt Full Bath", "Bsmt Half Bath", "Full Bath", "Half Bath")

with DATA.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

stats_rows = []
for variable in VARS:
    values = [float(row[variable]) for row in rows]
    stats_rows.append({
        "Variable": variable,
        "N": len(values),
        "Mean": statistics.mean(values),
        "SD": statistics.stdev(values),
        "Median": statistics.median(values),
        "Min": min(values),
        "Max": max(values),
    })
with SUMMARY.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=stats_rows[0].keys())
    writer.writeheader()
    writer.writerows(stats_rows)

groups = defaultdict(list)
for row in rows:
    groups[float(row["Total Bathrooms"])].append(int(row["SalePrice"]))

levels = sorted(groups)
change_rows = []
for lower in levels:
    upper = lower + 0.5
    if upper not in groups:
        continue
    lower_mean = statistics.mean(groups[lower])
    upper_mean = statistics.mean(groups[upper])
    change_rows.append({
        "From Total Bathrooms": lower,
        "To Total Bathrooms": upper,
        "N at lower": len(groups[lower]),
        "N at upper": len(groups[upper]),
        "Mean SalePrice at lower": lower_mean,
        "Mean SalePrice at upper": upper_mean,
        "Mean Price Difference": upper_mean - lower_mean,
        "Mean Price Percent Change": 100 * (upper_mean - lower_mean) / lower_mean,
        "Median SalePrice at lower": statistics.median(groups[lower]),
        "Median SalePrice at upper": statistics.median(groups[upper]),
    })
with CHANGES.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=change_rows[0].keys())
    writer.writeheader()
    writer.writerows(change_rows)

# Standalone SVG bar chart of changes between adjacent half-bath groups.
width, height = 1000, 560
left, right, top, bottom = 90, 30, 60, 145
plot_h = height - top - bottom
max_pct = max(float(r["Mean Price Percent Change"]) for r in change_rows)
scale = plot_h / max_pct
bar_w = 72
gap = (width - left - right - bar_w * len(change_rows)) / (len(change_rows) - 1)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
       '<rect width="100%" height="100%" fill="white"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#222}.small{font-size:13px}.label{font-size:14px}.title{font-size:22px;font-weight:bold}.subtitle{font-size:14px;fill:#555}</style>',
       f'<text x="{left}" y="30" class="title">Mean sale price change between adjacent half-bath groups</text>',
       f'<text x="{left}" y="52" class="subtitle">Percent change in group mean; observational comparison, not an adjusted causal effect</text>']
for tick in range(0, math.ceil(max_pct / 10) * 10 + 1, 10):
    y = top + plot_h - tick * scale
    if y < top - 1:
        continue
    svg.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#ddd"/>')
    svg.append(f'<text x="{left-12}" y="{y+5:.1f}" text-anchor="end" class="small">{tick}%</text>')
for i, row in enumerate(change_rows):
    x = left + i * (bar_w + gap)
    pct = float(row["Mean Price Percent Change"])
    bar_h = pct * scale
    y = top + plot_h - bar_h
    svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w}" height="{bar_h:.1f}" rx="3" fill="#2b7bba"/>')
    svg.append(f'<text x="{x+bar_w/2:.1f}" y="{y-8:.1f}" text-anchor="middle" class="label">{pct:.1f}%</text>')
    svg.append(f'<text x="{x+bar_w/2:.1f}" y="{top+plot_h+24}" text-anchor="middle" class="small">{row["From Total Bathrooms"]:g}→{row["To Total Bathrooms"]:g}</text>')
    svg.append(f'<text x="{x+bar_w/2:.1f}" y="{top+plot_h+43}" text-anchor="middle" class="small">n={row["N at lower"]},{row["N at upper"]}</text>')
svg.extend([f'<text x="{left+(width-left-right)/2:.1f}" y="{height-48}" text-anchor="middle" class="label">Total bathrooms (lower → higher group); sample sizes shown below</text>', '</svg>'])
CHART.write_text("\n".join(svg), encoding="utf-8")

for row in change_rows:
    print(f'{row["From Total Bathrooms"]:g} to {row["To Total Bathrooms"]:g}: '
          f'{row["Mean Price Percent Change"]:.2f}% (${row["Mean Price Difference"]:,.0f}); '
          f'n={row["N at lower"]}/{row["N at upper"]}')
print(f"Wrote {SUMMARY.name}, {CHANGES.name}, and {CHART.name}")
