from typing import List
from datetime import datetime
from app.models.candidate_entity import Candidate
from app.services.gap_calculator_service import GapCalculatorService
from app.services.experience_formatter import ExperienceFormatter
from app.config.logging import get_logger

logger = get_logger(__name__)

class CandidatePresenterService:
    """
    Transforms a Candidate into printable text lines.
    """

    def __init__(
        self,
        gap_calculator: GapCalculatorService,
        formatter: ExperienceFormatter,
    ):
        self._gap_calculator = gap_calculator
        self._formatter = formatter

    def build_lines(self, candidate: Candidate) -> str:
        lines: List[str] = []

        name = (
            candidate.contact_info.name.formatted_name
            if candidate.contact_info and candidate.contact_info.name
            else "Unknown"
        )

        lines.append(f"Hello {name},")
        lines.append("")  # blank line after greeting

        experiences = candidate.experience or []
        if not experiences:
            lines.append("No professional experience records found.")
            return "\n".join(lines)

        valid_exps = []
        for exp in experiences:
            try:
                if exp.start_date and exp.end_date:
                    datetime.strptime(exp.start_date, "%b/%d/%Y")
                    datetime.strptime(exp.end_date, "%b/%d/%Y")
                    valid_exps.append(exp)
            except Exception:
                logger.warning("Skipping experience with invalid dates: %s", exp)

        if not valid_exps:
            lines.append("No valid professional experience records found.")
            return "\n".join(lines)

        valid_exps.sort(
            key=lambda e: datetime.strptime(e.start_date, "%b/%d/%Y")
        )

        gaps = self._gap_calculator.calculate_gaps(valid_exps)

        for idx, exp in enumerate(valid_exps):
            lines.append(self._formatter.format_experience(exp))

            if idx < len(gaps):
                _, _, gap_days = gaps[idx]
                if gap_days > 0:
                    lines.append(self._formatter.format_gap(gap_days))

        return "\n".join(lines)

