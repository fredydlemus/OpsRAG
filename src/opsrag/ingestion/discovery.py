from pathlib import Path

SUPPORTED_EXTENSIONS = [".md", ".yaml", ".yml", ".tf", ".log", ".txt", ".json"]

def discover_files(root: Path) -> list[Path]:
    files = [
        file for file in root.rglob("*") 
        if file.is_file()
        and not any(path.startswith(".") for path in file.relative_to(root).parts)
        and file.suffix.lower() in SUPPORTED_EXTENSIONS]

    return sorted(files)
