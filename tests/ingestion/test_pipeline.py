from opsrag.ingestion.pipeline import ingest_directory

def test_should_process_valid_documents(tmp_path):
    YAML_content = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
  namespace: prod
"""

    markdown_content = """---
domain: kafka
status: current
---
# Runbook Hello"""

    kafka_dir = tmp_path / "kafka"
    kafka_dir.mkdir()
    runbook_file = kafka_dir / "runbook.md"
    runbook_file.write_text(markdown_content, encoding="utf-8")
    deployment_file = kafka_dir / "deployment.yml"
    deployment_file.write_text(YAML_content, encoding="utf-8")

    ingestion_result = ingest_directory(tmp_path)

    assert len(ingestion_result.documents) == 2
    assert len(ingestion_result.errors) == 0

def test_should_handle_invalid_documents(tmp_path):
    YAML_content = """
[
"""

    markdown_content = """---
domain: kafka
status: current
---
# Runbook Hello"""

    kafka_dir = tmp_path / "kafka"
    kafka_dir.mkdir()
    runbook_file = kafka_dir / "runbook.md"
    runbook_file.write_text(markdown_content, encoding="utf-8")
    deployment_file = kafka_dir / "deployment.yml"
    deployment_file.write_text(YAML_content, encoding="utf-8")

    ingestion_result = ingest_directory(tmp_path)

    assert len(ingestion_result.documents) == 1
    assert len(ingestion_result.errors) == 1

def test_an_error_should_preserve_the_correct_source(tmp_path):
    YAML_content = """
[
"""

    markdown_content = """---
domain: kafka
status: current
---
# Runbook Hello"""

    kafka_dir = tmp_path / "kafka"
    kafka_dir.mkdir()
    runbook_file = kafka_dir / "runbook.md"
    runbook_file.write_text(markdown_content, encoding="utf-8")
    deployment_file = kafka_dir / "deployment.yml"
    deployment_file.write_text(YAML_content, encoding="utf-8")

    ingestion_result = ingest_directory(tmp_path)

    assert ingestion_result.errors[0].source == "kafka/deployment.yml"

def test_should_produce_deterministic_ingestion_result(tmp_path):
    YAML_content = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
  namespace: prod
"""

    markdown_content = """---
domain: kafka
status: current
---
# Runbook Hello"""

    kafka_dir = tmp_path / "kafka"
    kafka_dir.mkdir()
    runbook_file = kafka_dir / "runbook.md"
    runbook_file.write_text(markdown_content, encoding="utf-8")
    deployment_file = kafka_dir / "deployment.yml"
    deployment_file.write_text(YAML_content, encoding="utf-8")

    first = ingest_directory(tmp_path)
    second = ingest_directory(tmp_path)

    first_sources = [document.source for document in first.documents]
    second_sources = [document.source for document in second.documents]

    first_ids = [document.id for document in first.documents]
    second_ids = [document.id for document in second.documents]

    first_checksums = [document.checksum for document in first.documents]
    second_checksums = [document.checksum for document in second.documents]

    assert first_sources == second_sources
    assert first_ids == second_ids
    assert first_checksums == second_checksums