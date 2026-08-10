from opsrag.ingestion.utils import generate_document_id, calculate_checksum

def test_generate_document_id_same_source_same_id():
    assert generate_document_id("eks/runbook.md") == generate_document_id("eks/runbook.md")

def test_generate_document_id_different_source_different_id():
    assert generate_document_id("eks/runbook.md") != generate_document_id("kafka/runbook.md")

def test_generate_document_id_type():
    assert isinstance(generate_document_id("eks/runbook.md"), str)

def test_calculate_checksum_type():
    assert isinstance(calculate_checksum("Hello, world!"), str)

def test_calculate_checksum_same_content_same_checksum():
    assert calculate_checksum("Hello, world!") == calculate_checksum("Hello, world!")

def test_calculate_checksum_different_content_different_checksum():
    assert calculate_checksum("Hello, world!") != calculate_checksum("Hello, world!2")