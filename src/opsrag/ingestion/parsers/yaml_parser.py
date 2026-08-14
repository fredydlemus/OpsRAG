from pathlib import Path

import yaml

from opsrag.ingestion.models import Document

class YAMLParser():
    def parse(self, path: Path, root: Path) -> Document:
        ...

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