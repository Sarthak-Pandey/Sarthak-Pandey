from pathlib import Path
from typing import List
from ..theme import ThemePalette, DARK_THEME

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    Image = None
    HAS_PIL = False

# Extended character set for richer ASCII gradients
GLYPHS = " .'`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

INPUT_IMAGE = Path("assets/photo-ready.png")
FALLBACK_IMAGE = Path("assets/me.jpg")

WIDTH = 80
FONT_SIZE = 10
LINE_HEIGHT = 12


def image_to_ascii(image: "Image.Image") -> List[str]:
    w, h = image.size
    aspect_ratio = h / w
    new_height = int(WIDTH * aspect_ratio * 0.55)

    img = image.resize((WIDTH, new_height))
    img = img.convert("L")

    pixels = img.load()
    rows: list[str] = []

    for y in range(img.height):
        row = ""
        for x in range(img.width):
            brightness = pixels[x, y]
            index = int(brightness / 255 * (len(GLYPHS) - 1))
            index = len(GLYPHS) - 1 - index
            row += GLYPHS[index]
        rows.append(row)

    return rows


def build_fallback_ascii() -> List[str]:
    return [
        "                                                                                ",
        "      ╔══════════════════════════════════════════════════════════════════╗        ",
        "      ║                                                                ║        ",
        "      ║     ███████╗ █████╗ ██████╗ ████████╗██╗  ██╗ █████╗ ██╗  ██╗  ║        ",
        "      ║     ██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║  ██║██╔══██╗██║ ██╔╝  ║        ",
        "      ║     ███████╗███████║██████╔╝   ██║   ███████║███████║█████╔╝   ║        ",
        "      ║     ╚════██║██╔══██║██╔══██╗   ██║   ██╔══██║██╔══██║██╔═██╗   ║        ",
        "      ║     ███████║██║  ██║██║  ██║   ██║   ██║  ██║██║  ██║██║  ██╗  ║        ",
        "      ║     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ║        ",
        "      ║                                                                ║        ",
        "      ║            A I   E N G I N E E R                               ║        ",
        "      ║                                                                ║        ",
        "      ╚══════════════════════════════════════════════════════════════════╝        ",
        "                                                                                ",
    ]


def _esc(ch: str) -> str:
    """Escape XML-sensitive characters."""
    if ch == "&":
        return "&amp;"
    if ch == "<":
        return "&lt;"
    if ch == ">":
        return "&gt;"
    if ch == '"':
        return "&quot;"
    if ch == "'":
        return "&apos;"
    return ch


def render_portrait_svg(
    theme: ThemePalette = DARK_THEME,
    output_path: Path | str = "portrait.svg"
) -> str:
    image = None
    if HAS_PIL and Image is not None:
        if INPUT_IMAGE.exists():
            try:
                image = Image.open(INPUT_IMAGE)
            except Exception:
                pass
        if image is None and FALLBACK_IMAGE.exists():
            try:
                image = Image.open(FALLBACK_IMAGE)
            except Exception:
                pass

    rows = image_to_ascii(image) if image is not None else build_fallback_ascii()

    svg_w = WIDTH * FONT_SIZE * 0.62 + 30
    svg_h = len(rows) * LINE_HEIGHT + 30

    svg: list[str] = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{svg_w}" height="{svg_h}" '
        f'viewBox="0 0 {svg_w} {svg_h}">'
    )

    # ── Definitions ──
    svg.append(f"""  <defs>
    <linearGradient id="portraitGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{theme.accent_blue}" stop-opacity="0.8"/>
      <stop offset="40%" stop-color="{theme.accent_blue}" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="{theme.accent_purple}" stop-opacity="0.3"/>
    </linearGradient>
    <filter id="portraitGlow" x="-5%" y="-5%" width="110%" height="110%">
      <feGaussianBlur stdDeviation="1" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <mask id="scanReveal">
      <rect width="100%" height="100%" fill="white">
        <animate attributeName="height" from="0%" to="100%" dur="1.5s" begin="0.3s" fill="freeze"/>
      </rect>
    </mask>
    <clipPath id="roundedClip">
      <rect width="100%" height="100%" rx="10"/>
    </clipPath>
  </defs>""")

    svg.append(f"""  <style>
    .mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace; }}
    @keyframes borderShimmer {{
      0%,100% {{ stroke: {theme.accent_blue}; stroke-opacity: 0.15; }}
      50% {{ stroke: {theme.accent_purple}; stroke-opacity: 0.35; }}
    }}
  </style>""")

    # ── Background ──
    svg.append(f'  <rect width="100%" height="100%" rx="10" fill="{theme.bg}"/>')
    svg.append(f'  <rect width="100%" height="100%" rx="10" fill="none" stroke="{theme.accent_blue}" stroke-width="1" stroke-opacity="0.15" style="animation: borderShimmer 4s ease-in-out infinite;"/>')

    # ── ASCII Art with scan-reveal mask and gradient colouring ──
    svg.append(f'  <g clip-path="url(#roundedClip)" mask="url(#scanReveal)">')
    svg.append(f'    <g class="mono" font-size="{FONT_SIZE}" fill="url(#portraitGrad)" filter="url(#portraitGlow)">')

    for i, row in enumerate(rows):
        ry = 15 + i * LINE_HEIGHT
        safe_row = "".join(_esc(ch) for ch in row)
        svg.append(f'      <text x="12" y="{ry}" xml:space="preserve">{safe_row}</text>')

    svg.append('    </g>')
    svg.append('  </g>')
    svg.append('</svg>')

    content = "\n".join(svg)
    out_file = Path(output_path)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated portrait SVG -> {out_file.resolve()}")
    return content
