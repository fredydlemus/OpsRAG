from pathlib import Path
from opsrag.ingestion.metadata import infer_metadata_from_path

def test_should_infer_domain_in_base_of_path():
    path = Path("knowledge-base/kafka/runbook.md")
    root = Path("knowledge-base")

    metadata = infer_metadata_from_path(path=path, root=root)

    assert metadata == {"domain": "kafka"}

def test_should_infer_domain_in_base_of_path_with_two_directories():
    path = Path("knowledge-base/kafka/runbooks/high-cpu.md")
    root = Path("knowledge-base")

    metadata = infer_metadata_from_path(path=path, root=root)

    assert metadata == {"domain": "kafka"}

def test_should_not_infer_domain_when_there_is_not_directory_between_root_and_file():
    path = Path("knowledge-base/readme.md")
    root = Path("knowledge-base")

    metadata = infer_metadata_from_path(path=path, root=root)

    assert metadata == {}