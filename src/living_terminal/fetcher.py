import json
from pathlib import Path
import re
from typing import Any, Dict, List
import httpx


def fetch_github_profile(username: str) -> Dict[str, Any]:
    url = f"https://api.github.com/users/{username}"
    headers = {"User-Agent": "LivingTerminal-Agent"}
    try:
        response = httpx.get(url, headers=headers, timeout=10.0)
        if response.status_code == 200:
            data = response.json()
            return {
                "public_repos": data.get("public_repos", 12),
                "followers": data.get("followers", 15),
                "following": data.get("following", 10),
            }
    except Exception as e:
        print(f"Warning: Could not fetch GitHub API profile stats ({e}). Using fallback values.")

    profile_path = Path("assets/user_profile.json")
    if profile_path.exists():
        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return {"public_repos": 12, "followers": 15, "following": 10}


def fetch_contributions(username: str, output_path: Path | str = "assets/contributions.json") -> List[Dict[str, Any]]:
    url = f"https://github.com/users/{username}/contributions"
    headers = {"User-Agent": "LivingTerminal-Agent"}
    output = Path(output_path)

    try:
        response = httpx.get(url, headers=headers, timeout=15.0)
        if response.status_code == 200:
            html_content = response.text

            # Extract tooltips mapping ID -> count
            tooltip_matches = re.findall(
                r'<tool-tip[^>]*for="([^"]+)"[^>]*>(.*?)</tool-tip>', html_content, re.DOTALL
            )
            counts: Dict[str, int] = {}
            for day_id, text in tooltip_matches:
                clean_text = text.strip()
                if clean_text.startswith("No "):
                    count = 0
                else:
                    m = re.search(r"(\d+)\s+contribution", clean_text)
                    count = int(m.group(1)) if m else 0
                counts[day_id] = count

            # Extract td elements with data-date, data-level, id
            td_matches = re.findall(
                r'<td[^>]*data-date="([^"]+)"[^>]*data-level="(\d+)"[^>]*id="([^"]+)"', html_content
            )
            if not td_matches:
                # Try alternate attributes order
                td_matches = re.findall(
                    r'<td[^>]*id="([^"]+)"[^>]*data-date="([^"]+)"[^>]*data-level="(\d+)"', html_content
                )
                # Reorder tuple to (date, level, id)
                td_matches = [(m[1], m[2], m[0]) for m in td_matches]

            contributions: List[Dict[str, Any]] = []
            for date, level_str, day_id in td_matches:
                count = counts.get(day_id, 0)
                contributions.append({
                    "date": date,
                    "count": count,
                    "level": int(level_str),
                })

            if contributions:
                output.parent.mkdir(parents=True, exist_ok=True)
                with open(output, "w", encoding="utf-8") as f:
                    json.dump(contributions, f, indent=4)
                print(f"Fetched and saved {len(contributions)} live contribution days to {output}")
                return contributions
    except Exception as e:
        print(f"Warning: Live contribution scraping failed ({e}). Loading cached data.")

    if output.exists():
        try:
            with open(output, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"Loaded {len(data)} cached contribution days from {output}")
                return data
        except Exception:
            pass

    return []
