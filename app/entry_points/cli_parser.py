import argparse
from app.models.dto.filter_params import CandidateFilterParams


class CliArgumentParser:
    def parse(self) -> CandidateFilterParams:
        parser = argparse.ArgumentParser(
            description="Candidate filtering service"
        )

        parser.add_argument("--industry", type=str)
        parser.add_argument("--skills", nargs="*")
        parser.add_argument("--min-experience", type=int, default=0)

        args = parser.parse_args()

        return CandidateFilterParams(
            industry=args.industry,
            skills=args.skills or None,
            min_years_experience=args.min_experience if args.min_experience > 0 else None,
        )