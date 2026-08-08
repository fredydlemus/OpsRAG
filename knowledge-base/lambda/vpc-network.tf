locals {
  vpc_id             = "vpc-0f1a2b3c4d5e6f70a"
  private_subnet_ids = ["subnet-0a11b22c33d44e501", "subnet-0a11b22c33d44e502"]
}

resource "aws_route_table" "private_a" {
  vpc_id = local.vpc_id

  route {
    cidr_block = "10.24.0.0/16"
    gateway_id = "local"
  }

  tags = {
    Name        = "prod-private-a"
    Environment = "production"
  }
}

resource "aws_route_table" "private_b" {
  vpc_id = local.vpc_id

  route {
    cidr_block = "10.24.0.0/16"
    gateway_id = "local"
  }

  tags = {
    Name        = "prod-private-b"
    Environment = "production"
  }
}

resource "aws_route_table_association" "private_a" {
  subnet_id      = "subnet-0a11b22c33d44e501"
  route_table_id = aws_route_table.private_a.id
}

resource "aws_route_table_association" "private_b" {
  subnet_id      = "subnet-0a11b22c33d44e502"
  route_table_id = aws_route_table.private_b.id
}

resource "aws_vpc_endpoint" "s3" {
  vpc_id            = local.vpc_id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [aws_route_table.private_a.id, aws_route_table.private_b.id]

  tags = {
    Name = "prod-s3-gateway-endpoint"
  } 
}

resource "aws_db_subnet_group" "orders" {
  name       = "prod-orders-db-subnets"
  subnet_ids = local.private_subnet_ids
}

resource "aws_security_group_rule" "lambda_to_rds" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = "sg-0rdsorders1234567"
  source_security_group_id = "sg-0lambdaegress1234"
  description              = "Allow order publisher Lambda to reach orders PostgreSQL"
}
