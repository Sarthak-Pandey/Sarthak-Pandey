import json
from pathlib import Path

INPUT = Path("assets/contributions.json")
OUTPUT = Path("graph.svg")

# Colors for contribution levels
LEVELS = [
    "#161b22",  # No contributions
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353"
]

CELL = 12
GAP = 3
MARGIN = 30


def load_data():
    with open(INPUT, "r") as f:
        return json.load(f)


def generate_svg(days):

    width = MARGIN * 2 + (53 * (CELL + GAP))
    height = MARGIN * 2 + (7 * (CELL + GAP)) + 60

    svg = []

    svg.append(f'''
<svg xmlns="http://www.w3.org/2000/svg"
     width="{width}"
     height="{height}">
''')

    # Background
    svg.append(f'''
<rect width="100%" height="100%" fill="#0d1117"/>
''')

    # Title
    svg.append(f'''
<text
    x="{MARGIN}"
    y="20"
    font-family="monospace"
    font-size="16"
    fill="#58a6ff">
GitHub Contributions
</text>
''')

    for index, day in enumerate(days):

        week = index // 7
        weekday = index % 7

        x = MARGIN + week * (CELL + GAP)
        y = MARGIN + weekday * (CELL + GAP)

        level = day["level"]

        color = LEVELS[level]

        svg.append(f'''
<rect
    x="{x}"
    y="{y}"
    width="{CELL}"
    height="{CELL}"
    rx="2"
    fill="{color}">
<title>
{day["date"]} : {day["count"]} contributions
</title>
</rect>
''')

    # Legend
    legend_y = height - 25
    legend_x = MARGIN

    svg.append(f'''
<text
x="{legend_x}"
y="{legend_y-5}"
font-family="monospace"
font-size="12"
fill="white">
Less
</text>
''')

    legend_x += 40

    for color in LEVELS:

        svg.append(f'''
<rect
x="{legend_x}"
y="{legend_y-15}"
width="10"
height="10"
fill="{color}"/>
''')

        legend_x += 15

    svg.append(f'''
<text
x="{legend_x+5}"
y="{legend_y-5}"
font-family="monospace"
font-size="12"
fill="white">
More
</text>
''')

    svg.append("</svg>")

    return "\n".join(svg)


def main():

    days = load_data()

    svg = generate_svg(days)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(svg)

    print("Generated graph.svg")


if __name__ == "__main__":
    main()