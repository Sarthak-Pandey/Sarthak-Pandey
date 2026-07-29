import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from living_terminal.stats import calculate_stats


def test_calculate_stats():
    sample_contributions = [
        {"date": "2026-01-01", "count": 5, "level": 2},
        {"date": "2026-01-02", "count": 10, "level": 4},
        {"date": "2026-01-03", "count": 0, "level": 0},
        {"date": "2026-01-04", "count": 3, "level": 1},
    ]
    user_info = {"public_repos": 15, "followers": 20, "following": 12}

    stats = calculate_stats(sample_contributions, user_info)

    assert stats.public_repos == 15
    assert stats.followers == 20
    assert stats.total_contributions == 18
    assert stats.average_commits_per_active_day == 6.0  # 18 / 3 active days
    assert stats.most_active_day == "2026-01-02"
    assert stats.most_active_count == 10
    assert stats.longest_streak == 2
    assert 0.0 <= stats.heat_score <= 100.0
