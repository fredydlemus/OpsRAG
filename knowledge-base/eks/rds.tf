variable "aws_region" {
  type    = string
  default = "us-east-1"
}

resource "aws_security_group" "orders_rds" {
  name        = "prod-orders-rds-sg"
  description = "PostgreSQL access for prod orders database"
  vpc_id      = "vpc-0f1a2b3c4d5e6f70a"

  ingress {
    description     = "PostgreSQL from EKS worker nodes"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = ["sg-0eksnodesprod987"]
  }

  egress {
    description = "Return traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["10.24.0.0/16"]
  }

  tags = {
    Name        = "prod-orders-rds-sg"
    Environment = "production"
    Service     = "orders-api"
  }
}

resource "aws_db_subnet_group" "orders" {
  name       = "prod-orders-db-subnets"
  subnet_ids = ["subnet-0a11b22c33d44e501", "subnet-0a11b22c33d44e502"]
}

resource "aws_rds_cluster" "orders" {
  cluster_identifier      = "prod-orders-db"
  engine                  = "aurora-postgresql"
  engine_version          = "15.5"
  database_name           = "orders"
  port                    = 5432
  db_subnet_group_name    = aws_db_subnet_group.orders.name
  vpc_security_group_ids  = [aws_security_group.orders_rds.id]
  storage_encrypted       = true
  backup_retention_period = 7
  deletion_protection     = true
  master_username         = "orders_admin"
  master_password         = "<REDACTED>"

  tags = {
    Name               = "prod-orders-db"
    Environment        = "production"
    operational_status = "available"
    endpoint           = "prod-orders-db.cluster-c8example.us-east-1.rds.amazonaws.com"
  }
}

resource "aws_rds_cluster_instance" "orders_writer" {
  identifier           = "prod-orders-db-1"
  cluster_identifier   = aws_rds_cluster.orders.id
  instance_class       = "db.r6g.large"
  engine               = aws_rds_cluster.orders.engine
  publicly_accessible  = false
  db_subnet_group_name = aws_db_subnet_group.orders.name
}
