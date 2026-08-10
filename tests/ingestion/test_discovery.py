from opsrag.ingestion.discovery import discover_files

def test_discover_files_recursive(tmp_path):
    kafka_dir = tmp_path / "kafka"
    kafka_dir.mkdir()
    runbook_file = kafka_dir / "runbook.md"
    runbook_file.write_text("# Runbook content.")

    result = discover_files(tmp_path)
    assert result == [runbook_file]


def test_discover_files_ignores_unsupported_extension(tmp_path):
    unsupported_file = tmp_path / "config.pdf"
    unsupported_file.write_text("# PDF Content.")

    result = discover_files(tmp_path)
    assert result == []

def test_discover_files_ignore_hidden_paths(tmp_path):
    hidden_dir = tmp_path / ".hidden"
    hidden_dir.mkdir()
    file_in_hidden_dir = hidden_dir / "runbook.md"
    file_in_hidden_dir.write_text("# Hidden")

    hidden_file = tmp_path / ".secret.md"
    hidden_file.write_text("# Secret")

    result = discover_files(tmp_path)
    assert result == []

def test_discover_files_sorted(tmp_path):
    file1 = tmp_path / "z.log"
    file1.write_text("1")

    file2 = tmp_path / "a.md"
    file2.write_text("2")

    file3 = tmp_path / "m.yaml"
    file3.write_text("3")

    discover = discover_files(tmp_path)

    assert discover == [file2, file3, file1]