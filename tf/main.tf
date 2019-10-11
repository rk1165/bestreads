provider "aws" {
  region = "us-east-2"
}

# Security group for rds instance
resource "aws_security_group" "rds_sg" {
  name = "rds_sg"
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create a RDS DB instance
resource "aws_db_instance" "postgresql" {
  engine                 = "postgres"
  engine_version         = "15.2"
  identifier             = "myrdsinstance"
  allocated_storage      = 32
  instance_class         = "db.t3.micro"
  username               = var.username
  password               = var.password
  db_name                = var.password
  parameter_group_name   = "default.postgres15"
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  skip_final_snapshot    = true
  publicly_accessible    = true
}
