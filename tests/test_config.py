import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from living_terminal.config import load_config, load_learning


def test_load_config():
    config = load_config("config.yaml")
    assert config.developer.name == "Sarthak Pandey"
    assert config.developer.github_username == "Sarthak-Pandey"
    assert config.developer.title == "AI Engineer"
    assert len(config.focus_rows) >= 8
    assert len(config.projects) == 0


def test_load_learning():
    learning = load_learning("assets/learning.json")
    assert isinstance(learning, list)
    assert "LangGraph" in learning
    assert "Model Context Protocol (MCP)" in learning
    assert "RAG" in learning or "Retrieval-Augmented Generation (RAG)" in learning
