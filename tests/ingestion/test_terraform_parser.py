from opsrag.ingestion.parsers.terraform import TerraformParser
from opsrag.ingestion.utils import calculate_checksum, generate_document_id

def test_should_parse_a_tf_file_correctly(tmp_path):
    terraform_content = """
    resource "aws_lambda_function" "processor" {
  function_name = "processor"
  }
    """

    terraform_dir = tmp_path / "lambda"
    terraform_dir.mkdir()
    lambda_file = terraform_dir / "lambda.tf"
    lambda_file.write_text(terraform_content, encoding="utf-8")

    parser = TerraformParser()
    document = parser.parse(lambda_file, tmp_path)

    assert document.content == terraform_content
    assert document.domain == "lambda"
    assert document.source == "lambda/lambda.tf"
    assert document.file_type == "terraform"

def test_document_checksum_is_calculated_from_raw_content(tmp_path):
    terraform_content = """
    resource "aws_lambda_function" "processor" {
  function_name = "processor"
  }
    """

    terraform_dir = tmp_path / "lambda"
    terraform_dir.mkdir()
    lambda_file = terraform_dir / "lambda.tf"
    lambda_file.write_text(terraform_content, encoding="utf-8")

    parser = TerraformParser()
    document = parser.parse(lambda_file, tmp_path)

    assert document.checksum == calculate_checksum(terraform_content)

def test_document_id_is_generated_from_source(tmp_path):
    terraform_content = """
    resource "aws_lambda_function" "processor" {
  function_name = "processor"
  }
    """

    terraform_dir = tmp_path / "lambda"
    terraform_dir.mkdir()
    lambda_file = terraform_dir / "lambda.tf"
    lambda_file.write_text(terraform_content, encoding="utf-8")

    parser = TerraformParser()
    document = parser.parse(lambda_file, tmp_path)

    assert document.id == generate_document_id(lambda_file.relative_to(tmp_path).as_posix())
