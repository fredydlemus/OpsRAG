from opsrag.ingestion.parsers.base import DocumentParser
from opsrag.ingestion.parsers.markdown import MarkdownParser
from opsrag.ingestion.parsers.terraform import TerraformParser
from opsrag.ingestion.parsers.text import TextParser
from opsrag.ingestion.parsers.yaml_parser import YAMLParser
from pathlib import Path

PARSERS_DICT = {
    "md": MarkdownParser,
    "tf": TerraformParser,
    "log": TextParser,
    "txt": TextParser,
    "yml": YAMLParser,
    "yaml": YAMLParser
}

def get_parser(path: Path) -> DocumentParser:
    file_type = path.suffix.lower()[1:]

    parser = PARSERS_DICT.get(file_type)

    if parser is None:
        raise ValueError(
            f"Unsupported file type: {file_type}"
        )

    return parser()