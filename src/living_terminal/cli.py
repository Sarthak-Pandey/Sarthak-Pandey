import shutil
import sys
from pathlib import Path
from .config import load_config, load_learning
from .fetcher import fetch_contributions, fetch_github_profile
from .stats import calculate_stats
from .theme import DARK_THEME, LIGHT_THEME
from .renderers.panel import render_panel_svg
from .renderers.graph import render_graph_svg
from .renderers.portrait import render_portrait_svg
from .renderers.readme import render_readme_markdown


def main() -> None:
    print("==========================================")
    print("  Living Terminal v2.0 - Profile Generator")
    print("==========================================")

    # 1. Load configuration
    config = load_config("config.yaml")
    learning = load_learning("assets/learning.json")
    print(f"Loaded developer config for: {config.developer.name}")

    # 2. Fetch data
    username = config.developer.github_username
    user_info = fetch_github_profile(username)
    contributions = fetch_contributions(username, "assets/contributions.json")

    # 3. Calculate statistics
    stats = calculate_stats(contributions, user_info)

    # Create build directory
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)

    # 4. Render dark and light theme assets
    print("Rendering SVG/Markdown assets...")

    # Panel SVGs
    render_panel_svg(config, DARK_THEME, build_dir / "sysinfo-dark.svg")
    render_panel_svg(config, LIGHT_THEME, build_dir / "sysinfo-light.svg")

    # Graph SVGs
    render_graph_svg(contributions, stats, DARK_THEME, build_dir / "graph-dark.svg")
    render_graph_svg(contributions, stats, LIGHT_THEME, build_dir / "graph-light.svg")

    # Portrait SVGs
    render_portrait_svg(DARK_THEME, build_dir / "portrait-dark.svg")
    render_portrait_svg(LIGHT_THEME, build_dir / "portrait-light.svg")

    # Readme Markdown (points to build/dark/light SVGs in root)
    render_readme_markdown(config, learning, stats, build_dir / "Readme.md")

    # Copy files to workspace root for GitHub display
    shutil.copy(build_dir / "sysinfo-dark.svg", "sysinfo-dark.svg")
    shutil.copy(build_dir / "sysinfo-light.svg", "sysinfo-light.svg")
    shutil.copy(build_dir / "sysinfo-dark.svg", "sysinfo.svg")
    
    shutil.copy(build_dir / "graph-dark.svg", "graph-dark.svg")
    shutil.copy(build_dir / "graph-light.svg", "graph-light.svg")
    shutil.copy(build_dir / "graph-dark.svg", "graph.svg")
    
    shutil.copy(build_dir / "portrait-dark.svg", "portrait-dark.svg")
    shutil.copy(build_dir / "portrait-light.svg", "portrait-light.svg")
    shutil.copy(build_dir / "portrait-dark.svg", "portrait.svg")
    
    shutil.copy(build_dir / "Readme.md", "Readme.md")

    print("==========================================")
    print("  Profile successfully generated to root!")
    print("==========================================")


if __name__ == "__main__":
    main()
