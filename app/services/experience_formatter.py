from typing import Any
from datetime import datetime
from app.models.candidate_entity import Experience

class ExperienceFormatter:
    @staticmethod
    def format_experience(exp: Experience) -> str:
        title = exp.title or "Unknown"
        start = exp.start_date or "?"
        end = exp.end_date or "?"
        loc = exp.location
        if loc:
            if hasattr(loc, "short_display_address") and getattr(loc, "short_display_address"):
                loc_str = getattr(loc, "short_display_address")
            else:
                municipality = getattr(loc, "municipality", None)
                region = getattr(loc, "region", None)
                country = getattr(loc, "country_code", None)
                parts = [p for p in [municipality, region, country] if p]
                loc_str = ", ".join(parts) if parts else "Unknown location"
        else:
            loc_str = "Unknown location"
        return f"Worked as : {title}, From {start} To {end} in {loc_str}"

    @staticmethod
    def format_gap(gap_days: int) -> str:
        return f"Gap in CV for {gap_days} days"
