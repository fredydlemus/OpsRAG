from pathlib import Path
from opsrag.ingestion.models import IngestionResult, IngestionError
from opsrag.ingestion.discovery import discover_files
from opsrag.ingestion.parsers.selector import get_parser
import yaml

def ingest_directory(root: Path) -> IngestionResult:
    files = discover_files(root)

    ingestion_results = IngestionResult()

    for file in files:
        try:
            parser = get_parser(file)
            document = parser.parse(file, root)
            ingestion_results.documents.append(document)
        except (ValueError, yaml.YAMLError, UnicodeDecodeError, OSError) as e:
            ingestion_error = IngestionError(
                source=file.relative_to(root).as_posix(),
                error=str(e)
            )
            ingestion_results.errors.append(ingestion_error)

    return ingestion_results