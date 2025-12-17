import hashlib

def generate_candidate_id(
    full_name: str | None,
    highest_degree: str | None,
    institution: str | None,
) -> str:
    base = f"{full_name or ''}|{highest_degree or ''}|{institution or ''}"
    normalized = base.strip().lower()
    return hashlib.sha256(normalized.encode()).hexdigest()
