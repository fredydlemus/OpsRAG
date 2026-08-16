from pathlib import Path

from opsrag.ingestion.models import Document
from opsrag.ingestion.metadata import infer_metadata_from_path
from opsrag.ingestion.utils import (
    calculate_checksum,
    generate_document_id
)

FILE_TYPES = {
    "log": "log",
    "txt": "text"
}

class TextParser:
    def parse(self, path: Path, root: Path) -> Document:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        checksum = calculate_checksum(content)

        inferred_metadata = infer_metadata_from_path(path=path, root=root)

        source = path.relative_to(root).as_posix()
        document_id = generate_document_id(source)

        file_type = path.suffix.lower()[1:]

        return Document(
            id=document_id,
            content=content,
            source=source,
            file_name=path.name,
            file_type=FILE_TYPES[file_type],
            domain=inferred_metadata.get("domain"),
            document_type=inferred_metadata.get("document_type"),
            environment=inferred_metadata.get("environment"),
            service=inferred_metadata.get("service"),
            status=inferred_metadata.get("status"),
            checksum=checksum,
            metadata=inferred_metadata
        )