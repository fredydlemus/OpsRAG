from opsrag.ingestion.parsers.yaml_parser import extract_yaml_metadata
import pytest
import yaml

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