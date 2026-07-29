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


def test_stats_edge_cases():
    # 1. Empty contributions list
    stats_empty = calculate_stats([])
    assert stats_empty.total_contributions == 0
    assert stats_empty.current_streak == 0
    assert stats_empty.longest_streak == 0
    assert stats_empty.average_commits_per_active_day == 0.0
    assert stats_empty.heat_score == 0.0

    # 2. All zeros contributions
    stats_zeros = calculate_stats([
        {"date": "2026-01-01", "count": 0, "level": 0},
        {"date": "2026-01-02", "count": 0, "level": 0},
    ])
    assert stats_zeros.total_contributions == 0
    assert stats_zeros.current_streak == 0
    assert stats_zeros.longest_streak == 0
    assert stats_zeros.average_commits_per_active_day == 0.0

    # 3. Single day active contribution
    stats_single = calculate_stats([
        {"date": "2026-01-01", "count": 5, "level": 2},
    ])
    assert stats_single.total_contributions == 5
    assert stats_single.current_streak == 1
    assert stats_single.longest_streak == 1
    assert stats_single.average_commits_per_active_day == 5.0
