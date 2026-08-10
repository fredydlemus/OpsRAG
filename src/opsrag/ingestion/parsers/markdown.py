import re
import yaml
from pathlib import Path

from opsrag.ingestion.models import Document

class MarkdownParser:
    def parse(self, path: Path, root: Path) -> Document:
        ...

def extract_frontmatter(content: str) -> tuple[dict, str]:
    pattern = r"^---\s*\n(.*?)\n---\s*\n?(.*)$"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        frontmatter_raw = match.group(1)
        body = match.group(2)

        frontmatter_dict = yaml.safe_load(frontmatter_raw) or {}

        if not isinstance(frontmatter_dict, dict):
            raise ValueError(
                f"Invalid frontmatter: Expected a YAML dictionary, but got {type(frontmatter_dict).__name__} ('{frontmatter_raw}')."
            )

        return (frontmatter_dict, body)

    return ({}, content)