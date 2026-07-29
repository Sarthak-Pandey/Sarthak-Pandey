import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List
from ..config import AppConfig
from ..stats import GitHubStats


def render_readme_markdown(
    config: AppConfig,
    learning_topics: List[str],
    stats: GitHubStats,
    output_path: Path | str = "Readme.md"
) -> str:
    utc_now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = []

    # 1. GitHub Terminal Banner Header
    lines.append("```")
    lines.append("╭────────────────────────────────────────────╮")
    lines.append("│                                            │")
    lines.append(f"│   {config.branding.banner_title:<41}│")
    lines.append("│                                            │")
    lines.append(f"│   {config.branding.subtitle:<41}│")
    lines.append(f"│   {config.branding.tagline:<41}│")
    lines.append("│                                            │")
    lines.append("╰────────────────────────────────────────────╯")
    lines.append("```")
    lines.append("")

    # 2. Main Visual Layout (Graph + Panel & Portrait)
    lines.append('<div align="center">')
    lines.append("")
    lines.append("### <code>$ cat contributions.log</code>")
    lines.append("")
    lines.append('<img src="./graph.svg" width="820"/>')
    lines.append("")
    lines.append("<br><br>")
    lines.append("")
    lines.append("### <code>$ living-terminal --whoami</code>")
    lines.append("")
    lines.append("<table>")
    lines.append("<tr>")
    lines.append("<td>")
    lines.append('<img src="./portrait.svg" width="350"/>')
    lines.append("</td>")
    lines.append("<td>")
    lines.append('<img src="./sysinfo.svg" width="460"/>')
    lines.append("</td>")
    lines.append("</tr>")
    lines.append("</table>")
    lines.append("")
    lines.append("</div>")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 3. GitHub Statistics Card
    lines.append("## 📊 GitHub Analytics & Telemetry")
    lines.append("")
    lines.append("| Metric | Value | Metric | Value |")
    lines.append("| :--- | :--- | :--- | :--- |")
    lines.append(f"| **Public Repositories** | `{stats.public_repos}` | **Total Contributions** | `{stats.total_contributions}` |")
    lines.append(f"| **Followers** | `{stats.followers}` | **Current Streak** | `{stats.current_streak} days` |")
    lines.append(f"| **Following** | `{stats.following}` | **Longest Streak** | `{stats.longest_streak} days` |")
    lines.append(f"| **Average Commits** | `{stats.average_commits_per_active_day} / active day` | **Most Active Day** | `{stats.most_active_day}` |")
    lines.append(f"| **Heat Score** | `{stats.heat_score_display}` | **Developer Status** | `Active & Building` |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 4. Technical Skills
    lines.append("## 🛠️ Technical Skills")
    lines.append("")
    s = config.skills
    lines.append(f"- **Programming Languages:** {', '.join(s.languages)}")
    lines.append(f"- **Frontend:** {', '.join(s.frontend)}")
    lines.append(f"- **Backend:** {', '.join(s.backend)}")
    lines.append(f"- **Databases:** {', '.join(s.databases)}")
    lines.append(f"- **AI Engineering:** {', '.join(s.ai_engineering)}")
    lines.append(f"- **Machine Learning:** {', '.join(s.machine_learning)}")
    lines.append(f"- **DevOps & Cloud:** {', '.join(s.devops_cloud)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 5. Currently Learning (Read from assets/learning.json)
    lines.append("## Currently Learning")
    lines.append("")
    for topic in learning_topics:
        display_topic = topic
        if "(" in topic and ")" in topic:
            m = re.search(r"\(([^)]+)\)", topic)
            if m:
                display_topic = m.group(1)
        lines.append(f"✓ {display_topic}")
        lines.append("")
    lines.append("---")
    lines.append("")

    # 6. Current Projects
    lines.append("## Current Projects")
    lines.append("")
    projects = config.projects or ["Living Terminal", "AI Core Search", "Prompt Optimizer", "Moodify"]
    for proj in projects:
        display_proj = proj
        if "(" in proj and ")" in proj:
            display_proj = re.sub(r"\s*\([^)]*\)", "", proj).strip()
        lines.append(f"• {display_proj}")
        lines.append("")
    lines.append("---")
    lines.append("")

    # 7. Research
    lines.append("## Research")
    lines.append("")
    research = config.research_interests or [
        "Large Language Models",
        "AI Agents",
        "Retrieval-Augmented Generation",
        "Prompt Engineering",
        "Prompt Optimization",
        "WorldQuant Alpha Research",
        "Backend Architecture",
        "System Design",
    ]
    for res in research:
        lines.append(f"• {res}")
        lines.append("")
    lines.append("---")
    lines.append("")

    # 8. Dynamic Footer
    lines.append("## Last Updated")
    lines.append("")
    lines.append(utc_now)
    lines.append("")
    lines.append("Generated automatically by Living Terminal")
    lines.append("")

    content = "\n".join(lines)
    out_file = Path(output_path)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Generated Readme markdown -> {out_file.resolve()}")
    return content
