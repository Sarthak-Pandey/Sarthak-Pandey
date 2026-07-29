from pathlib import Path
from typing import List, Tuple
from ..config import AppConfig


def render_panel_svg(
    config: AppConfig,
    output_path: Path | str = "sysinfo.svg"
) -> str:
    width = 840
    # Calculate height dynamically based on content
    # Titlebar (40) + Banner (140) + Boot Seq (150) + Prompt/Whoami (120) + Focus Header (30) + 10 Focus Rows (10 * 30 = 300) + Padding
    height = 760

    background = "#0d1117"
    border = "#30363d"
    text_color = "#58a6ff"
    label_color = "#7ee787"
    dim_color = "#8b949e"
    white_color = "#c9d1d9"
    accent_color = "#d2a8ff"

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')

    # CSS Styles for Animations
    svg.append("""
  <style>
    .font-mono { font-family: 'Fira Code', 'Courier New', Consolas, monospace; }
    .cursor { animation: blink 1s infinite; fill: #58a6ff; }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
  </style>
""")

    # Background Box with Terminal Border
    svg.append(f'  <rect width="100%" height="100%" rx="12" fill="{background}" stroke="{border}" stroke-width="2"/>')

    # Terminal Window Controls Header Bar
    svg.append('  <circle cx="25" cy="22" r="6" fill="#ff5f56"/>')
    svg.append('  <circle cx="45" cy="22" r="6" fill="#ffbd2e"/>')
    svg.append('  <circle cx="65" cy="22" r="6" fill="#27c93f"/>')
    svg.append(
        f'  <text x="90" y="27" class="font-mono" font-size="14" fill="{dim_color}">'
        f'{config.developer.github_username}@ai-terminal:~$ living-terminal --init'
        f'</text>'
    )
    svg.append(f'  <line x1="0" y1="42" x2="{width}" y2="42" stroke="{border}" stroke-width="1"/>')

    y = 65

    # 1. Boot Sequence Animation (Sequential appearance)
    boot_sequence = config.boot_sequence or [
        "Initializing terminal...",
        "Loading AI modules...",
        "Loading backend services...",
        "Connecting GitHub...",
        "Loading repositories...",
        "Rendering SVG...",
        "Fetching contribution graph...",
        "Loading learning progress...",
        "System ready."
    ]

    boot_start_time = 0.1
    boot_line_interval = 0.15

    for i, line in enumerate(boot_sequence):
        delay = round(boot_start_time + i * boot_line_interval, 2)
        color = "#7ee787" if "ready" in line.lower() else dim_color
        prefix = "[OK]" if "ready" in line.lower() else "  >>"
        svg.append(f'''  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{delay}s" fill="freeze"/>
    <text x="25" y="{y}" class="font-mono" font-size="13" fill="{color}">{prefix} {line}</text>
  </g>''')
        y += 22

    y += 10
    start_main_time = round(boot_start_time + len(boot_sequence) * boot_line_interval + 0.2, 2)

    # 2. Terminal Banner Box Frame
    banner_lines = [
        "╭────────────────────────────────────────────╮",
        "│                                            │",
        f"│   {config.branding.banner_title:<41}│",
        "│                                            │",
        f"│   {config.branding.subtitle:<41}│",
        f"│   {config.branding.tagline:<41}│",
        "│                                            │",
        "╰────────────────────────────────────────────╯",
    ]

    svg.append(f'''  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{start_main_time}s" fill="freeze"/>''')

    banner_y = y
    for line in banner_lines:
        color = accent_color if "Welcome" in line or "AI Engineer" in line else dim_color
        svg.append(f'    <text x="25" y="{banner_y}" class="font-mono" font-size="13" fill="{color}">{line}</text>')
        banner_y += 18

    svg.append('  </g>')

    y = banner_y + 15
    whoami_prompt_time = round(start_main_time + 0.4, 2)

    # 3. Typing Header (whoami prompt & output)
    svg.append(f'''  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{whoami_prompt_time}s" fill="freeze"/>
    <text x="25" y="{y}" class="font-mono" font-size="14" fill="{label_color}">
      sarthak@ai-terminal:~$ <tspan fill="{white_color}">whoami</tspan>
    </text>
  </g>''')

    y += 22
    whoami_output_time = round(whoami_prompt_time + 0.3, 2)
    whoami_roles = [
        f"Name   : {config.developer.name}",
        f"Title  : {config.developer.title}",
        f"Roles  : { ' • '.join(config.branding.roles[:4]) }",
    ]

    for role_line in whoami_roles:
        svg.append(f'''  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{whoami_output_time}s" fill="freeze"/>
    <text x="45" y="{y}" class="font-mono" font-size="13" fill="{text_color}">► {role_line}</text>
  </g>''')
        y += 20
        whoami_output_time = round(whoami_output_time + 0.15, 2)

    # Blinking cursor after whoami block
    svg.append(f'''  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{whoami_prompt_time}s" fill="freeze"/>
    <rect x="235" y="{y-62}" width="9" height="15" class="cursor"/>
  </g>''')

    y += 15
    focus_rows_start_time = round(whoami_output_time + 0.3, 2)

    # Separator Line
    svg.append(f'''  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{focus_rows_start_time}s" fill="freeze"/>
    <line x1="25" y1="{y}" x2="{width - 25}" y2="{y}" stroke="{border}" stroke-width="1" stroke-dasharray="4 4"/>
  </g>''')

    y += 25

    # Section Header
    svg.append(f'''  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{focus_rows_start_time}s" fill="freeze"/>
    <text x="25" y="{y}" class="font-mono" font-size="14" font-weight="bold" fill="{accent_color}">⚡ CURRENT FOCUS & STACK</text>
  </g>''')

    y += 25
    row_time = round(focus_rows_start_time + 0.2, 2)

    # 4. Sequential Focus Rows Animation
    for key, value in config.focus_rows:
        svg.append(f'''  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{row_time}s" fill="freeze"/>
    <text x="25" y="{y}" class="font-mono" font-size="13" fill="{label_color}">{key:<11}</text>
    <text x="140" y="{y}" class="font-mono" font-size="13" fill="{white_color}">: <tspan fill="{text_color}">{value}</tspan></text>
  </g>''')
        y += 24
        row_time = round(row_time + 0.15, 2)

    svg.append('</svg>')

    content = "\n".join(svg)
    out_file = Path(output_path)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Generated panel SVG -> {out_file.resolve()}")
    return content
