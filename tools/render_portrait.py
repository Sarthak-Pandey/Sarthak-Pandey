from PIL import Image

# Characters from light to dark
GLYPHS = " '.,:;~+*xXO#"

INPUT_IMAGE = "assets/photo-ready.png"
OUTPUT_SVG = "portrait.svg"

WIDTH = 80
FONT_SIZE = 10
LINE_HEIGHT = 12
TEXT_COLOR = "#58a6ff"
BACKGROUND = "#0d1117"


def image_to_ascii(image):
    w, h = image.size

    aspect_ratio = h / w
    new_height = int(WIDTH * aspect_ratio * 0.55)

    image = image.resize((WIDTH, new_height))
    image = image.convert("L")

    pixels = image.load()

    rows = []

    for y in range(image.height):
        row = ""

        for x in range(image.width):
            brightness = pixels[x, y]

            index = int(brightness / 255 * (len(GLYPHS) - 1))
            index = len(GLYPHS) - 1 - index

            row += GLYPHS[index]

        rows.append(row)

    return rows


def build_svg(rows):

    width = WIDTH * FONT_SIZE * 0.62 + 20
    height = len(rows) * LINE_HEIGHT + 20

    svg = []

    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
    )

    svg.append(
        f'<rect width="100%" height="100%" fill="{BACKGROUND}"/>'
    )

    svg.append(
        f'<g font-family="monospace" '
        f'font-size="{FONT_SIZE}" '
        f'fill="{TEXT_COLOR}">'
    )

    for i, row in enumerate(rows):
        y = 15 + i * LINE_HEIGHT
        svg.append(
            f'<text x="10" y="{y}" xml:space="preserve">{row}</text>'
        )

    svg.append("</g>")
    svg.append("</svg>")

    return "\n".join(svg)


def main():
    image = Image.open(INPUT_IMAGE)

    rows = image_to_ascii(image)

    svg = build_svg(rows)

    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write(svg)

    print("Saved portrait.svg")


if __name__ == "__main__":
    main()