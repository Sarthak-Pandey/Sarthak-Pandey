from pathlib import Path
from typing import Any, Dict, List
from ..stats import GitHubStats

LEVELS = [
    "#161b22",  # Level 0 – no contributions
    "#0e4429",  # Level 1
    "#006d32",  # Level 2
    "#26a641",  # Level 3
    "#39d353",  # Level 4
]

# Glow colours matching contribution level
GLOW_COLORS = [
    "none",
    "#0e442944",
    "#006d3244",
    "#26a64166",
    "#39d35388",
]

CELL = 13
GAP = 3
MARGIN_X = 55
MARGIN_Y = 70
MONTH_LABELS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]
DAY_LABELS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


def render_graph_svg(
    days: List[Dict[str, Any]],
    stats: GitHubStats,
    output_path: Path | str = "graph.svg"
) -> str:
    weeks_count = 53
    grid_w = weeks_count * (CELL + GAP)
    width = MARGIN_X + grid_w + 40
    height = MARGIN_Y + 7 * (CELL + GAP) + 90

    svg: list[str] = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
    )

    # ── Definitions ──
    svg.append("""  <defs>
    <filter id="cellGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="headerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#58a6ff"/>
      <stop offset="100%" stop-color="#d2a8ff"/>
    </linearGradient>
    <linearGradient id="statBadgeGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#7ee787"/>
      <stop offset="100%" stop-color="#39d353"/>
    </linearGradient>
    <!-- Scanline overlay -->
    <pattern id="scanlines" patternUnits="userSpaceOnUse" width="4" height="4">
      <line x1="0" y1="0" x2="4" y2="0" stroke="#ffffff" stroke-opacity="0.012" stroke-width="1"/>
    </pattern>
  </defs>""")

    svg.append("""  <style>
    .mono { font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Courier New', monospace; }
    @keyframes waveIn { from { opacity: 0; transform: scale(0.5); } to { opacity: 1; transform: scale(1); } }
    @keyframes borderPulse {
      0%,100% { stroke-opacity: 0.1; }
      50% { stroke-opacity: 0.25; }
    }
  </style>""")

    # ── Background ──
    svg.append(f'  <rect width="100%" height="100%" rx="12" fill="#0d1117"/>')
    svg.append(f'  <rect width="100%" height="100%" rx="12" fill="none" stroke="#58a6ff" stroke-width="1" stroke-opacity="0.1" style="animation: borderPulse 5s ease-in-out infinite;"/>')
    svg.append(f'  <rect width="100%" height="100%" rx="12" fill="url(#scanlines)"/>')

    # ── Header Bar ──
    svg.append(f'  <text x="{MARGIN_X}" y="30" class="mono" font-size="15" font-weight="bold" fill="url(#headerGrad)">$ cat contributions.log</text>')

    # Stats badges (pill-shaped)
    badges = [
        (f"Total: {stats.total_contributions}", "#7ee787"),
        (f"Streak: {stats.current_streak}d", "#58a6ff"),
        (f"Max: {stats.longest_streak}d", "#d2a8ff"),
        (f"Heat: {stats.heat_score_display}", "#ffa657"),
    ]
    bx = width - 35
    for badge_text, badge_color in reversed(badges):
        tw = len(badge_text) * 7.5 + 16
        bx -= tw + 6
        svg.append(
            f'  <rect x="{bx}" y="17" width="{tw}" height="20" rx="10" '
            f'fill="{badge_color}" fill-opacity="0.08" '
            f'stroke="{badge_color}" stroke-width="0.6" stroke-opacity="0.4"/>'
        )
        svg.append(
            f'  <text x="{bx + tw / 2}" y="31" class="mono" font-size="10" '
            f'fill="{badge_color}" text-anchor="middle">{badge_text}</text>'
        )

    svg.append(f'  <rect x="20" y="45" width="{width - 40}" height="1" fill="#30363d" opacity="0.6"/>')

    # ── Day labels (left side) ──
    for i, label in enumerate(DAY_LABELS):
        if i % 2 == 1:  # show Mon, Wed, Fri
            dy = MARGIN_Y + i * (CELL + GAP) + CELL // 2 + 4
            svg.append(f'  <text x="{MARGIN_X - 8}" y="{dy}" class="mono" font-size="9" fill="#484f58" text-anchor="end">{label}</text>')

    # ── Month labels (top) ──
    if days:
        last_month = -1
        for index in range(0, min(len(days), 53 * 7), 7):
            date_str = days[index].get("date", "")
            if date_str:
                try:
                    month = int(date_str.split("-")[1])
                    if month != last_month:
                        week = index // 7
                        mx = MARGIN_X + week * (CELL + GAP)
                        svg.append(
                            f'  <text x="{mx}" y="{MARGIN_Y - 8}" class="mono" font-size="9" fill="#484f58">'
                            f'{MONTH_LABELS[month - 1]}</text>'
                        )
                        last_month = month
                except (IndexError, ValueError):
                    pass

    # ── Heatmap Grid with wave animation ──
    total_cells = min(len(days), 53 * 7)
    for index in range(total_cells):
        day = days[index]
        week = index // 7
        weekday = index % 7

        x = MARGIN_X + week * (CELL + GAP)
        cell_y = MARGIN_Y + weekday * (CELL + GAP)

        level = min(max(int(day.get("level", 0)), 0), 4)
        color = LEVELS[level]
        date = day.get("date", "")
        count = day.get("count", 0)

        # Wave-in animation delay: column by column, top to bottom
        delay = round(0.3 + week * 0.03 + weekday * 0.005, 3)

        attrs = (
            f'x="{x}" y="{cell_y}" width="{CELL}" height="{CELL}" rx="2" fill="{color}"'
        )

        if level >= 3:
            # Active cells get a subtle glow
            svg.append(
                f'  <g opacity="0" style="animation: waveIn 0.2s {delay}s both;">'
                f'<rect {attrs} filter="url(#cellGlow)"/>'
                f'<title>{date}: {count} contributions</title></g>'
            )
        else:
            svg.append(
                f'  <g opacity="0" style="animation: waveIn 0.15s {delay}s both;">'
                f'<rect {attrs}/><title>{date}: {count} contributions</title></g>'
            )

    # ── Legend ──
    legend_y = height - 30
    lx = MARGIN_X

    svg.append(f'  <text x="{lx}" y="{legend_y}" class="mono" font-size="10" fill="#484f58">Less</text>')
    lx += 35
    for i, color in enumerate(LEVELS):
        svg.append(f'  <rect x="{lx}" y="{legend_y - 10}" width="12" height="12" rx="2" fill="{color}"/>')
        lx += 17
    svg.append(f'  <text x="{lx + 3}" y="{legend_y}" class="mono" font-size="10" fill="#484f58">More</text>')

    # ── Footer stats row ──
    footer_y = height - 12
    svg.append(
        f'  <text x="{MARGIN_X}" y="{footer_y}" class="mono" font-size="10" fill="#484f58">'
        f'Repos: {stats.public_repos} · Followers: {stats.followers} · Following: {stats.following}'
        f' · Avg: {stats.average_commits_per_active_day}/day · Peak: {stats.most_active_day}'
        f'</text>'
    )

    svg.append('</svg>')

    content = "\n".join(svg)
    out_file = Path(output_path)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated graph SVG -> {out_file.resolve()}")
    return content
