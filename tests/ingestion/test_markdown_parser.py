import textwrap
from opsrag.ingestion.parsers.markdown import extract_frontmatter, MarkdownParser
from opsrag.ingestion.utils import calculate_checksum, generate_document_id
import pytest

def test_extract_frontmatter_valid_frontmatter():
    content = """---
domain: kafka
status: current
---
# Runbook Hello"""
    metadata, body = extract_frontmatter(content)
    assert metadata["domain"] == "kafka"
    assert metadata["status"] == "current"
    assert body == "# Runbook Hello"

def test_extract_frontmatter_without_frontmatter():
    content = """
# Runbook Hello"""
    metadata, body = extract_frontmatter(content)
    assert metadata== {}
    assert body == "\n# Runbook Hello"

def test_extract_frontmatter_empty_frontmatter():
    content = """---

---
# Runbook Hello"""
    metadata, body = extract_frontmatter(content)
    assert metadata== {}
    assert body == "# Runbook Hello"

def test_extract_frontmatter_frontmatter_not_dict():
    content = """---
hello
---
# Runbook Hello"""
    with pytest.raises(ValueError):
        extract_frontmatter(content)

def test_extract_frontmatter_separator_inside_body_is_not_frontmatter():
    content = """
    # Runbook

Some text

---

More text
    """

    metadata, body = extract_frontmatter(content)

    assert metadata== {}
    assert body == """
    # Runbook

Some text

---

More text
    """

def test_parse_a_md_file_correctly(tmp_path):

    md_content = textwrap.dedent("""\
    ---
    domain: kafka
    document_type: runbook
    status: current
    ---
    # Runbook content.
    """)

    kafka_dir = tmp_path / "kafka"
    kafka_dir.mkdir()
    runbook_file = kafka_dir / "runbook.md"
    runbook_file.write_text(md_content, encoding="utf-8")

    parser = MarkdownParser()
    document = parser.parse(runbook_file, tmp_path)

    assert document.source == "kafka/runbook.md"
    assert document.file_name == "runbook.md"
    assert document.file_type == "markdown"

    assert document.domain == "kafka"
    assert document.document_type == "runbook"
    assert document.status == "current"    

def test_frontmatter_should_not_be_in_content(tmp_path):
    md_content = textwrap.dedent("""\
    ---
    domain: kafka
    ---
    # Runbook content.
    """)

    runbook_file = tmp_path / "runbook.md"
    runbook_file.write_text(md_content, encoding="utf-8")

    parser = MarkdownParser()
    document = parser.parse(runbook_file, tmp_path)

    assert document.content.strip() == "# Runbook content."

def test_document_checksum_is_calculated_from_raw_content(tmp_path):
    md_content = textwrap.dedent("""\
    ---
    domain: kafka
    ---
    # Runbook content.
    """)

    runbook_file = tmp_path / "runbook.md"
    runbook_file.write_text(md_content, encoding="utf-8")

    parser = MarkdownParser()
    document = parser.parse(runbook_file, tmp_path)

    assert document.checksum == calculate_checksum(md_content)

def test_document_id_is_generated_from_source(tmp_path):
    md_content = textwrap.dedent("""\
    ---
    domain: kafka
    ---
    # Runbook content.
    """)

    runbook_file = tmp_path / "runbook.md"
    runbook_file.write_text(md_content, encoding="utf-8")

    parser = MarkdownParser()
    document = parser.parse(runbook_file, tmp_path)

    assert document.id == generate_document_id(runbook_file.relative_to(tmp_path).as_posix())

def test_document_without_frontmatter(tmp_path):
    md_content = textwrap.dedent("""\
    # Simple Runbook

    Hello
    """)

    runbook_file = tmp_path / "runbook.md"
    runbook_file.write_text(md_content, encoding="utf-8")

    parser = MarkdownParser()
    document = parser.parse(runbook_file, tmp_path)

    assert document.metadata == {}
    assert document.domain is None
    assert document.content == md_content