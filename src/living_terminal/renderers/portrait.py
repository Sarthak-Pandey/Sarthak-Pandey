from pathlib import Path
from typing import List
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    Image = None
    HAS_PIL = False

GLYPHS = " '.,:;~+*xXO#"
INPUT_IMAGE = Path("assets/photo-ready.png")
FALLBACK_IMAGE = Path("assets/me.jpg")
WIDTH = 80
FONT_SIZE = 10
LINE_HEIGHT = 12
TEXT_COLOR = "#58a6ff"
BACKGROUND = "#0d1117"


def image_to_ascii(image: Image.Image) -> List[str]:
    w, h = image.size
    aspect_ratio = h / w
    new_height = int(WIDTH * aspect_ratio * 0.55)

    img = image.resize((WIDTH, new_height))
    img = img.convert("L")

    pixels = img.load()
    rows = []

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
        "      .----------------------------------------.      ",
        "     /  +------------------------------------+  \\     ",
        "    |  |  sarthak@ai-terminal:~$ whoami     |  |    ",
        "    |  |  Sarthak Pandey - AI Engineer      |  |    ",
        "    |  +------------------------------------+  |    ",
        "     \\________________________________________/     ",
    ]


def render_portrait_svg(output_path: Path | str = "portrait.svg") -> str:
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

    if image is not None:
        rows = image_to_ascii(image)
    else:
        rows = build_fallback_ascii()

    width = WIDTH * FONT_SIZE * 0.62 + 20
    height = len(rows) * LINE_HEIGHT + 20

    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
    )
    svg.append(f'  <rect width="100%" height="100%" fill="{BACKGROUND}" rx="8"/>')
    svg.append(f'  <g font-family="monospace" font-size="{FONT_SIZE}" fill="{TEXT_COLOR}">')

    for i, row in enumerate(rows):
        y = 15 + i * LINE_HEIGHT
        svg.append(f'    <text x="10" y="{y}" xml:space="preserve">{row}</text>')

    svg.append("  </g>")
    svg.append("</svg>")

    content = "\n".join(svg)
    out_file = Path(output_path)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Generated portrait SVG -> {out_file.resolve()}")
    return content
