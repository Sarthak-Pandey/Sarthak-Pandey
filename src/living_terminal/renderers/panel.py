from pathlib import Path
from typing import List, Tuple
from ..config import AppConfig


def _esc(text: str) -> str:
    """Escape XML special characters for SVG text content."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_panel_svg(
    config: AppConfig,
    output_path: Path | str = "sysinfo.svg"
) -> str:
    width = 860
    height = 820

    # ── Colour Palette (GitHub-dark + neon accents) ──
    bg = "#0d1117"
    bg_panel = "#161b22"
    border = "#30363d"
    cyan = "#58a6ff"
    green = "#7ee787"
    purple = "#d2a8ff"
    pink = "#f778ba"
    dim = "#484f58"
    muted = "#8b949e"
    white = "#e6edf3"
    orange = "#ffa657"
    red = "#ff7b72"

    svg: list[str] = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
    )

    # ── Definitions: gradients, filters, clip-paths ──
    svg.append("""  <defs>
    <!-- Glow filter for neon text -->
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <!-- Strong glow for banner -->
    <filter id="glowStrong" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <!-- Subtle inner shadow for panel depth -->
    <filter id="innerShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feOffset dx="0" dy="1"/>
      <feGaussianBlur stdDeviation="1.5" result="shadow"/>
      <feComposite in2="SourceGraphic" operator="arithmetic" k1="0" k2="1" k3="-0.2" k4="0"/>
    </filter>
    <!-- Gradient for the top bar -->
    <linearGradient id="barGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#161b22"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
    <!-- Accent gradient for section headers -->
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#d2a8ff"/>
      <stop offset="50%" stop-color="#f778ba"/>
      <stop offset="100%" stop-color="#ffa657"/>
    </linearGradient>
    <!-- Scanline overlay -->
    <pattern id="scanlines" patternUnits="userSpaceOnUse" width="4" height="4">
      <line x1="0" y1="0" x2="4" y2="0" stroke="#ffffff" stroke-opacity="0.015" stroke-width="1"/>
    </pattern>
  </defs>""")

    # ── CSS Styles & Keyframes ──
    svg.append(f"""  <style>
    .mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Courier New', monospace; }}
    .cursor {{ animation: blink 1s step-end infinite; }}
    @keyframes blink {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
    @keyframes slideIn {{ from {{ transform: translateX(-12px); opacity: 0; }} to {{ transform: translateX(0); opacity: 1; }} }}
    @keyframes fadeUp {{ from {{ transform: translateY(6px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: 0.6; }} 50% {{ opacity: 1; }} }}
    @keyframes scanPulse {{ 0%,100% {{ opacity: 0.02; }} 50% {{ opacity: 0.05; }} }}
    @keyframes borderGlow {{
      0%,100% {{ stroke: {border}; stroke-opacity: 0.5; }}
      50% {{ stroke: {cyan}; stroke-opacity: 0.25; }}
    }}
  </style>""")

    # ── Background ──
    svg.append(f'  <rect width="100%" height="100%" rx="14" fill="{bg}"/>')
    # Outer glow border
    svg.append(f'  <rect width="100%" height="100%" rx="14" fill="none" stroke="{cyan}" stroke-width="1" stroke-opacity="0.12" style="animation: borderGlow 6s ease-in-out infinite;"/>')
    # Scanline overlay
    svg.append(f'  <rect width="100%" height="100%" rx="14" fill="url(#scanlines)" style="animation: scanPulse 4s ease-in-out infinite;"/>')

    # ── Title Bar ──
    svg.append(f'  <rect x="0" y="0" width="{width}" height="44" rx="14" fill="url(#barGrad)"/>')
    svg.append(f'  <rect x="0" y="30" width="{width}" height="14" fill="url(#barGrad)"/>')
    # macOS traffic-light dots with subtle shadows
    for cx, color in [(24, "#ff5f57"), (46, "#febc2e"), (68, "#28c840")]:
        svg.append(f'  <circle cx="{cx}" cy="22" r="6.5" fill="{color}" opacity="0.9"/>')
        svg.append(f'  <circle cx="{cx}" cy="22" r="6.5" fill="none" stroke="#000" stroke-opacity="0.15" stroke-width="0.5"/>')

    # Title bar text
    svg.append(
        f'  <text x="95" y="27" class="mono" font-size="13" fill="{muted}" letter-spacing="0.5">'
        f'{_esc(config.developer.github_username)}@ai-terminal:~$ '
        f'<tspan fill="{green}">living-terminal</tspan>'
        f' <tspan fill="{muted}">--init</tspan>'
        f'</text>'
    )
    svg.append(f'  <line x1="0" y1="44" x2="{width}" y2="44" stroke="{border}" stroke-width="1"/>')

    y = 68

    # ════════════════════════════════════════════════════
    # 1.  BOOT SEQUENCE  –  staggered slide-in, per-line
    # ════════════════════════════════════════════════════
    boot_seq = config.boot_sequence or []
    t = 0.2  # start time

    for i, line in enumerate(boot_seq):
        is_ready = "ready" in line.lower()
        color = green if is_ready else dim
        icon = "✓" if is_ready else "›"
        svg.append(
            f'  <g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.25s" begin="{t:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="-10 0" to="0 0" dur="0.25s" begin="{t:.2f}s" fill="freeze"/>'
            f'<text x="28" y="{y}" class="mono" font-size="12" fill="{color}">'
            f'<tspan fill="{green if is_ready else muted}">{icon}</tspan> {_esc(line)}'
            f'</text></g>'
        )
        y += 19
        t += 0.12

    y += 8
    t += 0.25

    # ════════════════════════════════════════════════════
    # 2.  WELCOME BANNER  –  box with neon glow
    # ════════════════════════════════════════════════════
    banner_h = 130
    banner_x = 25
    banner_w = width - 50

    svg.append(
        f'  <g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{t:.2f}s" fill="freeze"/>'
    )
    # Banner background panel
    svg.append(
        f'    <rect x="{banner_x}" y="{y}" width="{banner_w}" height="{banner_h}" rx="8" '
        f'fill="{bg_panel}" stroke="{cyan}" stroke-width="0.6" stroke-opacity="0.3"/>'
    )
    # Gradient accent line at top of banner
    svg.append(
        f'    <rect x="{banner_x}" y="{y}" width="{banner_w}" height="2" rx="1" fill="url(#accentGrad)" opacity="0.7"/>'
    )

    # Banner text
    by = y + 32
    svg.append(f'    <text x="{width // 2}" y="{by}" class="mono" font-size="18" fill="{purple}" text-anchor="middle" filter="url(#glow)">{_esc(config.branding.banner_title)}</text>')
    by += 30
    svg.append(f'    <text x="{width // 2}" y="{by}" class="mono" font-size="14" fill="{cyan}" text-anchor="middle">{_esc(config.branding.subtitle)}</text>')
    by += 24
    svg.append(f'    <text x="{width // 2}" y="{by}" class="mono" font-size="13" fill="{muted}" text-anchor="middle">{_esc(config.branding.tagline)}</text>')
    by += 24
    # Role tags as pill badges
    tag_x_start = width // 2 - 250
    tag_colors = [cyan, green, purple, pink, orange, red]
    for idx, role in enumerate(config.branding.roles[:6]):
        tx = tag_x_start + idx * 140
        tc = tag_colors[idx % len(tag_colors)]
        svg.append(f'    <rect x="{tx}" y="{by - 10}" width="130" height="18" rx="9" fill="{tc}" fill-opacity="0.1" stroke="{tc}" stroke-width="0.5" stroke-opacity="0.4"/>')
        svg.append(f'    <text x="{tx + 65}" y="{by + 3}" class="mono" font-size="9" fill="{tc}" text-anchor="middle">{_esc(role)}</text>')

    svg.append('  </g>')

    y += banner_h + 18
    t += 0.5

    # ════════════════════════════════════════════════════
    # 3.  WHOAMI PROMPT  –  typing animation + cursor
    # ════════════════════════════════════════════════════
    prompt_text = "sarthak@ai-terminal:~$"
    command = "whoami"

    svg.append(
        f'  <g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{t:.2f}s" fill="freeze"/>'
        f'<text x="28" y="{y}" class="mono" font-size="14">'
        f'<tspan fill="{green}">{prompt_text}</tspan>'
        f' <tspan fill="{white}">{command}</tspan>'
        f'</text>'
        f'<rect x="255" y="{y - 12}" width="9" height="15" rx="1" fill="{cyan}" class="cursor"/>'
        f'</g>'
    )

    y += 24
    t += 0.3

    whoami_lines = [
        ("Name", config.developer.name, cyan),
        ("Title", config.developer.title, purple),
        ("Location", config.developer.location, green),
        ("Education", config.developer.education.degree, orange),
        ("College", config.developer.education.college, muted),
    ]

    for label, value, color in whoami_lines:
        svg.append(
            f'  <g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{t:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 4" to="0 0" dur="0.2s" begin="{t:.2f}s" fill="freeze"/>'
            f'<text x="45" y="{y}" class="mono" font-size="13">'
            f'<tspan fill="{green}">▸</tspan>'
            f' <tspan fill="{muted}">{_esc(label):8s}</tspan>'
            f' <tspan fill="{dim}">→</tspan>'
            f' <tspan fill="{color}">{_esc(value)}</tspan>'
            f'</text></g>'
        )
        y += 21
        t += 0.12

    y += 10
    t += 0.15

    # ════════════════════════════════════════════════════
    # 4.  SEPARATOR + SECTION HEADER  with gradient bar
    # ════════════════════════════════════════════════════
    svg.append(
        f'  <g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{t:.2f}s" fill="freeze"/>'
        f'<rect x="25" y="{y}" width="{width - 50}" height="1" fill="url(#accentGrad)" opacity="0.4"/>'
        f'</g>'
    )
    y += 22

    svg.append(
        f'  <g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{t:.2f}s" fill="freeze"/>'
        f'<text x="28" y="{y}" class="mono" font-size="14" font-weight="bold" fill="url(#accentGrad)" filter="url(#glow)">'
        f'⚡ CURRENT FOCUS &amp; STACK</text>'
        f'</g>'
    )
    y += 22
    t += 0.25

    # ════════════════════════════════════════════════════
    # 5.  FOCUS ROWS  –  slide-in from left, alternating
    # ════════════════════════════════════════════════════
    row_colors = [cyan, green, purple, pink, orange, cyan, green, purple, orange, pink]

    for i, (key, value) in enumerate(config.focus_rows):
        rc = row_colors[i % len(row_colors)]
        # Alternating subtle row background
        if i % 2 == 0:
            svg.append(
                f'  <g opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{t:.2f}s" fill="freeze"/>'
                f'<rect x="25" y="{y - 14}" width="{width - 50}" height="21" rx="3" fill="{bg_panel}" opacity="0.5"/>'
                f'</g>'
            )

        svg.append(
            f'  <g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.35s" begin="{t:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="-15 0" to="0 0" dur="0.35s" begin="{t:.2f}s" fill="freeze"/>'
            f'<text x="30" y="{y}" class="mono" font-size="13">'
            f'<tspan fill="{rc}" font-weight="bold">{_esc(key):11s}</tspan>'
            f'<tspan fill="{dim}"> : </tspan>'
            f'<tspan fill="{white}">{_esc(value)}</tspan>'
            f'</text></g>'
        )
        y += 23
        t += 0.10

    svg.append('</svg>')

    content = "\n".join(svg)
    out_file = Path(output_path)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated panel SVG -> {out_file.resolve()}")
    return content
