from dataclasses import dataclass
from typing import Dict


@dataclass
class ThemePalette:
    bg: str
    bg_panel: str
    border: str
    text: str
    text_muted: str
    text_dim: str
    accent_blue: str
    accent_green: str
    accent_purple: str
    accent_pink: str
    accent_orange: str
    accent_red: str
    accent_cyan: str
    accent_teal: str
    accent_yellow: str


DARK_THEME = ThemePalette(
    bg="#0d1117",
    bg_panel="#161b22",
    border="#30363d",
    text="#e6edf3",
    text_muted="#8b949e",
    text_dim="#7d8590",
    accent_blue="#58a6ff",
    accent_green="#7ee787",
    accent_purple="#d2a8ff",
    accent_pink="#f778ba",
    accent_orange="#ffa657",
    accent_red="#ff7b72",
    accent_cyan="#39c5cf",
    accent_teal="#56d364",
    accent_yellow="#e3b341",
)

LIGHT_THEME = ThemePalette(
    bg="#ffffff",
    bg_panel="#f6f8fa",
    border="#d0d7de",
    text="#1f2328",
    text_muted="#656d76",
    text_dim="#8c959f",
    accent_blue="#0969da",
    accent_green="#1a7f37",
    accent_purple="#8250df",
    accent_pink="#bf3989",
    accent_orange="#bc4c00",
    accent_red="#cf222e",
    accent_cyan="#006070",
    accent_teal="#117f6e",
    accent_yellow="#9a6700",
)


def get_category_color(theme: ThemePalette, category: str) -> str:
    mapping = {
        "role": theme.accent_blue,
        "focus": theme.accent_green,
        "backend": theme.accent_cyan,
        "frontend": theme.accent_pink,
        "languages": theme.accent_purple,
        "database": theme.accent_orange,
        "cloud": theme.accent_teal,
        "devops": theme.accent_yellow,
        "learning": theme.accent_purple,
        "research": theme.accent_red,
    }
    return mapping.get(category.lower(), theme.text)


def esc(text: str) -> str:
    """Escape XML special characters for SVG text content."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def svg_defs(theme: ThemePalette) -> str:
    return f"""  <defs>
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
    <!-- Accent gradient for section headers -->
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{theme.accent_purple}"/>
      <stop offset="50%" stop-color="{theme.accent_pink}"/>
      <stop offset="100%" stop-color="{theme.accent_orange}"/>
    </linearGradient>
    <!-- Gradient for the top bar -->
    <linearGradient id="barGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{theme.bg_panel}"/>
      <stop offset="100%" stop-color="{theme.bg}"/>
    </linearGradient>
    <!-- Scanline overlay -->
    <pattern id="scanlines" patternUnits="userSpaceOnUse" width="4" height="4">
      <line x1="0" y1="0" x2="4" y2="0" stroke="{theme.text}" stroke-opacity="0.015" stroke-width="1"/>
    </pattern>
  </defs>"""


def svg_styles(theme: ThemePalette) -> str:
    return f"""  <style>
    .mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Courier New', monospace; }}
    .cursor {{ animation: blink 1s step-end infinite; }}
    @keyframes blink {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
    @keyframes slideIn {{ from {{ transform: translateX(-12px); opacity: 0; }} to {{ transform: translateX(0); opacity: 1; }} }}
    @keyframes fadeUp {{ from {{ transform: translateY(6px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: 0.6; }} 50% {{ opacity: 1; }} }}
    @keyframes scanPulse {{ 0%,100% {{ opacity: 0.02; }} 50% {{ opacity: 0.05; }} }}
    @keyframes borderGlow {{
      0%,100% {{ stroke: {theme.border}; stroke-opacity: 0.5; }}
      50% {{ stroke: {theme.accent_blue}; stroke-opacity: 0.25; }}
    }}
  </style>"""
