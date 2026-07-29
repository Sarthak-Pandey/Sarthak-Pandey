from pathlib import Path
from typing import Any, Dict, List
from ..stats import GitHubStats
from ..theme import ThemePalette, DARK_THEME, svg_defs


def render_graph_svg(
    days: List[Dict[str, Any]],
    stats: GitHubStats,
    theme: ThemePalette = DARK_THEME,
    output_path: Path | str = "graph.svg"
) -> str:
    # Colors for contribution levels based on the theme
    levels = [
        theme.bg_panel,            # Level 0 (No contributions)
        theme.accent_teal + "33",  # Level 1
        theme.accent_teal + "66",  # Level 2
        theme.accent_teal + "b3",  # Level 3
        theme.accent_teal,         # Level 4
    ]

    cell_size = 13
    gap = 3
    margin_x = 55
    margin_y = 70
    weeks_count = 53
    grid_w = weeks_count * (cell_size + gap)
    width = margin_x + grid_w + 40
    # Make height slightly taller to fit the new 30-day sparkline
    height = margin_y + 7 * (cell_size + gap) + 145

    svg: list[str] = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
    )

    # ── Definitions & Styles ──
    svg.append(svg_defs(theme))
    svg.append(f"""  <style>
    .mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Courier New', monospace; }}
    @keyframes waveIn {{ from {{ opacity: 0; transform: scale(0.5); }} to {{ opacity: 1; transform: scale(1); }} }}
    @keyframes borderPulse {{
      0%,100% {{ stroke-opacity: 0.1; }}
      50% {{ stroke-opacity: 0.25; }}
    }}
    .cell {{
      transform-box: fill-box;
      transform-origin: center;
      transition: transform 0.15s cubic-bezier(0.4, 0, 0.2, 1), fill 0.15s ease;
      cursor: pointer;
    }}
    .cell:hover {{
      transform: scale(1.4);
      fill: {theme.accent_cyan} !important;
    }}
    .sparkline-path {{
      stroke-dasharray: 400;
      stroke-dashoffset: 400;
      animation: drawSpark 2s ease-out 1s forwards;
    }}
    @keyframes drawSpark {{
      to {{ stroke-dashoffset: 0; }}
    }}
  </style>""")

    # ── Background ──
    svg.append(f'  <rect width="100%" height="100%" rx="12" fill="{theme.bg}"/>')
    svg.append(f'  <rect width="100%" height="100%" rx="12" fill="none" stroke="{theme.accent_blue}" stroke-width="1" stroke-opacity="0.1" style="animation: borderPulse 5s ease-in-out infinite;"/>')
    svg.append(f'  <rect width="100%" height="100%" rx="12" fill="url(#scanlines)" opacity="0.4"/>')

    # ── Header ──
    svg.append(f'  <text x="{margin_x}" y="30" class="mono" font-size="15" font-weight="bold" fill="url(#accentGrad)">$ cat contributions.log</text>')

    # Stats badges
    badges = [
        (f"Total: {stats.total_contributions}", theme.accent_green),
        (f"Streak: {stats.current_streak}d", theme.accent_blue),
        (f"Max: {stats.longest_streak}d", theme.accent_purple),
        (f"Heat: {stats.heat_score_display}", theme.accent_orange),
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

    svg.append(f'  <rect x="20" y="45" width="{width - 40}" height="1" fill="{theme.border}" opacity="0.6"/>')

    # ── Day Labels ──
    day_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for i, label in enumerate(day_labels):
        if i % 2 == 1:
            dy = margin_y + i * (cell_size + gap) + cell_size // 2 + 4
            svg.append(f'  <text x="{margin_x - 8}" y="{dy}" class="mono" font-size="9" fill="{theme.text_muted}" text-anchor="end">{label}</text>')

    # ── Month Labels ──
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    if days:
        last_month = -1
        for index in range(0, min(len(days), 53 * 7), 7):
            date_str = days[index].get("date", "")
            if date_str:
                try:
                    month = int(date_str.split("-")[1])
                    if month != last_month:
                        week = index // 7
                        mx = margin_x + week * (cell_size + gap)
                        svg.append(
                            f'  <text x="{mx}" y="{margin_y - 8}" class="mono" font-size="9" fill="{theme.text_muted}">'
                            f'{month_labels[month - 1]}</text>'
                        )
                        last_month = month
                except (IndexError, ValueError):
                    pass

    # ── Grid cells ──
    total_cells = min(len(days), 53 * 7)
    for index in range(total_cells):
        day = days[index]
        week = index // 7
        weekday = index % 7

        x = margin_x + week * (cell_size + gap)
        cell_y = margin_y + weekday * (cell_size + gap)

        level = min(max(int(day.get("level", 0)), 0), 4)
        color = levels[level]
        date = day.get("date", "")
        count = day.get("count", 0)

        delay = round(0.3 + week * 0.03 + weekday * 0.005, 3)
        attrs = f'x="{x}" y="{cell_y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}" class="cell"'

        if level >= 3:
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

    # ── 30-Day Activity Sparkline ──
    sparkline_top = margin_y + 7 * (cell_size + gap) + 30
    sparkline_height = 45
    spark_days = days[-30:] if len(days) >= 30 else days

    if spark_days:
        max_count = max(d.get("count", 0) for d in spark_days)
        if max_count == 0:
            max_count = 1

        points = []
        x_step = grid_w / max(1, len(spark_days) - 1)
        for i, d in enumerate(spark_days):
            cx = margin_x + i * x_step
            cy = sparkline_top + sparkline_height - (d.get("count", 0) / max_count) * sparkline_height
            points.append((cx, cy))

        # Polyline points string
        pts_str = " ".join(f"{px},{py}" for px, py in points)

        # Glow Area Gradient
        svg.append(f"""  <defs>
    <linearGradient id="sparkAreaGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{theme.accent_cyan}" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="{theme.accent_cyan}" stop-opacity="0.0"/>
    </linearGradient>
  </defs>""")

        # Draw filled area under sparkline
        area_pts = f"{margin_x},{sparkline_top + sparkline_height} {pts_str} {margin_x + (len(spark_days)-1)*x_step},{sparkline_top + sparkline_height}"
        svg.append(f'  <polygon points="{area_pts}" fill="url(#sparkAreaGrad)"/>')

        # Draw sparkline path
        svg.append(
            f'  <polyline points="{pts_str}" fill="none" stroke="{theme.accent_cyan}" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" class="sparkline-path"/>'
        )

        # Add data points with tooltips
        for px, py in points:
            svg.append(f'  <circle cx="{px}" cy="{py}" r="2" fill="{theme.accent_cyan}" opacity="0.8"/>')

        # Sparkline Label
        svg.append(
            f'  <text x="{margin_x}" y="{sparkline_top - 6}" class="mono" font-size="9" fill="{theme.text_muted}">'
            f'📈 30-Day Activity Sparkline (Max: {max_count} commits/day)'
            f'</text>'
        )

    # ── Legend ──
    legend_y = height - 30
    lx = margin_x

    svg.append(f'  <text x="{lx}" y="{legend_y}" class="mono" font-size="10" fill="{theme.text_muted}">Less</text>')
    lx += 35
    for color in levels:
        svg.append(f'  <rect x="{lx}" y="{legend_y - 10}" width="12" height="12" rx="2" fill="{color}"/>')
        lx += 17
    svg.append(f'  <text x="{lx + 3}" y="{legend_y}" class="mono" font-size="10" fill="{theme.text_muted}">More</text>')

    # ── Footer stats row ──
    footer_y = height - 12
    svg.append(
        f'  <text x="{margin_x}" y="{footer_y}" class="mono" font-size="10" fill="{theme.text_dim}">'
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
