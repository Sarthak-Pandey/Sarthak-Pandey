ROWS = [
    ("focus",     "Backend • LLMs • RAG • AI Agents"),
    ("languages", "Python • TypeScript • C++"),
    ("backend",   "Node.js • Express • FastAPI"),
    ("frontend",  "React • Tailwind CSS"),
    ("database",  "MongoDB • PostgreSQL"),
    ("framework", "LangChain • LangGraph • MCP"),
    ("learning",  "System Design • AI Engineering"),
    ("solving",   "500+ LeetCode"),
]

OUTPUT = "sysinfo.svg"

WIDTH = 760
HEIGHT = 330

BACKGROUND = "#0d1117"
TEXT = "#58a6ff"
LABEL = "#7ee787"
BORDER = "#30363d"

FONT_SIZE = 18
LINE_HEIGHT = 34


def generate_svg():
    svg = []

    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{WIDTH}" height="{HEIGHT}">'
    )

    # Background
    svg.append(
        f'<rect width="100%" height="100%" rx="12" '
        f'fill="{BACKGROUND}" stroke="{BORDER}" />'
    )

    # Header Bar
    svg.append('<circle cx="25" cy="22" r="6" fill="#ff5f56"/>')
    svg.append('<circle cx="45" cy="22" r="6" fill="#ffbd2e"/>')
    svg.append('<circle cx="65" cy="22" r="6" fill="#27c93f"/>')

    svg.append(
        f'<text x="90" y="28" '
        f'font-family="monospace" '
        f'font-size="16" '
        f'fill="{TEXT}">'
        f'sarthak@github:~$ whoami'
        f'</text>'
    )

    y = 65

    for i, (key, value) in enumerate(ROWS):

        delay = i * 0.15

        svg.append(
            f'''
<g opacity="0">
    <animate attributeName="opacity"
             from="0"
             to="1"
             dur="0.4s"
             begin="{delay}s"
             fill="freeze"/>

    <text
        x="20"
        y="{y}"
        font-family="monospace"
        font-size="{FONT_SIZE}"
        fill="{LABEL}">
        {key}
    </text>

    <text
        x="190"
        y="{y}"
        font-family="monospace"
        font-size="{FONT_SIZE}"
        fill="{TEXT}">
        : {value}
    </text>
</g>
'''
        )

        y += LINE_HEIGHT

    svg.append("</svg>")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print("Generated sysinfo.svg")


if __name__ == "__main__":
    generate_svg()

