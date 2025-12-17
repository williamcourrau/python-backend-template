from datetime import datetime, timedelta
from typing import List, Tuple, Optional
from app.models.candidate_entity import Experience

class GapCalculator:
    @staticmethod
    def calculate_gaps(experiences: List[Experience]) -> List[Tuple[datetime, datetime, int]]:
        """
        Returns a list of (gap_start, gap_end, gap_days) tuples for gaps > 0 days.
        gap_start: first day of the gap
        gap_end: last day before next job
        gap_days: number of days in the gap
        """
        exps = []
        for exp in experiences:
            if exp.start_date and exp.end_date:
                try:
                    start = datetime.strptime(exp.start_date, "%b/%d/%Y")
                    end = datetime.strptime(exp.end_date, "%b/%d/%Y")
                    exps.append((start, end, exp))
                except Exception:
                    continue
        if len(exps) < 2:
            return []
        exps.sort(key=lambda x: x[0])
        gaps = []
        for i in range(len(exps) - 1):
            prev_end = exps[i][1]
            next_start = exps[i + 1][0]
            gap_days = (next_start - prev_end).days - 1
            if gap_days > 0:
                gaps.append((prev_end + timedelta(days=1), next_start - timedelta(days=1), gap_days))
        return gaps