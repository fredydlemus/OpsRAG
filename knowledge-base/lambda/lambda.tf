variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "private_subnet_ids" {
  type = list(string)
  default = [
    "subnet-0a11b22c33d44e501",
    "subnet-0a11b22c33d44e502"
  ]
}

variable "sns_topic_arn" {
  type    = string
  default = "arn:aws:sns:us-east-1:123456789012:prod-order-events"
}

resource "aws_iam_role" "order_events_publisher" {
  name = "prod-order-events-publisher-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_security_group" "lambda" {
  name        = "prod-lambda-sg"
  description = "Egress for order events publisher Lambda"
  vpc_id      = "vpc-0f1a2b3c4d5e6f70a"

  egress {
    description = "HTTPS egress for AWS APIs"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description     = "PostgreSQL to orders RDS"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = ["sg-0rdsorders1234567"]
  }
}

resource "aws_lambda_function" "order_events_publisher" {
  function_name = "prod-order-events-publisher"
  runtime       = "nodejs20.x"
  handler       = "dist/handler.publish"
  role          = aws_iam_role.order_events_publisher.arn
  filename      = "build/order-events-publisher.zip"
  timeout       = 15
  memory_size   = 512

  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      NODE_ENV       = "production"
      SNS_TOPIC_ARN  = var.sns_topic_arn
      DB_HOST        = "prod-orders-db.cluster-c8example.us-east-1.rds.amazonaws.com"
      DB_PORT        = "5432"
      DB_SECRET_NAME = "prod/orders-api/db"
    }
  }
}
