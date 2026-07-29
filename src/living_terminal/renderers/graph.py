from pathlib import Path
from typing import Any, Dict, List
from ..stats import GitHubStats

LEVELS = [
    "#161b22",  # Level 0 (No contributions)
    "#0e4429",  # Level 1
    "#006d32",  # Level 2
    "#26a641",  # Level 3
    "#39d353",  # Level 4 (Highest)
]

CELL = 12
GAP = 3
MARGIN_X = 30
MARGIN_Y = 65


def render_graph_svg(
    days: List[Dict[str, Any]],
    stats: GitHubStats,
    output_path: Path | str = "graph.svg"
) -> str:
    # 53 weeks max grid
    weeks_count = 53
    width = MARGIN_X * 2 + (weeks_count * (CELL + GAP))
    height = MARGIN_Y + (7 * (CELL + GAP)) + 65

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    svg.append("""
  <style>
    .font-mono { font-family: 'Fira Code', 'Courier New', Consolas, monospace; }
  </style>
""")

    # Background
    svg.append('  <rect width="100%" height="100%" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1"/>')

    # Title & Stats Badges Bar
    svg.append('  <text x="30" y="32" class="font-mono" font-size="16" font-weight="bold" fill="#58a6ff">GitHub Contributions</text>')
    svg.append(
        f'  <text x="{width - 30}" y="32" class="font-mono" font-size="13" text-anchor="end" fill="#7ee787">'
        f'Total: {stats.total_contributions} • Streak: {stats.current_streak}d (Max: {stats.longest_streak}d) • Heat Score: {stats.heat_score_display}'
        f'</text>'
    )

    svg.append(f'  <line x1="20" y1="45" x2="{width - 20}" y2="45" stroke="#30363d" stroke-width="1"/>')

    # Heatmap Grid
    for index, day in enumerate(days[: 53 * 7]):
        week = index // 7
        weekday = index % 7

        x = MARGIN_X + week * (CELL + GAP)
        y = MARGIN_Y + weekday * (CELL + GAP)

        level = min(max(int(day.get("level", 0)), 0), 4)
        color = LEVELS[level]
        date = day.get("date", "")
        count = day.get("count", 0)

        svg.append(
            f'  <rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{color}">'
            f'<title>{date}: {count} contributions</title>'
            f'</rect>'
        )

    # Legend at Bottom
    legend_y = height - 20
    legend_x = MARGIN_X

    svg.append(f'  <text x="{legend_x}" y="{legend_y - 2}" class="font-mono" font-size="11" fill="#8b949e">Less</text>')
    legend_x += 40

    for color in LEVELS:
        svg.append(f'  <rect x="{legend_x}" y="{legend_y - 12}" width="10" height="10" rx="2" fill="{color}"/>')
        legend_x += 15

    svg.append(f'  <text x="{legend_x + 5}" y="{legend_y - 2}" class="font-mono" font-size="11" fill="#8b949e">More</text>')

    svg.append('</svg>')

    content = "\n".join(svg)
    out_file = Path(output_path)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Generated graph SVG -> {out_file.resolve()}")
    return content
