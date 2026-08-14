from pathlib import Path

import yaml

from opsrag.ingestion.models import Document
from opsrag.ingestion.metadata import infer_metadata_from_path
from opsrag.ingestion.utils import (
    calculate_checksum,
    generate_document_id
)

class YAMLParser():
    def parse(self, path: Path, root: Path) -> Document:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        checksum = calculate_checksum(content)

        inferred_metadata = infer_metadata_from_path(path=path, root=root)
        metadata = extract_yaml_metadata(content)

        metadata = inferred_metadata | metadata

        source = path.relative_to(root).as_posix()
        document_id = generate_document_id(source)

        return Document(
            id=document_id,
            content=content,
            source=source,
            file_name=path.name,
            file_type="yaml",
            domain=metadata.get("domain"),
            document_type=metadata.get("document_type"),
            environment=metadata.get("environment"),
            service=metadata.get("service"),
            status=metadata.get("status"),
            checksum=checksum,
            metadata=metadata
        )


def extract_yaml_metadata(content: str) -> dict:
    yaml_content = yaml.safe_load(content) or {}

    if not isinstance(yaml_content, dict):
       return {}

    yaml_metadata = yaml_content.get("metadata")

    metadata_section = yaml_metadata if isinstance(yaml_metadata, dict) else {}

    metadata_dict = {
        "api_version": yaml_content.get("apiVersion"),
        "kubernetes_kind": yaml_content.get("kind"),
        "resource_name": metadata_section.get("name"),
        "namespace": metadata_section.get("namespace")
    }

    cleaned_dict = {k: v for k, v in metadata_dict.items() if v is not None}

    return cleaned_dict