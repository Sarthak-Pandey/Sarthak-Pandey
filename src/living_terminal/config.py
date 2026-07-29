import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Tuple
import yaml


@dataclass
class EducationConfig:
    degree: str
    college: str


@dataclass
class DeveloperProfile:
    name: str
    title: str
    location: str
    education: EducationConfig
    github_username: str


@dataclass
class BrandingConfig:
    banner_title: str
    subtitle: str
    tagline: str
    roles: List[str]


@dataclass
class SkillsConfig:
    languages: List[str]
    frontend: List[str]
    backend: List[str]
    databases: List[str]
    ai_engineering: List[str]
    machine_learning: List[str]
    devops_cloud: List[str]


@dataclass
class AppConfig:
    developer: DeveloperProfile
    branding: BrandingConfig
    focus_rows: List[Tuple[str, str]]
    skills: SkillsConfig
    projects: List[str]
    research_interests: List[str]
    boot_sequence: List[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppConfig":
        edu = EducationConfig(**data["developer"]["education"])
        dev = DeveloperProfile(
            name=data["developer"]["name"],
            title=data["developer"]["title"],
            location=data["developer"]["location"],
            education=edu,
            github_username=data["developer"]["github_username"],
        )
        branding = BrandingConfig(**data["branding"])
        focus_rows = [(row[0], row[1]) for row in data["focus_rows"]]
        skills = SkillsConfig(**data["skills"])

        return cls(
            developer=dev,
            branding=branding,
            focus_rows=focus_rows,
            skills=skills,
            projects=data.get("projects", []),
            research_interests=data.get("research_interests", []),
            boot_sequence=data.get("boot_sequence", []),
        )


def load_config(config_path: Path | str = "config.yaml") -> AppConfig:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found at {path.resolve()}")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return AppConfig.from_dict(data)


def load_learning(learning_path: Path | str = "assets/learning.json") -> List[str]:
    path = Path(learning_path)
    if not path.exists():
        return [
            "LangGraph",
            "Model Context Protocol (MCP)",
            "Retrieval-Augmented Generation (RAG)",
            "AI Agents",
            "Prompt Optimization",
            "WorldQuant Brain",
            "Backend Engineering",
            "System Design",
            "AWS",
            "MLOps",
        ]
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, list):
            return data
        return []
