import re
import yaml
from pathlib import Path

from opsrag.ingestion.models import Document
from opsrag.ingestion.utils import (
    calculate_checksum,
    generate_document_id
)

class MarkdownParser:
    def parse(self, path: Path, root: Path) -> Document:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        checksum = calculate_checksum(content)
        metadata, body = extract_frontmatter(content)

        source = path.relative_to(root).as_posix()
        document_id = generate_document_id(source)

        return Document(
            id=document_id,
            content=body,
            source=source,
            file_name=path.name,
            file_type="markdown",
            domain=metadata.get("domain"),
            document_type=metadata.get("document_type"),
            environment=metadata.get("environment"),
            service=metadata.get("service"),
            status=metadata.get("status"),
            checksum=checksum,
            metadata=metadata
        )

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