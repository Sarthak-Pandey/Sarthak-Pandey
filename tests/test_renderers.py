import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from living_terminal.config import load_config, load_learning
from living_terminal.renderers.graph import render_graph_svg
from living_terminal.renderers.panel import render_panel_svg
from living_terminal.renderers.portrait import render_portrait_svg
from living_terminal.renderers.readme import render_readme_markdown
from living_terminal.stats import calculate_stats


def test_renderers(tmp_path: Path):
    config = load_config("config.yaml")
    learning = load_learning("assets/learning.json")
    stats = calculate_stats([{"date": "2026-01-01", "count": 2, "level": 1}])

    panel_path = tmp_path / "sysinfo.svg"
    graph_path = tmp_path / "graph.svg"
    portrait_path = tmp_path / "portrait.svg"
    readme_path = tmp_path / "Readme.md"

    panel_content = render_panel_svg(config, panel_path)
    assert "<svg" in panel_content
    assert "sarthak" in panel_content.lower() or "Sarthak" in panel_content
    assert "AI Engineer" in panel_content

    graph_content = render_graph_svg(
        [{"date": "2026-01-01", "count": 2, "level": 1}],
        stats, graph_path
    )
    assert "<svg" in graph_content
    assert "contributions.log" in graph_content

    portrait_content = render_portrait_svg(portrait_path)
    assert "<svg" in portrait_content

    readme_content = render_readme_markdown(config, learning, stats, readme_path)
    assert "Living Terminal" in readme_content
    assert "Currently Learning" in readme_content
    assert "Current Projects" in readme_content
    assert "Research" in readme_content
    assert "Last updated" in readme_content
