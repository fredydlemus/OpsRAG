from pathlib import Path

def infer_metadata_from_path(path: Path, root: Path) -> dict[str, str]:
    parts = path.relative_to(root).parts
    
    if len(parts) <= 1:
        return {}

    domain = parts[0]

    return {
        "domain": domain
    }