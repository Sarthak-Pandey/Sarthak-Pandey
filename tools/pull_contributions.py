import json
import re
from pathlib import Path

import httpx
from lxml import html

# -------------------------------
# CHANGE THIS TO YOUR USERNAME
# -------------------------------
USERNAME = "Sarthak-Pandey"

URL = f"https://github.com/users/Sarthak-Pandey/contributions"

OUTPUT = Path("assets/contributions.json")


def fetch_contributions():

    print(f"Fetching contributions for {USERNAME}...")

    response = httpx.get(URL, timeout=30)

    response.raise_for_status()

    tree = html.fromstring(response.text)

    days = tree.xpath("//td[@data-date]")
    tooltips = tree.xpath("//tool-tip[@for]")

    # Map from element ID to contribution count
    counts = {}
    for tooltip in tooltips:
        for_id = tooltip.get("for")
        text = tooltip.text_content().strip()
        if text.startswith("No "):
            count = 0
        else:
            match = re.match(r"^(\d+)", text)
            count = int(match.group(1)) if match else 0
        counts[for_id] = count

    contributions = []
    total = 0

    for day in days:

        date = day.get("data-date")
        level = int(day.get("data-level", "0"))
        day_id = day.get("id")
        count = counts.get(day_id, 0)

        contributions.append(
            {
                "date": date,
                "count": count,
                "level": level,
            }
        )

        total += count

    OUTPUT.parent.mkdir(exist_ok=True)

    with open(OUTPUT, "w") as f:
        json.dump(contributions, f, indent=4)

    print(f"Saved {len(contributions)} days")
    print(f"Total Contributions : {total}")
    print(f"Output -> {OUTPUT}")


if __name__ == "__main__":
    fetch_contributions()