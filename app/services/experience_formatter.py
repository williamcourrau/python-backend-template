from typing import Any
from app.models.candidate_entity import Experience
from app.config.logging import get_logger

logger = get_logger(__name__)

class ExperienceFormatter:
    """
        Responsible for converting Experience domain objects into human-readable text.

        This class focuses exclusively on presentation logic and is designed to:
        - Be resilient to incomplete or malformed data
        - Produce recruiter-friendly (HR-friendly) output
        - Avoid raising exceptions during formatting
        - Log technical issues for debugging purposes

        It does NOT:
        - Parse dates
        - Perform business logic
        - Access external services
    """
    @staticmethod
    def format_experience(exp: Experience) -> str:
        if not exp:
            logger.warning("Attempted to format a null Experience object")
            return "Employment details are unavailable"

        title = exp.title.strip() if isinstance(exp.title, str) and exp.title.strip() else "Role not specified"
        start = exp.start_date.strip() if isinstance(exp.start_date, str) and exp.start_date.strip() else "Start date not specified"
        end = exp.end_date.strip() if isinstance(exp.end_date, str) and exp.end_date.strip() else "End date not specified"

        loc_str = ExperienceFormatter._format_location(exp.location)

        return f"Worked as {title}, from {start} to {end}, located in {loc_str}"

    @staticmethod
    def _format_location(location: Any) -> str:
        if not location:
            return "Location not specified"

        try:
            short = getattr(location, "short_display_address", None)
            if isinstance(short, str) and short.strip():
                return short.strip()

            municipality = getattr(location, "municipality", None)
            region = getattr(location, "region", None)
            country = getattr(location, "country_code", None)

            parts = [p.strip() for p in [municipality, region, country] if isinstance(p, str) and p.strip()]
            return ", ".join(parts) if parts else "Location not specified"

        except Exception as e:
            logger.exception("Failed to format location: %s", location)
            return "Location not specified"

    @staticmethod
    def format_gap(gap_days: int) -> str:
        """Formats a descriptive string about the employment gap.
           Added for friendlier output message for the recruiter can read clear information.
        Args:
            gap_days (int): Number of days in the employment gap.

        Returns:
            str: A descriptive string about the employment gap.
        """
        if not isinstance(gap_days, int) or gap_days <= 0:
            logger.debug("Invalid or non-positive gap_days value: %s", gap_days)
            return "No significant employment gap identified"

        if gap_days < 30:
            return f"Short career gap of approximately {gap_days} days"

        if gap_days < 180:
            return f"Career gap of approximately {gap_days} days"

        return f"Extended career gap of approximately {gap_days} days"
