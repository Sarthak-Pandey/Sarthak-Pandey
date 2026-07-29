from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple
from ..config import AppConfig
from ..theme import ThemePalette, DARK_THEME, get_category_color, esc, svg_defs, svg_styles


def wrap_text_to_cols(text: str, width: int) -> List[str]:
    words = text.split(" ")
    lines = []
    current_line = []
    current_len = 0
    for word in words:
        word_len = len(word)
        if current_len + word_len + (1 if current_line else 0) <= width:
            current_line.append(word)
            current_len += word_len + (1 if current_line else 0)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            current_len = word_len
    if current_line:
        lines.append(" ".join(current_line))
    return lines or [""]


def render_panel_svg(
    config: AppConfig,
    theme: ThemePalette = DARK_THEME,
    output_path: Path | str = "sysinfo.svg",
    current_time: str | None = None
) -> str:
    width = 860

    if current_time is None:
        current_time = datetime.now(timezone.utc).strftime("%H:%M UTC · %Y-%m-%d")

    svg: list[str] = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="__SVG_HEIGHT__" '
        f'viewBox="0 0 {width} __SVG_HEIGHT__">'
    )

    # ── Definitions & Styles ──
    svg.append(svg_defs(theme))
    svg.append(svg_styles(theme))

    # ── Background ──
    svg.append(f'  <rect width="100%" height="100%" rx="14" fill="{theme.bg}"/>')
    svg.append(f'  <rect width="100%" height="100%" rx="14" fill="none" stroke="{theme.accent_blue}" stroke-width="1" stroke-opacity="0.12" style="animation: borderGlow 6s ease-in-out infinite;"/>')
    svg.append(f'  <rect width="100%" height="100%" rx="14" fill="url(#scanlines)" style="animation: scanPulse 4s ease-in-out infinite;"/>')

    # ── Title Bar ──
    svg.append(f'  <rect x="0" y="0" width="{width}" height="44" rx="14" fill="url(#barGrad)"/>')
    svg.append(f'  <rect x="0" y="30" width="{width}" height="14" fill="url(#barGrad)"/>')

    # macOS window dots
    for cx, color in [(24, "#ff5f57"), (46, "#febc2e"), (68, "#28c840")]:
        svg.append(f'  <circle cx="{cx}" cy="22" r="6.5" fill="{color}" opacity="0.9"/>')
        svg.append(f'  <circle cx="{cx}" cy="22" r="6.5" fill="none" stroke="#000" stroke-opacity="0.15" stroke-width="0.5"/>')

    # Title bar text & live clock
    svg.append(
        f'  <text x="95" y="27" class="mono" font-size="13" fill="{theme.text_muted}" letter-spacing="0.5">'
        f'{esc(config.developer.github_username)}@ai-terminal:~$ '
        f'<tspan fill="{theme.accent_green}">living-terminal</tspan>'
        f' <tspan fill="{theme.text_muted}">--init</tspan>'
        f'</text>'
    )
    svg.append(
        f'  <text x="{width - 25}" y="27" class="mono" font-size="11" fill="{theme.text_muted}" text-anchor="end">'
        f'🕐 {esc(current_time)}'
        f'</text>'
    )
    svg.append(f'  <line x1="0" y1="44" x2="{width}" y2="44" stroke="{theme.border}" stroke-width="1"/>')

    y = 68

    # ── 1. Boot Sequence ──
    boot_seq = config.boot_sequence or []
    t = 0.2
    for line in boot_seq:
        is_ready = "ready" in line.lower()
        color = theme.accent_green if is_ready else theme.text_dim
        icon = "✓" if is_ready else "›"
        svg.append(
            f'  <g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.25s" begin="{t:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="-10 0" to="0 0" dur="0.25s" begin="{t:.2f}s" fill="freeze"/>'
            f'<text x="28" y="{y}" class="mono" font-size="11" fill="{color}">'
            f'<tspan fill="{theme.accent_green if is_ready else theme.text_muted}">{icon}</tspan> {esc(line)}'
            f'</text></g>'
        )
        y += 18
        t += 0.1

    y += 8
    t += 0.2

    # ── 2. Welcome Banner ──
    banner_h = 130
    banner_x = 25
    banner_w = width - 50

    svg.append(
        f'  <g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{t:.2f}s" fill="freeze"/>'
    )
    svg.append(
        f'    <rect x="{banner_x}" y="{y}" width="{banner_w}" height="{banner_h}" rx="8" '
        f'fill="{theme.bg_panel}" stroke="{theme.accent_blue}" stroke-width="0.6" stroke-opacity="0.3"/>'
    )
    svg.append(
        f'    <rect x="{banner_x}" y="{y}" width="{banner_w}" height="2" rx="1" fill="url(#accentGrad)" opacity="0.7"/>'
    )

    by = y + 32
    svg.append(f'    <text x="{width // 2}" y="{by}" class="mono" font-size="18" fill="{theme.accent_purple}" text-anchor="middle" filter="url(#glow)">{esc(config.branding.banner_title)}</text>')
    by += 30
    svg.append(f'    <text x="{width // 2}" y="{by}" class="mono" font-size="14" fill="{theme.accent_blue}" text-anchor="middle">{esc(config.branding.subtitle)}</text>')
    by += 24
    svg.append(f'    <text x="{width // 2}" y="{by}" class="mono" font-size="13" fill="{theme.text_muted}" text-anchor="middle">{esc(config.branding.tagline)}</text>')
    by += 24

    num_roles = len(config.branding.roles)
    tag_w = 120
    tag_gap = 12
    total_tag_w = num_roles * tag_w + (num_roles - 1) * tag_gap
    tag_x_start = width // 2 - total_tag_w // 2

    tag_colors = [theme.accent_blue, theme.accent_green, theme.accent_purple, theme.accent_pink, theme.accent_orange, theme.accent_red]
    for idx, role in enumerate(config.branding.roles):
        tx = tag_x_start + idx * (tag_w + tag_gap)
        tc = tag_colors[idx % len(tag_colors)]
        svg.append(f'    <rect x="{tx}" y="{by - 10}" width="{tag_w}" height="18" rx="9" fill="{tc}" fill-opacity="0.1" stroke="{tc}" stroke-width="0.5" stroke-opacity="0.4"/>')
        svg.append(f'    <text x="{tx + tag_w // 2}" y="{by + 3}" class="mono" font-size="9" fill="{tc}" text-anchor="middle">{esc(role)}</text>')

    svg.append('  </g>')

    y += banner_h + 18
    t += 0.4

    # ── 3. Whoami Prompt ──
    svg.append(
        f'  <g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{t:.2f}s" fill="freeze"/>'
        f'<text x="28" y="{y}" class="mono" font-size="14">'
        f'<tspan fill="{theme.accent_green}">sarthak@ai-terminal:~$</tspan>'
        f' <tspan fill="{theme.text}">whoami</tspan>'
        f'</text>'
        f'<rect x="255" y="{y - 12}" width="9" height="15" rx="1" fill="{theme.accent_blue}" class="cursor"/>'
        f'</g>'
    )
    y += 22
    t += 0.2

    # Grouped profile block (Name, Title, Location, Education, College)
    svg.append(
        f'  <g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{t:.2f}s" fill="freeze"/>'
        f'<rect x="25" y="{y - 10}" width="{width - 50}" height="115" rx="6" fill="{theme.bg_panel}" stroke="{theme.border}" stroke-width="0.5" stroke-opacity="0.5"/>'
        f'</g>'
    )

    profile_lines = [
        ("Name", config.developer.name, theme.accent_blue),
        ("Title", config.developer.title, theme.accent_purple),
        ("Location", config.developer.location, theme.accent_green),
        ("Education", f"{config.developer.education.degree} ({config.developer.education.college})", theme.accent_orange),
    ]

    for label, value, color in profile_lines:
        svg.append(
            f'  <g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{t:.2f}s" fill="freeze"/>'
            f'<text x="45" y="{y + 12}" class="mono" font-size="12" fill="{theme.text}">'
            f'<tspan fill="{theme.accent_green}">▸</tspan> '
            f'<tspan font-weight="bold" fill="{theme.text_muted}">{esc(label):<10}</tspan> '
            f'<tspan fill="{theme.text_dim}">→</tspan> '
            f'<tspan fill="{color}">{esc(value)}</tspan>'
            f'</text></g>'
        )
        y += 22
        t += 0.08

    y += 18
    t += 0.15

    # ── 4. Current Focus & Stack section header ──
    svg.append(
        f'  <g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{t:.2f}s" fill="freeze"/>'
        f'<text x="28" y="{y}" class="mono" font-size="14" font-weight="bold" fill="url(#accentGrad)" filter="url(#glow)">'
        f'⚡ CURRENT FOCUS &amp; STACK</text>'
        f'</g>'
    )
    y += 15
    t += 0.15

    # ── 5. Box-Drawing Table ──
    col1_w = 11
    col2_w = 47

    table_lines = []
    table_lines.append("┌" + "─" * col1_w + "┬" + "─" * col2_w + "┐")

    for i, (key, value) in enumerate(config.focus_rows):
        wrapped = wrap_text_to_cols(value, col2_w - 2)
        for idx, val_line in enumerate(wrapped):
            k = key if idx == 0 else ""
            table_lines.append(f"│ {k.ljust(col1_w - 1)}│ {val_line.ljust(col2_w - 2)} │")
        if i < len(config.focus_rows) - 1:
            table_lines.append("├" + "─" * col1_w + "┼" + "─" * col2_w + "┤")

    table_lines.append("└" + "─" * col1_w + "┴" + "─" * col2_w + "┘")

    # Render each line of the table
    for line in table_lines:
        # Determine color for the line characters vs text
        svg.append(
            f'  <g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.25s" begin="{t:.2f}s" fill="freeze"/>'
            f'<text x="28" y="{y}" class="mono" font-size="12" xml:space="preserve" fill="{theme.text_dim}">'
        )

        # Highlight key items
        if "│" in line:
            parts = line.split("│")
            # format: │ label │ value │
            label_part = parts[1]
            val_part = parts[2]
            key_clean = label_part.strip()
            key_color = get_category_color(theme, key_clean) if key_clean else theme.text

            svg.append(f'<tspan fill="{theme.border}">│</tspan>')
            svg.append(f'<tspan fill="{key_color}" font-weight="bold">{esc(label_part)}</tspan>')
            svg.append(f'<tspan fill="{theme.border}">│</tspan>')
            svg.append(f'<tspan fill="{theme.text}">{esc(val_part)}</tspan>')
            svg.append(f'<tspan fill="{theme.border}">│</tspan>')
        else:
            svg.append(esc(line))

        svg.append('</text></g>')
        y += 18
        t += 0.04

    # ── 6. Footer ──
    y += 10
    svg.append(
        f'  <g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{t:.2f}s" fill="freeze"/>'
        f'<line x1="25" y1="{y}" x2="{width - 25}" y2="{y}" stroke="{theme.border}" stroke-width="0.8" stroke-dasharray="3 3"/>'
        f'<text x="{width // 2}" y="{y + 20}" class="mono" font-size="10" fill="{theme.text_muted}" text-anchor="middle">'
        f'Living Terminal • v2.0 • © 2026 Sarthak Pandey'
        f'</text></g>'
    )

    svg.append('</svg>')

    final_height = y + 45
    content = "\n".join(svg).replace("__SVG_HEIGHT__", str(final_height))
    out_file = Path(output_path)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated panel SVG -> {out_file.resolve()}")
    return content
