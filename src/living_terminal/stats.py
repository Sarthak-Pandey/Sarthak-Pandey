from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass
class GitHubStats:
    public_repos: int
    followers: int
    following: int
    total_contributions: int
    current_streak: int
    longest_streak: int
    most_active_day: str
    most_active_count: int
    average_commits_per_active_day: float
    heat_score: float

    @property
    def heat_score_display(self) -> str:
        return f"{self.heat_score:.1f} / 100"


def calculate_stats(
    contributions: List[Dict[str, Any]],
    user_info: Dict[str, Any] | None = None
) -> GitHubStats:
    if user_info is None:
        user_info = {}

    public_repos = user_info.get("public_repos", 12)
    followers = user_info.get("followers", 15)
    following = user_info.get("following", 10)

    if not contributions:
        return GitHubStats(
            public_repos=public_repos,
            followers=followers,
            following=following,
            total_contributions=0,
            current_streak=0,
            longest_streak=0,
            most_active_day="N/A",
            most_active_count=0,
            average_commits_per_active_day=0.0,
            heat_score=0.0,
        )

    # Sort contributions chronologically by date
    sorted_days = sorted(contributions, key=lambda d: d.get("date", ""))

    total_contributions = sum(d.get("count", 0) for d in sorted_days)

    active_days = [d for d in sorted_days if d.get("count", 0) > 0]
    num_active_days = len(active_days)

    if num_active_days > 0:
        avg_commits = total_contributions / num_active_days
    else:
        avg_commits = 0.0

    # Most active day
    max_day = max(sorted_days, key=lambda d: d.get("count", 0)) if sorted_days else {}
    most_active_day = max_day.get("date", "N/A")
    most_active_count = max_day.get("count", 0)

    # Longest streak calculation
    longest_streak = 0
    curr_streak = 0
    for d in sorted_days:
        if d.get("count", 0) > 0:
            curr_streak += 1
            if curr_streak > longest_streak:
                longest_streak = curr_streak
        else:
            curr_streak = 0

    # Current streak calculation (working backwards from latest day)
    current_streak = 0
    rev_days = list(reversed(sorted_days))
    # If today's count is 0, check if yesterday was active to allow ongoing streak today
    start_idx = 0
    if rev_days and rev_days[0].get("count", 0) == 0:
        if len(rev_days) > 1 and rev_days[1].get("count", 0) > 0:
            start_idx = 1

    for d in rev_days[start_idx:]:
        if d.get("count", 0) > 0:
            current_streak += 1
        else:
            break

    # Contribution Heat Score (0.0 to 100.0)
    # Factor 1: Total commits density (up to 40 pts)
    density_score = min(40.0, (total_contributions / 300.0) * 40.0)
    # Factor 2: Active days ratio (up to 30 pts)
    ratio_score = min(30.0, (num_active_days / max(1, len(sorted_days))) * 30.0 * 2.5)
    # Factor 3: Streak persistence (up to 30 pts)
    streak_score = min(30.0, (longest_streak / 30.0) * 30.0)

    heat_score = min(100.0, round(density_score + ratio_score + streak_score, 1))

    return GitHubStats(
        public_repos=public_repos,
        followers=followers,
        following=following,
        total_contributions=total_contributions,
        current_streak=current_streak,
        longest_streak=longest_streak,
        most_active_day=most_active_day,
        most_active_count=most_active_count,
        average_commits_per_active_day=round(avg_commits, 2),
        heat_score=heat_score,
    )
