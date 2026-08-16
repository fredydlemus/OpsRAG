from opsrag.ingestion.parsers.text import TextParser
from opsrag.ingestion.utils import calculate_checksum, generate_document_id

def test_should_parse_a_log_file_correctly(tmp_path):
    content = """
    connect ETIMEDOUT 10.0.12.31:5432
Connection refused
    """

    log_dir = tmp_path / "kafka"
    log_dir.mkdir()
    file = log_dir / "kafka.log"
    file.write_text(content, encoding="utf-8")

    parser = TextParser()
    document = parser.parse(file, tmp_path)

    assert document.content == content
    assert document.domain == "kafka"
    assert document.source == "kafka/kafka.log"
    assert document.file_type == "log"

def test_document_checksum_is_calculated_from_raw_content(tmp_path):
    content = """
    connect ETIMEDOUT 10.0.12.31:5432
Connection refused
    """

    log_dir = tmp_path / "kafka"
    log_dir.mkdir()
    file = log_dir / "kafka.log"
    file.write_text(content, encoding="utf-8")

    parser = TextParser()
    document = parser.parse(file, tmp_path)

    assert document.checksum == calculate_checksum(content)

def test_document_id_is_generated_from_source(tmp_path):
    content = """
    connect ETIMEDOUT 10.0.12.31:5432
Connection refused
    """

    log_dir = tmp_path / "kafka"
    log_dir.mkdir()
    file = log_dir / "kafka.log"
    file.write_text(content, encoding="utf-8")

    parser = TextParser()
    document = parser.parse(file, tmp_path)

    assert document.id == generate_document_id(file.relative_to(tmp_path).as_posix())

def test_should_parse_a_text_file_correctly(tmp_path):
    content = """
    connect ETIMEDOUT 10.0.12.31:5432
Connection refused
    """

    log_dir = tmp_path / "kafka"
    log_dir.mkdir()
    file = log_dir / "kafka.txt"
    file.write_text(content, encoding="utf-8")

    parser = TextParser()
    document = parser.parse(file, tmp_path)

    assert document.content == content
    assert document.domain == "kafka"
    assert document.source == "kafka/kafka.txt"
    assert document.file_type == "text"