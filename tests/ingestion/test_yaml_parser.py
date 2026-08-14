from opsrag.ingestion.parsers.yaml_parser import extract_yaml_metadata, YAMLParser
import pytest
import yaml
from opsrag.ingestion.utils import calculate_checksum, generate_document_id

def test_should_extract_kubernetes_metadata():
    YAML_content = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
  namespace: prod
"""
    metadata = extract_yaml_metadata(YAML_content)
    assert metadata["api_version"] == "apps/v1"
    assert metadata["kubernetes_kind"] == "Deployment"
    assert metadata["resource_name"] == "orders-api"
    assert metadata["namespace"] == "prod"

def test_should_return_empty_dict_with_a_valid_not_kubernetes_yaml():
    YAML_content = """
rules:
  - pattern: foo
"""
    metadata = extract_yaml_metadata(YAML_content)
    assert metadata == {}

def test_should_return_empty_dict_with_a_list_in_yaml_root():
    YAML_content = """
- kafka
- eks
- lambda
"""
    metadata = extract_yaml_metadata(YAML_content)
    assert metadata == {}

def test_should_ignore_invalid_metadata_section_type():
    YAML_content = """
apiVersion: apps/v1
kind: Deployment
metadata: Metadata
"""
    metadata = extract_yaml_metadata(YAML_content)
    assert metadata["api_version"] == "apps/v1"
    assert metadata["kubernetes_kind"] == "Deployment"
    assert "resource_name" not in metadata
    assert "namespace" not in metadata

def test_should_raise_error_with_invalid_yaml():
    YAML_content = """
    [
    """

    with pytest.raises(yaml.YAMLError):
        extract_yaml_metadata(YAML_content)

def test_parse_a_yaml_file_correctly(tmp_path):
    YAML_content = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
  namespace: prod
"""

    yaml_dir = tmp_path / "eks"
    yaml_dir.mkdir()
    deployment_file = yaml_dir / "deployment.yaml"
    deployment_file.write_text(YAML_content, encoding="utf-8")

    parser = YAMLParser()
    document = parser.parse(deployment_file, tmp_path)

    assert document.file_type == "yaml"
    assert document.source == "eks/deployment.yaml"
    assert document.domain == "eks"
    assert document.metadata["resource_name"] == "orders-api"

def test_should_parse_preserve_all_yaml_content(tmp_path):
    YAML_content = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
  namespace: prod
"""

    yaml_dir = tmp_path / "eks"
    yaml_dir.mkdir()
    deployment_file = yaml_dir / "deployment.yaml"
    deployment_file.write_text(YAML_content, encoding="utf-8")

    parser = YAMLParser()
    document = parser.parse(deployment_file, tmp_path)

    assert document.content == YAML_content


def test_document_checksum_is_calculated_from_raw_content(tmp_path):
    YAML_content = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
  namespace: prod
"""

    yaml_dir = tmp_path / "eks"
    yaml_dir.mkdir()
    deployment_file = yaml_dir / "deployment.yaml"
    deployment_file.write_text(YAML_content, encoding="utf-8")

    parser = YAMLParser()
    document = parser.parse(deployment_file, tmp_path)

    assert document.checksum == calculate_checksum(YAML_content)

def test_document_id_is_generated_from_source(tmp_path):
    YAML_content = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
  namespace: prod
"""

    yaml_dir = tmp_path / "eks"
    yaml_dir.mkdir()
    deployment_file = yaml_dir / "deployment.yaml"
    deployment_file.write_text(YAML_content, encoding="utf-8")

    parser = YAMLParser()
    document = parser.parse(deployment_file, tmp_path)

    assert document.id == generate_document_id(deployment_file.relative_to(tmp_path).as_posix())

def test_should_parse_non_kubernetes_yaml(tmp_path):
    YAML_content = """
rules:
  - pattern: foo
"""
    yaml_dir = tmp_path / "eks"
    yaml_dir.mkdir()
    deployment_file = yaml_dir / "deployment.yaml"
    deployment_file.write_text(YAML_content, encoding="utf-8")

    parser = YAMLParser()
    document = parser.parse(deployment_file, tmp_path)

    assert document.content == YAML_content