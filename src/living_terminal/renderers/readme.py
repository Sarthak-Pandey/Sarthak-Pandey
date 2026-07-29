import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List
from ..config import AppConfig
from ..stats import GitHubStats

SKILL_BADGES: dict[str, tuple[str, str]] = {
    "Python":           ("python",          "3776AB"),
    "JavaScript":       ("javascript",      "F7DF1E"),
    "C++":              ("cplusplus",        "00599C"),
    "SQL":              ("mysql",            "4479A1"),
    "React":            ("react",            "61DAFB"),
    "Vite":             ("vite",             "646CFF"),
    "HTML":             ("html5",            "E34F26"),
    "CSS":              ("css3",             "1572B6"),
    "Node.js":          ("nodedotjs",        "339933"),
    "Express":          ("express",          "000000"),
    "FastAPI":          ("fastapi",          "009688"),
    "REST APIs":        ("swagger",          "85EA2D"),
    "MongoDB":          ("mongodb",          "47A248"),
    "PostgreSQL":       ("postgresql",       "4169E1"),
    "Redis":            ("redis",            "DC382D"),
    "LangChain":        ("langchain",        "1C3C3C"),
    "LangGraph":        ("langchain",        "1C3C3C"),
    "MCP":              ("anthropic",        "191919"),
    "RAG":              ("openai",           "412991"),
    "Vector Databases": ("pinecone",         "000000"),
    "Hugging Face":     ("huggingface",      "FFD21E"),
    "Transformers":     ("huggingface",      "FFD21E"),
    "AI Agents":        ("openai",           "412991"),
    "NumPy":            ("numpy",            "013243"),
    "Pandas":           ("pandas",           "150458"),
    "Scikit-learn":     ("scikitlearn",      "F7931E"),
    "PyTorch":          ("pytorch",          "EE4C2C"),
    "Git":              ("git",              "F05032"),
    "GitHub":           ("github",           "181717"),
    "Docker":           ("docker",           "2496ED"),
    "GitHub Actions":   ("githubactions",    "2088FF"),
    "AWS":              ("amazonwebservices","232F3E"),
}


def _badge_url(skill: str) -> str:
    slug, color = SKILL_BADGES.get(skill, ("", "555555"))
    label = skill.replace(" ", "%20").replace("+", "%2B")
    if slug:
        return f"https://img.shields.io/badge/{label}-{color}?style=for-the-badge&logo={slug}&logoColor=white"
    return f"https://img.shields.io/badge/{label}-{color}?style=for-the-badge"


def _badge_img(skill: str) -> str:
    url = _badge_url(skill)
    return f'<img src="{url}" alt="{skill}" height="28"/>'


def render_readme_markdown(
    config: AppConfig,
    learning_topics: List[str],
    stats: GitHubStats,
    output_path: Path | str = "Readme.md"
) -> str:
    utc_now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    L: list[str] = []

    # ── 1. Header Banner (ASCII) ──
    L.append('<div align="center">')
    L.append("")
    L.append("```")
    bw = 52
    L.append("╭" + "─" * bw + "╮")
    L.append("│" + " " * bw + "│")
    L.append("│" + f"   {config.branding.banner_title}".ljust(bw) + "│")
    L.append("│" + " " * bw + "│")
    L.append("│" + f"   {config.branding.subtitle}".ljust(bw) + "│")
    L.append("│" + f"   {config.branding.tagline}".ljust(bw) + "│")
    L.append("│" + " " * bw + "│")
    L.append("╰" + "─" * bw + "╯")
    L.append("```")
    L.append("")

    # Typing SVG header
    typing_lines = "%3B".join([
        "AI+Engineer+%7C+Backend+Developer",
        "Building+AI+Systems,+Agents+%26+Products",
        "LLMs+%E2%80%A2+AI+Agents+%E2%80%A2+RAG+%E2%80%A2+Backend",
    ])
    L.append(
        f'<a href="https://github.com/{config.developer.github_username}">'
        f'<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&amp;weight=600'
        f'&amp;size=22&amp;duration=3000&amp;pause=1000&amp;color=58A6FF&amp;center=true&amp;vCenter=true'
        f'&amp;multiline=true&amp;repeat=true&amp;width=600&amp;height=100'
        f'&amp;lines={typing_lines}" alt="Typing SVG" />'
        f'</a>'
    )
    L.append("")
    L.append("</div>")
    L.append("")

    # ── 2. Contribution Graph (Dark/Light Media Query) ──
    L.append('<div align="center">')
    L.append("")
    L.append("### `$ cat contributions.log`")
    L.append("")
    L.append('<picture>')
    L.append('  <source media="(prefers-color-scheme: dark)" srcset="./graph-dark.svg">')
    L.append('  <source media="(prefers-color-scheme: light)" srcset="./graph-light.svg">')
    L.append('  <img alt="GitHub Contributions Graph" src="./graph-dark.svg" width="850">')
    L.append('</picture>')
    L.append("")
    L.append("</div>")
    L.append("")
    L.append("<br>")
    L.append("")

    # ── 3. Whoami Panel (Dark/Light Media Query) ──
    L.append('<div align="center">')
    L.append("")
    L.append("### `$ living-terminal --whoami`")
    L.append("")
    L.append("<table>")
    L.append("<tr>")
    L.append('<td valign="middle">')
    L.append('  <picture>')
    L.append('    <source media="(prefers-color-scheme: dark)" srcset="./portrait-dark.svg">')
    L.append('    <source media="(prefers-color-scheme: light)" srcset="./portrait-light.svg">')
    L.append('    <img alt="Developer Portrait" src="./portrait-dark.svg" width="350">')
    L.append('  </picture>')
    L.append("</td>")
    L.append('<td valign="middle">')
    L.append('  <picture>')
    L.append('    <source media="(prefers-color-scheme: dark)" srcset="./sysinfo-dark.svg">')
    L.append('    <source media="(prefers-color-scheme: light)" srcset="./sysinfo-light.svg">')
    L.append('    <img alt="Terminal System Information" src="./sysinfo-dark.svg" width="480">')
    L.append('  </picture>')
    L.append("</td>")
    L.append("</tr>")
    L.append("</table>")
    L.append("")
    L.append("</div>")
    L.append("")
    L.append("---")
    L.append("")

    # ── 4. GitHub Analytics & Telemetry ──
    L.append("## 📊 GitHub Analytics & Telemetry")
    L.append("")
    L.append('<div align="center">')
    L.append("")
    L.append("| Metric | Value | Metric | Value |")
    L.append("| :--- | :---: | :--- | :---: |")
    L.append(f"| 📦 **Public Repos** | `{stats.public_repos}` | 🔥 **Total Contributions** | `{stats.total_contributions}` |")
    L.append(f"| 👥 **Followers** | `{stats.followers}` | ⚡ **Current Streak** | `{stats.current_streak} days` |")
    L.append(f"| 👤 **Following** | `{stats.following}` | 🏆 **Longest Streak** | `{stats.longest_streak} days` |")
    L.append(f"| 📈 **Avg Commits** | `{stats.average_commits_per_active_day}/day` | 📅 **Most Active** | `{stats.most_active_day}` |")
    L.append(f"| 🌡️ **Heat Score** | `{stats.heat_score_display}` | 🚀 **Status** | `Active & Building` |")
    L.append("")
    L.append("</div>")
    L.append("")
    L.append("---")
    L.append("")

    # ── 5. Technical Arsenal (Shields) ──
    L.append("## 🛠️ Technical Arsenal")
    L.append("")

    skill_sections = [
        ("💻 Languages",      config.skills.languages),
        ("🎨 Frontend",       config.skills.frontend),
        ("⚙️ Backend",        config.skills.backend),
        ("🗄️ Databases",      config.skills.databases),
        ("🤖 AI Engineering", config.skills.ai_engineering),
        ("🧠 Machine Learning", config.skills.machine_learning),
        ("☁️ DevOps & Cloud", config.skills.devops_cloud),
    ]

    for section_title, skills in skill_sections:
        badges = " ".join(_badge_img(s) for s in skills)
        L.append(f"### {section_title}")
        L.append("")
        L.append(f'<p>{badges}</p>')
        L.append("")

    L.append("---")
    L.append("")

    # ── 6. Currently Learning ──
    L.append("## 📚 Currently Learning")
    L.append("")
    for topic in learning_topics:
        display = topic
        if "(" in topic and ")" in topic:
            m = re.search(r"\(([^)]+)\)", topic)
            if m:
                display = m.group(1)
        L.append(f"- [x] {display}")
    L.append("")
    L.append("---")
    L.append("")

    # ── 7. Research Interests ──
    L.append("## 🔬 Research Interests")
    L.append("")
    research = config.research_interests or []
    for res in research:
        L.append(f"▸ **{res}**")
        L.append("    ◆ Advanced algorithmic architectures and engineering models.")
    L.append("")
    L.append("---")
    L.append("")

    # ── 9. Footer ──
    L.append('<div align="center">')
    L.append("")
    L.append("────────────────────────────────────────────────────────────────────────")
    L.append(f"Living Terminal • v2.0 • © 2026 Sarthak Pandey")
    L.append(f"<sub>🕐 Last updated: {utc_now} · Generated dynamically</sub>")
    L.append("")
    L.append("</div>")
    L.append("")

    content = "\n".join(L)
    out_file = Path(output_path)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated Readme markdown -> {out_file.resolve()}")
    return content
