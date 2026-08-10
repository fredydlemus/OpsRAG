from pathlib import Path
from typing import Protocol

from opsrag.ingestion.models import Document

class DocumentParser(Protocol):
    def parse(self, path: Path, root: Path) -> Document:
        pass