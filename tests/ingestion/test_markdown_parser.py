from opsrag.ingestion.parsers.markdown import extract_frontmatter
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