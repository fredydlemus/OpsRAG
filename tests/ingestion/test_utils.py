from opsrag.ingestion.utils import generate_document_id

def test_generate_document_id_same_source_same_id():
    assert generate_document_id("eks/runbook.md") == generate_document_id("eks/runbook.md")

def test_generate_document_id_different_source_different_id():
    assert generate_document_id("eks/runbook.md") != generate_document_id("kafka/runbook.md")

def test_generate_document_id_type():
    assert isinstance(generate_document_id("eks/runbook.md"), str)