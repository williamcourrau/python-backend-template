from datetime import datetime, timedelta
from typing import List, Tuple
from app.models.candidate_entity import Experience
from app.config.logging import get_logger

logger = get_logger(__name__)

class GapCalculatorService:
    """
        Service responsible for calculating employment gaps between professional experiences.

        This class:
        - Parses start and end dates safely
        - Handles 'present' / 'current' values
        - Ignores invalid or overlapping experiences
        - Applies a configurable minimum gap threshold
        - Returns structured gap information for downstream formatting

        It does NOT:
        - Format output for display
        - Print results
        - Persist data
        - Fetch external data
    """
    DATE_FORMAT = "%b/%d/%Y"

    @staticmethod
    def _parse_date(value: str | None) -> datetime | None:
        if not value:
            return None

        if value.lower() in {"present", "current"}:
            return datetime.today()

        try:
            return datetime.strptime(value, GapCalculatorService.DATE_FORMAT)
        except ValueError:
            logger.warning("Unable to parse date value: '%s'", value)
            return None

    @staticmethod
    def calculate_gaps(
        experiences: List[Experience],
        min_gap_days: int = 1,
    ) -> List[Tuple[datetime, datetime, int]]:
        """
        Calculates employment gaps between experiences.
        Returns a list of (gap_start, gap_end, gap_days).
        """

        if not experiences:
            logger.info("No experiences provided; skipping gap calculation")
            return []

        parsed = []

        for exp in experiences:
            start = GapCalculatorService._parse_date(exp.start_date)
            end = GapCalculatorService._parse_date(exp.end_date)

            if not start or not end:
                logger.info(
                    "Skipping experience due to missing dates: start=%s end=%s",
                    exp.start_date,
                    exp.end_date,
                )
                continue

            if end < start:
                logger.warning(
                    "Invalid experience dates (end before start): start=%s end=%s",
                    exp.start_date,
                    exp.end_date,
                )
                continue

            parsed.append((start, end))

        if len(parsed) < 2:
            logger.info(
                "Not enough valid experiences to calculate gaps (count=%d)",
                len(parsed),
            )
            return []

        parsed.sort(key=lambda x: x[0])

        gaps = []

        for i in range(len(parsed) - 1):
            prev_end = parsed[i][1]
            next_start = parsed[i + 1][0]

            # Overlapping or same-day transitions
            if next_start <= prev_end:
                logger.debug(
                    "Overlapping or adjacent jobs detected: prev_end=%s next_start=%s",
                    prev_end,
                    next_start,
                )
                continue

            gap_days = (next_start - prev_end).days - 1

            if gap_days < min_gap_days:
                logger.debug(
                    "Gap ignored (below threshold): %d days", gap_days
                )
                continue

            gap_start = prev_end + timedelta(days=1)
            gap_end = next_start - timedelta(days=1)

            logger.info(
                "Employment gap detected: %s → %s (%d days)",
                gap_start.date(),
                gap_end.date(),
                gap_days,
            )

            gaps.append((gap_start, gap_end, gap_days))

        return gaps
