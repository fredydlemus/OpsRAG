from opsrag.ingestion.parsers.selector import get_parser
from opsrag.ingestion.parsers.markdown import MarkdownParser
from opsrag.ingestion.parsers.terraform import TerraformParser
from opsrag.ingestion.parsers.text import TextParser
from opsrag.ingestion.parsers.yaml_parser import YAMLParser
import pytest

def test_should_return_MarkdownParser_for_md_files(tmp_path):
    file = tmp_path / "runbook.md"
    file.write_text("", encoding="utf-8")

    parser = get_parser(file)

    assert isinstance(parser, MarkdownParser)

def test_should_return_TerraformParser_for_tf_files(tmp_path):
    file = tmp_path / "lambda.tf"
    file.write_text("", encoding="utf-8")

    parser = get_parser(file)

    assert isinstance(parser, TerraformParser)

def test_should_return_TextParser_for_log_files(tmp_path):
    file = tmp_path / "error.log"
    file.write_text("", encoding="utf-8")

    parser = get_parser(file)

    assert isinstance(parser, TextParser)

def test_should_return_TextParser_for_txt_files(tmp_path):
    file = tmp_path / "error.txt"
    file.write_text("", encoding="utf-8")

    parser = get_parser(file)

    assert isinstance(parser, TextParser)

def test_should_return_YAMLParser_for_yml_files(tmp_path):
    file = tmp_path / "deployment.yml"
    file.write_text("", encoding="utf-8")

    parser = get_parser(file)

    assert isinstance(parser, YAMLParser)

def test_should_return_YAMLParser_for_yaml_files(tmp_path):
    file = tmp_path / "deployment.yaml"
    file.write_text("", encoding="utf-8")

    parser = get_parser(file)

    assert isinstance(parser, YAMLParser)

def test_should_raise_an_error_when_the_file_type_is_unsupported(tmp_path):
    file = tmp_path / "doc.pdf"
    file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError):
        get_parser(file)

