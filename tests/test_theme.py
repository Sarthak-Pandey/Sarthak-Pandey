import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from living_terminal.theme import DARK_THEME, LIGHT_THEME, get_category_color, esc, svg_defs, svg_styles


def test_theme_properties():
    assert DARK_THEME.bg == "#0d1117"
    assert LIGHT_THEME.bg == "#ffffff"
    assert DARK_THEME.accent_blue == "#58a6ff"
    assert LIGHT_THEME.accent_blue == "#0969da"


def test_get_category_color():
    color_dark = get_category_color(DARK_THEME, "Role")
    assert color_dark == DARK_THEME.accent_blue

    color_light = get_category_color(LIGHT_THEME, "Backend")
    assert color_light == LIGHT_THEME.accent_cyan

    unknown_color = get_category_color(DARK_THEME, "Unknown")
    assert unknown_color == DARK_THEME.text


def test_esc():
    original = "Sarthak <Pandey> & Co."
    escaped = esc(original)
    assert escaped == "Sarthak &lt;Pandey&gt; &amp; Co."


def test_svg_defs_and_styles():
    defs = svg_defs(DARK_THEME)
    assert "accentGrad" in defs
    assert "barGrad" in defs

    styles = svg_styles(DARK_THEME)
    assert ".mono" in styles
    assert "@keyframes blink" in styles
