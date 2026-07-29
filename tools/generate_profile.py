import sys
from pathlib import Path

# Add workspace src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from living_terminal.config import load_config, load_learning
from living_terminal.fetcher import fetch_contributions, fetch_github_profile
from living_terminal.renderers.graph import render_graph_svg
from living_terminal.renderers.panel import render_panel_svg
from living_terminal.renderers.portrait import render_portrait_svg
from living_terminal.renderers.readme import render_readme_markdown
from living_terminal.stats import calculate_stats


def main() -> None:
    print("==========================================")
    print("  Living Terminal - Profile Generator     ")
    print("==========================================")

    # 1. Load Configurations
    config = load_config("config.yaml")
    learning = load_learning("assets/learning.json")
    print(f"Loaded config for developer: {config.developer.name}")
    print(f"Loaded {len(learning)} learning topics.")

    # 2. Fetch GitHub Profile & Contributions
    username = config.developer.github_username
    user_info = fetch_github_profile(username)
    contributions = fetch_contributions(username, "assets/contributions.json")

    # 3. Calculate GitHub Statistics
    stats = calculate_stats(contributions, user_info)
    print(
        f"Calculated Stats: Repos={stats.public_repos}, Followers={stats.followers}, "
        f"Contributions={stats.total_contributions}, Current Streak={stats.current_streak}d, "
        f"Heat Score={stats.heat_score_display}"
    )

    # 4. Render SVGs & Markdown
    render_panel_svg(config, "sysinfo.svg")
    render_graph_svg(contributions, stats, "graph.svg")
    render_portrait_svg("portrait.svg")
    render_readme_markdown(config, learning, stats, "Readme.md")

    print("==========================================")
    print("  Profile successfully generated!         ")
    print("==========================================")


if __name__ == "__main__":
    main()
