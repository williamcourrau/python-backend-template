import argparse
from typing import List

from app.models.dto.filter_params import CandidateFilterParams
from app.entry_points.exceptions import InvalidCliArguments

class CliArgumentParser:
    def parse_filter_arguments(
        self,
        raw_args: list[str],
    ) -> CandidateFilterParams:

        parser = argparse.ArgumentParser(
            description="Filter candidates"
        )

        parser.add_argument("--industry", type=str)

        parser.add_argument(
            "--skills",
            nargs="*",
            help="Space-separated list of skills (e.g. --skills python sql)",
        )

        parser.add_argument(
            "--min-experience",
            type=int,
            default=0,
            help="Minimum years of experience (>= 0)",
        )

        args = parser.parse_args(raw_args)

        skills = self._validate_skills(args.skills)
        min_years = self._validate_min_experience(args.min_experience)

        return CandidateFilterParams(
            industry=args.industry,
            skills=skills,
            min_years_experience=min_years,
        )

    def _validate_skills(self, skills: List[str] | None) -> List[str] | None:
        if skills is None:
            return None

        if not isinstance(skills, list):
            raise InvalidCliArguments(
                "--skills must be separated by commas and wrapped into double quotes. E.g. --skills \"python, sql, aws\""
            )

        normalized: List[str] = []
        for s in skills:
            if not isinstance(s, str):
                raise InvalidCliArguments(
                    f"Invalid skill value '{s}'. Skills must be wrapped into double quotes. E.g. --skills \"python, sql, aws\""
                )
            if s.strip():
                normalized.append(s.strip().lower())

        return normalized or None

    def _validate_min_experience(self, value: int) -> int | None:
        if value < 0:
            raise InvalidCliArguments(
                "--min-experience must start from 0. Not valid negative years of experience."
            )

        return value if value > 0 else None
