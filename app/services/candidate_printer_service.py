from datetime import datetime

from app.services.gap_calculator import GapCalculator
from app.services.experience_formatter import ExperienceFormatter

class CandidatePrinterService:
    @staticmethod
    def print_candidate(candidate):
        name = "Unknown"
        if candidate.contact_info and candidate.contact_info.name and getattr(candidate.contact_info.name, "formatted_name", None):
            name = candidate.contact_info.name.formatted_name
        print(f"Hello {name},")
        experiences = candidate.experience or []
        if not experiences:
            print("No professional experience records found.\n")
            return
        # Sort by start date ascending
        sorted_exps = [exp for exp in experiences if exp.start_date and exp.end_date]
        sorted_exps.sort(key=lambda e: datetime.strptime(e.start_date, "%b/%d/%Y"))
        # Calculate gaps
        gaps = GapCalculator.calculate_gaps(sorted_exps)
        # Print in reverse (newest first)
        idx_gap = len(gaps) - 1
        for idx in range(len(sorted_exps) - 1, -1, -1):
            exp = sorted_exps[idx]
            print(ExperienceFormatter.format_experience(exp))
            if idx - 1 >= 0 and idx_gap >= 0:
                gap = gaps[idx_gap]
                if gap[2] > 0:
                    print(ExperienceFormatter.format_gap(gap[2]))
                idx_gap -= 1
        print()
