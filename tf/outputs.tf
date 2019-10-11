output "hostname" {
  value       = aws_db_instance.postgresql.address
  description = "Public DNS name of database instance"
}

output "port" {
  value       = aws_db_instance.postgresql.port
  description = "Port of database instance"
}

output "endpoint" {
  value       = aws_db_instance.postgresql.endpoint
  description = "Public DNS name and port separated by a colon"
}
