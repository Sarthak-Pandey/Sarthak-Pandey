import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from living_terminal.config import load_config, load_learning
from living_terminal.renderers.graph import render_graph_svg
from living_terminal.renderers.panel import render_panel_svg
from living_terminal.renderers.portrait import render_portrait_svg
from living_terminal.renderers.readme import render_readme_markdown
from living_terminal.stats import calculate_stats
from living_terminal.theme import DARK_THEME, LIGHT_THEME


def test_renderers(tmp_path: Path):
    config = load_config("config.yaml")
    learning = load_learning("assets/learning.json")
    stats = calculate_stats([{"date": "2026-01-01", "count": 2, "level": 1}])

    # 1. Dark theme rendering
    panel_dark = tmp_path / "sysinfo-dark.svg"
    graph_dark = tmp_path / "graph-dark.svg"
    portrait_dark = tmp_path / "portrait-dark.svg"

    panel_content_dark = render_panel_svg(config, DARK_THEME, panel_dark)
    assert "<svg" in panel_content_dark
    assert "Sarthak Pandey" in panel_content_dark
    # Check for box-drawing characters used in table
    assert "┌" in panel_content_dark or "├" in panel_content_dark

    graph_content_dark = render_graph_svg([{"date": "2026-01-01", "count": 2, "level": 1}], stats, DARK_THEME, graph_dark)
    assert "<svg" in graph_content_dark
    # Check for hover transition CSS style
    assert ".cell:hover" in graph_content_dark
    # Check for Sparkline path style
    assert "polyline" in graph_content_dark

    portrait_content_dark = render_portrait_svg(DARK_THEME, portrait_dark)
    assert "<svg" in portrait_content_dark

    # 2. Light theme rendering
    panel_light = tmp_path / "sysinfo-light.svg"
    graph_light = tmp_path / "graph-light.svg"
    portrait_light = tmp_path / "portrait-light.svg"

    panel_content_light = render_panel_svg(config, LIGHT_THEME, panel_light)
    assert "<svg" in panel_content_light
    assert LIGHT_THEME.bg in panel_content_light

    graph_content_light = render_graph_svg([{"date": "2026-01-01", "count": 2, "level": 1}], stats, LIGHT_THEME, graph_light)
    assert "<svg" in graph_content_light

    portrait_content_light = render_portrait_svg(LIGHT_THEME, portrait_light)
    assert "<svg" in portrait_content_light

    # 3. Readme markdown rendering
    readme_path = tmp_path / "Readme.md"
    readme_content = render_readme_markdown(config, learning, stats, readme_path)
    assert "Living Terminal • v2.0" in readme_content
    # Check that it uses prefers-color-scheme picture source tags
    assert "prefers-color-scheme: dark" in readme_content
    assert "sysinfo-dark.svg" in readme_content
