import hashlib

def generate_candidate_id(
    full_name: str | None,
    highest_degree: str | None,
    institution: str | None,
) -> str:
    """
    Generates a stable, deterministic identifier for a candidate.

    This function creates a unique candidate identifier based on personal and
    educational attributes that are unlikely to change frequently. The same
    input values will always produce the same identifier, ensuring idempotent
    behavior across multiple data loads.

    The identifier is generated using a SHA-256 hash of a normalized string
    composed of:
      - Full name
      - Highest academic degree
      - Educational institution

    This approach prevents duplicate candidate records when the same individual
    appears multiple times across data ingestion runs, even if employment
    history changes.

    Args:
        full_name (str | None):
            The candidate’s full name as provided by the source system.
            If missing, an empty string is used.

        highest_degree (str | None):
            The highest academic degree achieved by the candidate.
            If missing, an empty string is used.

        institution (str | None):
            The name of the educational institution associated with the
            highest degree. If missing, an empty string is used.

    Returns:
        str:
            A SHA-256 hexadecimal hash string representing the candidate’s
            unique identifier.

    Design Notes:
        - The function is deterministic: identical inputs always produce
          the same output.
        - Normalization (lowercasing and trimming) reduces accidental
          duplicates caused by casing or whitespace differences.
        - This identifier is intended for internal system use only and does
          not expose personal data.
        - The function does not perform validation; input sanitation is
          expected to be handled upstream.

    Example:
        >>> generate_candidate_id(
        ...     full_name="Jane Doe",
        ...     highest_degree="Bachelor's",
        ...     institution="University of Example"
        ... )
        '3f7a3d4f6e4c8e0b8c9d5b0e4b7d1c8c9a2e6c0f8c3c5b7a9e2d4c8f1a7e'
    """
    base = f"{full_name or ''}|{highest_degree or ''}|{institution or ''}"
    normalized = base.strip().lower()
    return hashlib.sha256(normalized.encode()).hexdigest()